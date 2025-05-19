from typing import Literal, Optional, TypedDict


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
