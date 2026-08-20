---
name: etsy-api
description: Etsy Open API v3 for managing listings, orders, receipts, reviews, and OAuth token refresh, including fee calculation.
version: 1.0.0
tags: [latest]
---

# Etsy Open API v3

Full read/write access to Etsy's Open API v3 for managing shop listings, orders/receipts, reviews, images, and OAuth2 PKCE token lifecycle.

## Setup

### Environment Variables

- `ETSY_CLIENT_ID` — OAuth2 client ID (e.g. `YOUR_CLIENT_ID`)
- `ETSY_ACCESS_TOKEN` — Bearer token (format: `{user_id}.{token}`)
- `ETSY_REFRESH_TOKEN` — Refresh token (format: `{user_id}.{token}`)
- `ETSY_SHOP_ID` — Shop ID (e.g. `YOUR_SHOP_ID`)

### Authentication

All requests require two headers:

```
Authorization: Bearer {ETSY_ACCESS_TOKEN}
x-api-key: {ETSY_CLIENT_ID}
```

**IMPORTANT**: `x-api-key` is ONLY the client ID. Do NOT append `:shared_secret`.

### Token Storage

Tokens are stored in an Airtable Brand Info table (`YOUR_AIRTABLE_TABLE_ID`) fields `Etsy Access Token` and `Etsy Refresh Token` so n8n workflows can load them dynamically.

## Gotchas

1. **Amounts are objects** — `{ "amount": 2650, "divisor": 100, "currency_code": "USD" }` → divide `amount / divisor` for dollars
2. **Pagination uses offset** — not page numbers. Max `limit=100` per request
3. **State filtering** — must specify one state per request (`active`, `inactive`, `draft`, `sold_out`, `expired`)
4. **Listing IDs** — can arrive as floats; always cast to int/string for lookups
5. **Refresh token rotation** — each refresh returns a NEW refresh token; always persist both
6. **PKCE required** — OAuth2 mandates `code_challenge` + `code_challenge_method=S256`
7. **Token format** — includes user ID prefix: `{user_id}.token_string`. Never strip the prefix
8. **No num_sold** — v3 doesn't expose total sales count on listing objects
9. **Rate limits** — 429 with `Retry-After` header (usually 5-30s)

## OAuth2 PKCE Flow

### Generate PKCE Codes

```python
import hashlib, base64, secrets

code_verifier = secrets.token_urlsafe(64)[:128]
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip('=')
```

### Authorization URL

```
https://www.etsy.com/oauth/connect?
  response_type=code
  &client_id={CLIENT_ID}
  &redirect_uri=http://localhost:3001/callback
  &scope=address_r address_w billing_r cart_r cart_w email_r favorites_r favorites_w feedback_r listings_d listings_r listings_w profile_r profile_w recommend_r recommend_w shops_r shops_w transactions_r transactions_w
  &state={RANDOM_STATE}
  &code_challenge={CODE_CHALLENGE}
  &code_challenge_method=S256
```

### Token Exchange

```bash
curl -X POST "https://api.etsy.com/v3/public/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&client_id=$ETSY_CLIENT_ID&redirect_uri=http://localhost:3001/callback&code={CODE}&code_verifier={CODE_VERIFIER}"
```

### Token Refresh

```bash
curl -X POST "https://api.etsy.com/v3/public/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&client_id=$ETSY_CLIENT_ID&refresh_token=$ETSY_REFRESH_TOKEN"
```

Response:

```json
{
  "access_token": "{user_id}.new_token_string",
  "refresh_token": "{user_id}.new_refresh_string",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Always persist both tokens after refresh.**

## API Reference

Base URL: `https://openapi.etsy.com/v3/application`

Alternate base (some endpoints): `https://api.etsy.com/v3/application`

### User / Shop

#### Get Current User

```bash
curl "https://openapi.etsy.com/v3/application/users/me" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

#### Get Shop Info

```bash
curl "https://openapi.etsy.com/v3/application/shops/$ETSY_SHOP_ID" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Listings

#### List Shop Listings

