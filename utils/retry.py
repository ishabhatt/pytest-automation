# utils/retry.py
import logging
from functools import wraps

from selenium.common import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait

from utils.diagnostics import capture_browser_diagnostics

logger = logging.getLogger(__name__)


def wait_for_page_ready(driver, timeout: float) -> None:
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def retry_on_exception(
    attempts: int, delay: float, exceptions=None, capture_diagnostics=True
):
    if exceptions is None:
        exceptions = (
            StaleElementReferenceException,
            ElementClickInterceptedException,
            ElementNotInteractableException,
            TimeoutException,
        )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page_object = args[0]
            driver = page_object.driver

            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == attempts:
                        logger.warning(
                            "Retry %s/%s failed for %s due to %s. No attempts left.",
                            attempt,
                            attempts,
                            func.__name__,
                            type(e).__name__,
                        )
                        if capture_diagnostics:
                            capture_browser_diagnostics(
                                driver, name=f"{func.__name__}_failure"
                            )
                        raise

                    backoff_delay = delay * (2 ** (attempt - 1))
                    logger.warning(
                        "Retry %s/%s for %s due to %s. Waiting %.2fs before retry.",
                        attempt,
                        attempts,
                        func.__name__,
                        type(e).__name__,
                        backoff_delay,
                    )

                    try:
                        wait_for_page_ready(driver, timeout=backoff_delay)
                    except TimeoutException:
                        logger.warning("Page did not reach readyState=complete")

        return wrapper

    return decorator
