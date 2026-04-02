import logging
import click
from typing import Collection

from http_status_checker.checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s  %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option(
    "--timeout",
    default=5,
    help="Timeout for each request in seconds.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging.",
)
def main(urls: Collection, timeout: int, verbose: bool):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

    logger.info(f" Received urls: {urls}")
    logger.info(f"Received timeout: {timeout}")
    logger.info(f"Received verbose: {verbose}")

    if not urls:
        logger.warning(
            "No URLs provided. Please provide at least one URL to check."
        )
        click.echo("Usage: check-urls <URL1> <URL2> ...")
        return

    logger.info(f"Starting to check {len(urls)} URLs.")

    results = check_urls(urls, timeout)

    click.echo("\n--- Results ---")
    for url, status in results.items():
        if "OK" in status:
            fg_color = "green"
        else:
            fg_color = "red"

        click.secho(f"{url:<40} -> {status}", fg=fg_color)
