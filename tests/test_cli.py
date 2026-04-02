from click.testing import CliRunner
from pytest_mock import MockerFixture

from http_status_checker.cli import main

def test_cli_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "Usage: check-urls" in result.output

def test_cli_main_single_url_success(mocker: MockerFixture):
    url = "https://example.com"
    mock_check = mocker.patch("http_status_checker.cli.check_urls")
    mock_check.return_value = {url: "200 OK"}

    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url,), 5)

    assert "--- Results ---" in result.output
    assert url in result.output
    assert "-> 200 OK" in result.output

def test_cli_main_timeout_option(mocker: MockerFixture):
    url = "https://example.com"
    timeout = 10
    mock_check = mocker.patch("http_status_checker.cli.check_urls")
    mock_check.return_value = {url: "Timeout"}

    runner = CliRunner()
    result = runner.invoke(main, [url, "--timeout", str(timeout)])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url,), timeout)

    assert "--- Results ---" in result.output
    assert url in result.output
    assert "Timeout" in result.output