```bash
curl "https://openapi.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings?state=active&limit=100&offset=0&includes=Images" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

Query parameters: `state` (active|inactive|draft|sold_out|expired), `limit` (1-100), `offset`, `includes` (Images), `sort_on` (created|updated|score), `sort_order` (asc|desc)

Response:

```json
{
  "count": 157,
  "results": [
    {
      "listing_id": 123456789,
      "title": "Funny Cat T-Shirt",
      "description": "...",
      "state": "active",
      "views": 42,
      "num_favorers": 5,
      "taxonomy_id": 123,
      "tags": ["funny", "cat", "tshirt"],
      "quantity": 100,
      "price": { "amount": 1999, "divisor": 100, "currency_code": "USD" },
      "created_timestamp": 1700000000,
      "updated_timestamp": 1700100000,
      "images": [{ "url_fullxfull": "https://..." }]
    }
  ]
}
```

#### Create Listing

```bash
curl -X POST "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Product",
    "description": "Description here",
    "quantity": 100,
    "price": 19.99,
    "taxonomy_id": 123,
    "when_made": "2020_2024",
    "who_made": "i_did",
    "is_supply": false,
    "should_auto_renew": true,
    "type": "physical",
    "tags": ["tag1", "tag2"],
    "shipping_profile_id": 123
  }'
```

#### Update Listing

```bash
curl -X PATCH "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings/{LISTING_ID}" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "tags": ["new", "tags"]}'
```

#### Delete Listing

```bash
curl -X DELETE "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings/{LISTING_ID}" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

#### Get Listing by ID

```bash
curl "https://openapi.etsy.com/v3/application/listings/{LISTING_ID}?includes=Images" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Listing Images

#### Upload Listing Image

```bash
curl -X POST "https://openapi.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings/{LISTING_ID}/images" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID" \
  -F "image=@/path/to/image.jpg" \
  -F "rank=1"
```

#### Delete Listing Image

```bash
curl -X DELETE "https://openapi.etsy.com/v3/application/shops/$ETSY_SHOP_ID/listings/{LISTING_ID}/images/{IMAGE_ID}" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Orders / Receipts

#### List Shop Receipts

```bash
curl "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/receipts?limit=100&offset=0" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

Query parameters: `limit` (1-100), `offset`, `min_created`, `max_created` (unix timestamps), `was_shipped` (true|false), `was_paid` (true|false)

Response:

```json
{
  "count": 642,
  "results": [
    {
      "receipt_id": 123456789,
      "create_timestamp": 1700000000,
      "name": "Customer Name",
      "city": "City",
      "state": "ST",
      "country_iso": "US",
      "status": "Paid",
      "was_shipped": false,
      "message_from_buyer": "...",
      "is_gift": false,
      "subtotal": { "amount": 2000, "divisor": 100, "currency_code": "USD" },
      "total_shipping_cost": { "amount": 500, "divisor": 100, "currency_code": "USD" },
      "total_tax_cost": { "amount": 150, "divisor": 100, "currency_code": "USD" },
      "discount_amt": { "amount": 0, "divisor": 100, "currency_code": "USD" },
      "grandtotal": { "amount": 2650, "divisor": 100, "currency_code": "USD" },
      "transactions": [
        {
          "transaction_id": 987654321,
          "listing_id": 123456789,
          "title": "Product Name",
          "quantity": 1,
          "price": { "amount": 1999, "divisor": 100, "currency_code": "USD" },
          "sku": "SHOP-CAT-DESIGN-TYPE-COLOR-SIZE",
          "is_from_offsite_ads": false,
          "variations": [
            { "formatted_name": "Color", "formatted_value": "Blue" }
          ]
        }
      ]
    }
  ]
}
```

#### Get Receipt by ID

```bash
curl "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/receipts/{RECEIPT_ID}" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Reviews

#### List Shop Reviews

```bash
curl "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/reviews?limit=100&offset=0" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Shipping Profiles

#### List Shipping Profiles

```bash
curl "https://api.etsy.com/v3/application/shops/$ETSY_SHOP_ID/shipping-profiles" \
  -H "Authorization: Bearer $ETSY_ACCESS_TOKEN" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

### Taxonomy

#### Get Seller Taxonomy

```bash
curl "https://openapi.etsy.com/v3/application/seller-taxonomy/nodes" \
  -H "x-api-key: $ETSY_CLIENT_ID"
```

No auth required — public endpoint.

## Fee Calculations

