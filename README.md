# Monoprix Receipt Parser

**Monoprix Receipt Parser** is a Python tool that automates scraping your Monoprix account to retrieve your digital receipts.  
It parses each receipt and sends a structured JSON payload to a given webhook endpoint.

## Features

- Login to your Monoprix account
- Fetch and download receipts (PDF format)
- Parse receipt content: shop name, date, articles, discounts, payments
- Serialize parsed data into JSON
- Optionally send the structured data to a webhook
- Control fetching date range and receipt limits

## Usage

This tool is designed to be run via **Docker**, with environment variables to configure its behavior.

### Configuration (Environment Variables)

| Variable             | Description                                         | Type    | Default |
|:---------------------|:----------------------------------------------------|:--------|:--------|
| `MONOPRIX_EMAIL`      | Monoprix account email address                      | String  | **Required** |
| `MONOPRIX_PASSWORD`   | Monoprix account password                           | String  | **Required** |
| `FROM_DATE`           | Start date to fetch receipts (format: `YYYY-MM-DD`) | String  | _Optional_ |
| `FROM_DATE_RELATIVE`  | Start date relative to today (e.g., `-30` for 30 days ago) | Integer | _Optional_ |
| `LIMIT`               | Maximum number of receipts to fetch                | Integer | `5` |
| `WEBHOOK_URL`         | Webhook endpoint to send parsed receipts            | String  | _Optional_ |
| `VERBOSE`             | Enable verbose logging (dumps parsed data)          | Boolean | `False` |

> If both `FROM_DATE` and `FROM_DATE_RELATIVE` are provided, `FROM_DATE` takes precedence.

### Docker Usage

```bash
docker run --rm \
  -e MONOPRIX_EMAIL="your-email@example.com" \
  -e MONOPRIX_PASSWORD="your-password" \
  -e FROM_DATE_RELATIVE=30 \
  -e LIMIT=10 \
  -e WEBHOOK_URL="https://your-post-webhook-url.com" \
  -e VERBOSE=true \
  your-docker-image-name
```

## JSON Payload Format

Each parsed receipt sent to the webhook follows this structure:

```json
{
  "date": "2024-04-20T14:32:00",
  "shop": "MONO LA GARENNE",
  "total_cost": 45.30,
  "total_discount": -5.00,
  "articles": [
    {
      "name": "PAVE DE TRUITE",
      "quantity": 2,
      "unit_price": 3.5,
      "total_cost": 5.25,
      "category": "SURGELES/PRODUITS FRAIS",
      "total_discount": -1.75,
      "cost_without_discount": 7,
      "discount_name": "2e a moins 50%"
    }
  ],
  "discounts": [
    {
      "name": "2e a moins 50%",
      "amount": -1.75
    }
  ],
  "payments": [
    {
      "name": "CARTE BANCAIRE",
      "card_number": "****1234",
      "amount": 5.25
    }
  ]
}
```

## Development

### Requirements

- Python 3.10+

You can run the project locally using:

```bash
MONOPRIX_EMAIL="your-email@example.com" \
MONOPRIX_PASSWORD="your-password" \
FROM_DATE_RELATIVE=30 \
LIMIT=10 \
WEBHOOK_URL="https://your-post-webhook-url.com" \
VERBOSE=true \
uv run src/main.py
```

## Notes

- This tool is designed for personal use. Use responsibly and according to Monoprix’s terms of service.
- This project is **not** affiliated with or endorsed by Monoprix.
