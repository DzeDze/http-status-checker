import pytest
import requests
from pytest_mock import MockerFixture

from http_status_checker.checker import check_urls


def test_check_urls_success(mocker: MockerFixture):
    mock_request_get = mocker.patch(
        "http_status_checker.checker.requests.get"
    )

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.reason = "OK"
    mock_request_get.return_value = mock_response

    urls = ["https://example.com"]
    results = check_urls(urls)

    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "200 OK"


def test_check_urls_client_error(mocker: MockerFixture):
    mock_request_get = mocker.patch(
        "http_status_checker.checker.requests.get"
    )

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.ok = False
    mock_response.reason = "Not Found"
    mock_request_get.return_value = mock_response

    urls = ["https://example.com/nonexistent"]
    results = check_urls(urls)

    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "404 Not Found"


@pytest.mark.parametrize(
    "exception, expected_status",
    [
        (requests.exceptions.Timeout, "Timeout"),
        (
            requests.exceptions.ConnectionError,
            "Connection Error",
        ),
        (
            requests.exceptions.RequestException,
            "Request Error: RequestException",
        ),
        (ValueError, "Error: ValueError"),
    ],
)
def test_check_urls_request_exception(
    mocker: MockerFixture,
    exception,
    expected_status,
):
    mock_request_get = mocker.patch(
        "http_status_checker.checker.requests.get"
    )

    mock_request_get.side_effect = exception(
        f"Simulated {expected_status}"
    )

    urls = ["https://problem.com"]
    results = check_urls(urls)

    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == expected_status


def test_check_urls_with_multiple_urls(mocker: MockerFixture):
    mock_request_get = mocker.patch(
        "http_status_checker.checker.requests.get"
    )

    # First call: OK
    mock_response_ok = mocker.MagicMock(spec=requests.Response)
    mock_response_ok.status_code = 200
    mock_response_ok.okmock_response_ok = True
    mock_response_ok.reason = "OK"

    # Second call: Timeout
    timeout_exception = requests.exceptions.Timeout(
        "Simulated timeout"
    )

    # Third call: 500 Server Error
    mock_response_failed = mocker.MagicMock(
        spec=requests.Response
    )
    mock_response_failed.status_code = 500
    mock_response_failed.reason = "Internal Server Error"
    mock_response_failed.ok = False

    mock_request_get.side_effect = [
        mock_response_ok,
        timeout_exception,
        mock_response_failed,
    ]

    urls = [
        "https://success.com",
        "https://timeout.com",
        "https://servererror.com",
    ]
    results = check_urls(urls)

    assert len(results) == 3
    assert mock_request_get.call_count == 3
    assert results[urls[0]] == "200 OK"
    assert results[urls[1]] == "Timeout"
    assert results[urls[2]] == "500 Internal Server Error"


def test_check_urls_empty_list():
    urls = []
    results = check_urls(urls)

    assert results == {}


def test_check_urls_custom_timeout(mocker: MockerFixture):
    mock_request_get = mocker.patch(
        "http_status_checker.checker.requests.get"
    )

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.reason = "OK"
    mock_request_get.return_value = mock_response

    urls = ["https://example.com"]
    custom_timeout = 10
    results = check_urls(urls, timeout=custom_timeout)

    mock_request_get.assert_called_once_with(
        urls[0], timeout=custom_timeout
    )
    assert results[urls[0]] == "200 OK"
