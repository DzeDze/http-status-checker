import logging
import requests


logger = logging.getLogger(__name__)

def check_urls(urls: list[str], timeout: int = 5) -> dict[str, str]:
    """
    Check a list of URLs and return their status.

    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int): The timeout for each request in seconds. Default is 5 seconds.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status string.
    """

    logger.info(
        f"Starting to check for {len(urls)} URLs with a timeout of {timeout} seconds."
    )
    results: dict[str, str] = {}
    for url in urls:
        status = "Unknown"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "Timeout"
            logger.warning(f"Timeout occurred while checking {url}")
        except requests.exceptions.ConnectionError:
            status = "Connection Error"
            logger.warning(f"Connection error occurred while checking {url}")
        except requests.RequestException as e:
            status = f"Request Error: {type(e).__name__}"
            logger.error(
                f"An unexpected error occurred while checking {url}: {e}", 
                exc_info=True,
            )
        except Exception as e:
            status = f"Error: {type(e).__name__}"
            logger.error(
                f"An unexpected error occurred while checking {url}: {e}", 
            )
        results[url] = status
        logger.debug(f"Checked URL: {url:<40} - Status: {status}")
    return results