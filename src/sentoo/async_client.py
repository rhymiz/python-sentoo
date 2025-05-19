import httpx
from httpx import Response

from sentoo._compat import CreateTransactionKwargs, get_base_url


class AsyncSentoo:
    """
    AsyncSentoo API client

    An async client for interacting with the Sentoo payment processing API.
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
        self._client = httpx.AsyncClient()

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

    async def transaction_create(self, **kwargs: CreateTransactionKwargs) -> Response:
        """
        Create a new transaction

        Args:
            **kwargs: Transaction parameters as defined in CreateTransactionKwargs

        Returns:
            Response: API response containing transaction details
        """

        url = self._url("/payment/new")
        kwargs["sentoo_merchant"] = self._merchant_id
        self._headers["Content-Type"] = "application/x-www-form-urlencoded"

        async with self._client as client:
            return await client.post(url, headers=self._headers, data=kwargs)

    async def transaction_cancel(self, transaction_id: str) -> Response:
        """
        Cancel an existing transaction

        Args:
            transaction_id (str): The transaction identifier to cancel

        Returns:
            Response: API response containing cancellation result
        """

        url = self._url(f"/payment/cancel/{self._merchant_id}/{transaction_id}")
        async with self._client as client:
            return await client.get(url, headers=self._headers)

    async def transaction_status(self, transaction_id: str) -> Response:
        """
        Check the status of a transaction

        Args:
            transaction_id (str): The transaction identifier to check

        Returns:
            Response: API response containing transaction status
        """

        url = self._url(f"/payment/status/{self._merchant_id}/{transaction_id}")
        async with self._client as client:
            return await client.get(url, headers=self._headers)

    async def transaction_processors(self, transaction_id: str) -> Response:
        """
        Get available payment processors for a transaction

        Args:
            transaction_id (str): The transaction identifier

        Returns:
            Response: API response containing available payment methods
        """

        url = self._url(f"/payment/methods/{self._merchant_id}/{transaction_id}")
        async with self._client as client:
            return await client.get(url, headers=self._headers)
