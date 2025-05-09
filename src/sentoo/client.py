from typing import Any, TypedDict, Literal
from typing import Optional
import httpx


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
    sentoo_merchant: str
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

    def __init__(self, token: str, sandbox: bool = False) -> None:
        """
        Initialize Sentoo API client

        Args:
            token (str): Your Sentoo API secret token
            sandbox (bool): Whether to use sandbox environment. Defaults to False.
        """
        self._token = token
        self._sandbox = sandbox
        self._base_url = get_base_url(self._sandbox)
        self._headers = {"X-SENTOO-SECRET": self._token}

    def _url(self, path: str) -> str:
        """
        Build a complete URL for an API endpoint

        Args:
            path (str): The API endpoint path

        Returns:
            str: Complete URL including base URL and path
        """
        return f"{self._base_url}/{path}"

    def transaction_create(self, **kwargs: CreateTransactionKwargs) -> dict[str, Any]:
        """
        Create a new transaction

        Args:
            **kwargs: Transaction parameters as defined in CreateTransactionKwargs

        Returns:
            dict[str, Any]: API response containing transaction details
        """
        url = self._url("/transactions/new")
        return httpx.post(url, headers=self._headers, json=kwargs)

    def transaction_cancel(self, merchant_id: str, transaction_id: str) -> dict[str, Any]:
        """
        Cancel an existing transaction

        Args:
            merchant_id (str): The merchant identifier
            transaction_id (str): The transaction identifier to cancel

        Returns:
            dict[str, Any]: API response containing cancellation result
        """
        url = self._url(f"/payment/cancel/{merchant_id}/{transaction_id}")
        return httpx.post(url, headers=self._headers)

    def transaction_status(self, merchant_id: str, transaction_id: str) -> dict[str, Any]:
        """
        Check the status of a transaction

        Args:
            merchant_id (str): The merchant identifier
            transaction_id (str): The transaction identifier to check

        Returns:
            dict[str, Any]: API response containing transaction status
        """
        url = self._url(f"/payment/status/{merchant_id}/{transaction_id}")
        return httpx.get(url, headers=self._headers)

    def transaction_processors(self, merchant_id: str, transaction_id: str) -> dict[str, Any]:
        """
        Get available payment processors for a transaction

        Args:
            merchant_id (str): The merchant identifier
            transaction_id (str): The transaction identifier

        Returns:
            dict[str, Any]: API response containing available payment methods
        """
        url = self._url(f"/payment/methods/{merchant_id}/{transaction_id}")
        return httpx.get(url, headers=self._headers)
