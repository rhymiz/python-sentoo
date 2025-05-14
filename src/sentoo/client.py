from typing import Literal, Optional, TypedDict

import httpx
from httpx import Response


def get_base_url(sandbox: bool = False) -> str:
    """
    Retrieve environment specific base url

    Args:
        sandbox (bool): If True, uses sandbox environment. Defaults to False.

    Returns:
        str: The base URL for the API
    """

    if sandbox:
        base_url = "https://api.sandbox.sentoo.io/v1"
    else:
        base_url = "https://api.sentoo.io/v1"
    return base_url


class CreateTransactionKwargs(TypedDict):
    """
    Type definition for transaction creation parameters
    """

    sentoo_amount: int
    sentoo_description: str
    sentoo_currency: Literal["ANG", "AWG", "USD", "EUR", "XCD"]
    sentoo_return_url: str
    sentoo_customer: Optional[str]
    sentoo_expires: Optional[str]
    sentoo_2nd_currency: Optional[str]
    sentoo_2nd_amount: Optional[str]


class Sentoo:
    """
    Sentoo API client

    A client for interacting with the Sentoo payment processing API.
    """

    def __init__(self, secret: str, merchant_id: str, sandbox: bool = False) -> None:
        """
        Initialize Sentoo API client

        Args:
            token (str): Your Sentoo API secret token
            merchant_id (str): Your Sentoo merchant identifier
            sandbox (bool): Whether to use sandbox environment. Defaults to False.
        """
        self._secret = secret
        self._sandbox = sandbox
        self._merchant_id = merchant_id
        self._base_url = get_base_url(self._sandbox)
        self._headers = {"X-SENTOO-SECRET": self._secret}

    def _url(self, path: str) -> str:
        """
        Build a complete URL for an API endpoint

        Args:
            path (str): The API endpoint path

        Returns:
            str: Complete URL including base URL and path
        """

        if path.startswith("/"):
            path = path[1:]
        return f"{self._base_url}/{path}"

    def transaction_create(self, **kwargs: CreateTransactionKwargs) -> Response:
        """
        Create a new transaction

        Args:
            **kwargs: Transaction parameters as defined in CreateTransactionKwargs

        Returns:
            dict[str, Any]: API response containing transaction details
        """
        url = self._url("/payment/new")
        kwargs["sentoo_merchant"] = self._merchant_id
        self._headers["Content-Type"] = "application/x-www-form-urlencoded"
        return httpx.post(url, headers=self._headers, data=kwargs)

    def transaction_cancel(self, transaction_id: str) -> Response:
        """
        Cancel an existing transaction

        Args:
            transaction_id (str): The transaction identifier to cancel

        Returns:
            dict[str, Any]: API response containing cancellation result
        """
        url = self._url(f"/payment/cancel/{self._merchant_id}/{transaction_id}")
        return httpx.get(url, headers=self._headers)

    def transaction_status(self, transaction_id: str) -> Response:
        """
        Check the status of a transaction

        Args:
            transaction_id (str): The transaction identifier to check

        Returns:
            dict[str, Any]: API response containing transaction status
        """
        url = self._url(f"/payment/status/{self._merchant_id}/{transaction_id}")
        return httpx.get(url, headers=self._headers)

    def transaction_processors(self, transaction_id: str) -> Response:
        """
        Get available payment processors for a transaction

        Args:
            transaction_id (str): The transaction identifier

        Returns:
            dict[str, Any]: API response containing available payment methods
        """
        url = self._url(f"/payment/methods/{self._merchant_id}/{transaction_id}")
        return httpx.get(url, headers=self._headers)
