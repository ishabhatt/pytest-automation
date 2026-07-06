# utils/diagnostics.py
import logging

import allure

logger = logging.getLogger(__name__)


def capture_browser_diagnostics(driver, name: str) -> None:
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"{name}_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        logger.warning("Failed to capture screenshot: %s", exc)

    try:
        allure.attach(
            driver.page_source,
            name=f"{name}_page_source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:
        logger.warning("Failed to capture page source: %s", exc)

    try:
        console_logs = driver.get_log("browser")
        allure.attach(
            str(console_logs),
            name=f"{name}_browser_console_logs",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception as exc:
        logger.warning("Browser console logs unavailable: %s", exc)

    try:
        network_logs = driver.get_log("performance")
        allure.attach(
            str(network_logs),
            name=f"{name}_network_logs",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception as exc:
        logger.warning("Network logs unavailable: %s", exc)
