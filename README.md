## python-sentoo

A client library for [Sentoo](https://sentoo.io/)

## Installation

You can install the library using pip:

```bash
pip install sentoo
```
## Usage

To use the library, import it and create a client instance:

```python
from sentoo import Sentoo

sentoo = Sentoo(token='your_token')
```
## Documentation

The Sentoo client provides the following methods:

### Creating a transaction

```python
# Create a new transaction
response = sentoo.transaction_create(
    sentoo_merchant="your_merchant_id",
    sentoo_amount=1000,  # Amount in cents
    sentoo_description="Payment description",
    sentoo_currency="ANG",  # Supported: ANG, AWG, USD, EUR, XCD
    sentoo_return_url="https://your-site.com/callback",
    # Optional parameters
    sentoo_customer="customer_id",  # Optional customer identifier
    sentoo_expires="2023-12-31T23:59:59",  # Optional expiration date
    sentoo_2nd_currency="USD",  # Optional secondary currency
    sentoo_2nd_amount="1200"  # Optional secondary amount
)
```

### Canceling a transaction

```python
# Cancel an existing transaction
response = sentoo.transaction_cancel(
    merchant_id="your_merchant_id",
    transaction_id="transaction_id"
)
```

### Checking transaction status

```python
# Check the status of a transaction
response = sentoo.transaction_status(
    merchant_id="your_merchant_id",
    transaction_id="transaction_id"
)
```

### Getting payment processors

```python
# Get available payment processors for a transaction
response = sentoo.transaction_processors(
    merchant_id="your_merchant_id",
    transaction_id="transaction_id"
)
```