Etsy charges multiple fees per order:

| Fee | Formula |
|-----|---------|
| Listing fee | $0.20 per item quantity |
| Transaction fee | 6.5% of item subtotal |
| Payment processing | 3% of grandtotal + $0.25 |
| Offsite ads | 15% of item total (only if `is_from_offsite_ads: true`) |

### Amount Helper

```python
def etsy_amount(obj):
    """Convert Etsy amount object to float dollars."""
    if not obj:
        return 0.0
    return (obj.get("amount", 0)) / (obj.get("divisor", 100))
```

### Fee Calculation

```python
def calculate_etsy_fees(receipt):
    subtotal = etsy_amount(receipt.get("subtotal"))
    grandtotal = etsy_amount(receipt.get("grandtotal"))
    total_qty = sum(t.get("quantity", 1) for t in receipt.get("transactions", []))

    listing_fee = round(0.20 * total_qty, 2)
    transaction_fee = round(subtotal * 0.065, 2)
    processing_fee = round(grandtotal * 0.03 + 0.25, 2)

    offsite_ads_fee = 0.0
    for txn in receipt.get("transactions", []):
        if txn.get("is_from_offsite_ads"):
            item_total = etsy_amount(txn.get("price")) * txn.get("quantity", 1)
            offsite_ads_fee += round(item_total * 0.15, 2)

    return {
        "listing_fee": listing_fee,
        "transaction_fee": transaction_fee,
        "processing_fee": processing_fee,
        "offsite_ads_fee": offsite_ads_fee,
        "total_fees": round(listing_fee + transaction_fee + processing_fee + offsite_ads_fee, 2),
    }
```

## n8n Code Patterns

### Token Refresh in n8n

```javascript
const tokenResp = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.etsy.com/v3/public/oauth/token',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: `grant_type=refresh_token&client_id=${ETSY_CLIENT_ID}&refresh_token=${ETSY_REFRESH_TOKEN}`
});
const ETSY_ACCESS_TOKEN = tokenResp.access_token;
const newRefreshToken = tokenResp.refresh_token;

// Persist new tokens to Airtable Brand Info
await this.helpers.httpRequest({
  method: 'PATCH',
  url: `https://api.airtable.com/v0/${YOUR_AIRTABLE_BASE}/${YOUR_BRAND_TABLE}`,
  headers: { 'Authorization': `Bearer ${AIRTABLE_PAT}`, 'Content-Type': 'application/json' },
  body: {
    records: [{
      id: brandRecordId,
      fields: { 'Etsy Access Token': ETSY_ACCESS_TOKEN, 'Etsy Refresh Token': newRefreshToken }
    }]
  }
});
```

### Paginated Listing Fetch

```javascript
let allListings = [];
let offset = 0;
let hasMore = true;
while (hasMore) {
  const resp = await this.helpers.httpRequest({
    method: 'GET',
    url: `https://api.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings`,
    headers: {
      'x-api-key': ETSY_CLIENT_ID,
      'Authorization': `Bearer ${ETSY_ACCESS_TOKEN}`
    },
    qs: { state: 'active', limit: 100, offset }
  });
  allListings = allListings.concat(resp.results || []);
  hasMore = resp.results && resp.results.length === 100;
  offset += 100;
}
```

## Rate Limiting

- 429 responses include `Retry-After` header
- Implement retry with backoff (5-30 seconds typical wait)
- Token refresh also subject to rate limits

```python
def etsy_get(url, params=None):
    for attempt in range(3):
        r = requests.get(url, headers=ETSY_HEADERS, params=params, timeout=60)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 5))
            time.sleep(wait)
            continue
        if r.status_code == 401:
            refresh_tokens()
            continue
        return r
    return r
```

## Pagination

Etsy uses offset-based pagination:

- `limit`: 1-100 (max 100)
- `offset`: starting position
- Response includes `count` (total results)
- When `len(results) < limit`, you've reached the end
- **Cannot use other filters with different states** — query each state separately

## Changelog

### v1.0.0

- Initial release with full Etsy Open API v3 coverage
- OAuth2 PKCE flow with token refresh
- Listings CRUD, images, receipts, reviews
- Fee calculation formulas
- n8n code patterns with Airtable token persistence
- Production gotchas
