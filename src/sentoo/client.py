from typing import Unpack

import httpx
from httpx import Response

from ._compat import CreateTransactionKwargs, get_base_url


class Sentoo:
    """
    Sentoo API client

    A client for interacting with the Sentoo payment processing API.
    """

    def __init__(self, secret: str, merchant_id: str, sandbox: bool = False) -> None:
        """
        Initialize Sentoo API client

        Args:
            secret (str): Your Sentoo API secret token
            merchant_id (str): Your Sentoo merchant identifier
            sandbox (bool): Whether to use sandbox environment. Defaults to False.
        """
        self._secret = secret
        self._sandbox = sandbox
        self._merchant_id = merchant_id
        self._base_url = get_base_url(self._sandbox)
        self._headers = {"X-SENTOO-SECRET": self._secret}
        self._client = httpx.Client(headers=self._headers, base_url=self._base_url)

    def transaction_create(self, **kwargs: Unpack[CreateTransactionKwargs]) -> Response:
        """
        Create a new transaction

        Args:
            **kwargs: Transaction parameters as defined in CreateTransactionKwargs

        Returns:
            Response: API response containing transaction details
        """

        kwargs["sentoo_merchant"] = self._merchant_id
        self._headers["Content-Type"] = "application/x-www-form-urlencoded"

        url = "/payment/new"
        return self._client.post(url, headers=self._headers, data=kwargs)

    def transaction_cancel(self, transaction_id: str) -> Response:
        """
        Cancel an existing transaction

        Args:
            transaction_id (str): The transaction identifier to cancel

        Returns:
            Response: API response containing cancellation result
        """

        url = f"/payment/cancel/{self._merchant_id}/{transaction_id}"
        return self._client.get(url, headers=self._headers)

    def transaction_status(self, transaction_id: str) -> Response:
        """
        Check the status of a transaction

        Args:
            transaction_id (str): The transaction identifier to check

        Returns:
            Response: API response containing transaction status
        """

        url = f"/payment/status/{self._merchant_id}/{transaction_id}"
        return self._client.get(url, headers=self._headers)

    def transaction_processors(self, transaction_id: str) -> Response:
        """
        Get available payment processors for a transaction

        Args:
            transaction_id (str): The transaction identifier

        Returns:
            Response: API response containing available payment methods
        """

        url = f"/payment/methods/{self._merchant_id}/{transaction_id}"
        return self._client.get(url, headers=self._headers)
