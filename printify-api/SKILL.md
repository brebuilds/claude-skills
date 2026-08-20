---
name: printify-api
description: Printify REST API v1 for managing products, orders, images, catalog, and publishing to sales channels, including production cost tracking.
version: 1.0.0
tags: [latest]
---

# Printify API v1

Full read/write access to Printify's REST API for managing print-on-demand products, orders, image uploads, catalog browsing, and publishing to connected sales channels.

## Setup

### Environment Variables

- `PRINTIFY_TOKEN` — Bearer API token (JWT, long-lived, expires 2027-04-18)
- `PRINTIFY_SHOP_ID` — Shop ID (e.g. `YOUR_SHOP_ID`)

### Authentication

All requests require:

```
Authorization: Bearer {PRINTIFY_TOKEN}
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) YourApp/1.0
```

### Token Scopes

`shops.manage`, `shops.read`, `catalog.read`, `orders.read`, `orders.write`, `products.read`, `products.write`, `webhooks.read`, `webhooks.write`, `uploads.read`, `uploads.write`, `print_providers.read`, `user.info`

## Gotchas

1. **Prices in cents** — All prices (cost, price, shipping) are integers in cents. Divide by 100 for dollars, multiply by 100 when sending.
2. **Custom User-Agent required** — Cloudflare blocks Python's default `python-urllib` user-agent. Always include a browser-like User-Agent string.
3. **`.json` suffix required** — All endpoints MUST end with `.json` (e.g., `/shops/{id}/products.json`). Omitting it causes 404s.
4. **Variant IDs NOT globally unique** — Same variant ID can appear across different products. Always use composite key: `product_id + variant_id`.
5. **Tracking field name** — Shipments use `number` not `tracking_number`. Check both fields with fallback.
6. **Pagination uses `page`** — Not offset. Response includes `current_page` and `last_page`. Stop when `current_page >= last_page`.
7. **External IDs** — `product.external.id` contains the connected Etsy listing ID. `metadata.shop_order_id` contains the Etsy receipt ID.
8. **Order status values** — `pending`, `on-hold`, `sending-to-production`, `in-production`, `shipped`, `partially-shipped`, `fulfilled`, `delivered`, `canceled`, `cancelled` (both spellings exist).
9. **Rate limiting** — 429 responses with `Retry-After` header. Also watch for 403s from Cloudflare (retry after 3s).
10. **Date formats** — Mixed: `"2026-02-16 06:05:05+00:00"` (with space) and ISO 8601. Parse with timezone awareness.

## API Reference

Base URL: `https://api.printify.com/v1`

### Products

#### List Products (Paginated)

```bash
curl "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products.json?page=1&limit=50" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

Response:

```json
{
  "current_page": 1,
  "last_page": 3,
  "data": [
    {
      "id": "product_id",
      "title": "Funny Cat Tee",
      "blueprint_id": 123,
      "print_provider_id": 99,
      "description": "...",
      "tags": ["funny", "cat"],
      "images": [{ "src": "https://...", "position": 0 }],
      "variants": [
        {
          "id": 12345,
          "title": "S / Black",
          "sku": "SHOP-CAT-DESIGN-TYPE-COLOR-SIZE",
          "cost": 753,
          "price": 1642,
          "is_enabled": true,
          "is_available": true
        }
      ],
      "external": {
        "id": "etsy_listing_id",
        "handle": "/shop/YourShopName/listing/123456789"
      }
    }
  ]
}
```

#### Get Product by ID

```bash
curl "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products/{PRODUCT_ID}.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

#### Create Product

```bash
curl -X POST "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "title": "New Design Tee",
    "description": "Description here",
    "tags": ["tag1", "tag2"],
    "blueprint_id": 123,
    "print_provider_id": 99,
    "variants": [
      { "id": 12345, "price": 1999, "is_enabled": true }
    ],
    "print_areas": [
      {
        "variant_ids": [12345, 12346],
        "placeholders": [
          {
            "position": "front",
            "images": [
              {
                "id": "printify_image_id",
                "x": 0.5, "y": 0.5,
                "scale": 1, "angle": 0
              }
            ]
          }
        ]
      }
    ]
  }'
```

#### Update Product (Variants/SKUs)

```bash
curl -X PUT "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products/{PRODUCT_ID}.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "variants": [
      {
        "id": 12345,
        "sku": "SHOP-CAT-DESIGN-TYPE-COLOR-SIZE",
        "price": 1642,
        "is_enabled": true
      }
    ]
  }'
```

#### Delete Product

```bash
curl -X DELETE "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products/{PRODUCT_ID}.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

### Publishing

#### Publish Product to Sales Channel

```bash
curl -X POST "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/products/{PRODUCT_ID}/publish.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "title": true,
    "description": true,
    "images": true,
    "variants": true,
    "tags": true
  }'
```

Set fields to `true` to sync that field to the connected channel (Etsy), or `false` to skip.

### Orders

#### List Orders (Paginated)

```bash
curl "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/orders.json?page=1&limit=50" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

Response:

```json
{
  "current_page": 1,
  "last_page": 1,
  "data": [
    {
      "id": "order_id",
      "status": "shipped",
      "metadata": {
        "shop_order_id": "etsy_receipt_id",
        "order_type": "etsy"
      },
      "total_price": 5000,
      "total_shipping": 0,
      "line_items": [
        {
          "id": "item_id",
          "product_id": "product_id",
          "variant_id": 12345,
          "title": "Product Name",
          "sku": "SHOP-CAT-DESIGN-TYPE-COLOR-SIZE",
          "quantity": 1,
          "cost": 753,
          "shipping_cost": 0,
          "metadata": { "title": "Product Name", "sku": "SKU" }
        }
      ],
      "shipments": [
        {
          "id": "shipment_id",
          "carrier": "USPS",
          "number": "9400111899223100012345",
          "created_at": "2026-02-16 06:05:05+00:00",
          "delivered_at": "2026-02-20T12:00:00+00:00"
        }
      ],
      "created_at": "2026-02-16 06:05:05+00:00",
      "sent_to_production_at": "2026-02-16 08:00:00+00:00",
      "fulfilled_at": "2026-02-20T12:00:00+00:00"
    }
  ]
}
```

#### Get Order by ID

```bash
curl "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/orders/{ORDER_ID}.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

### Image Uploads

#### Upload Image (Base64)

```bash
curl -X POST "https://api.printify.com/v1/uploads/images.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "file_name": "design.png",
    "contents": "base64_encoded_image_data"
  }'
```

Response:

```json
{
  "id": "image_id",
  "file_name": "design.png",
  "height": 4000,
  "width": 4000,
  "size": 1234567,
  "mime_type": "image/png",
  "preview_url": "https://...",
  "upload_time": "2026-02-20T..."
}
```

#### Upload Image (URL)

```bash
curl -X POST "https://api.printify.com/v1/uploads/images.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "file_name": "design.png",
    "url": "https://example.com/design.png"
  }'
```

### Catalog

#### List Blueprints

```bash
curl "https://api.printify.com/v1/catalog/blueprints.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

#### Get Blueprint Print Providers

```bash
curl "https://api.printify.com/v1/catalog/blueprints/{BLUEPRINT_ID}/print_providers.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

#### Get Provider Variants

```bash
curl "https://api.printify.com/v1/catalog/blueprints/{BLUEPRINT_ID}/print_providers/{PROVIDER_ID}/variants.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

Response:

```json
{
  "id": 99,
  "title": "Provider Name",
  "variants": [
    { "id": 12345, "title": "S / Black", "options": { "size": "S", "color": "Black" } },
    { "id": 12346, "title": "M / Black", "options": { "size": "M", "color": "Black" } }
  ]
}
```

#### Get Shipping Info

```bash
curl "https://api.printify.com/v1/catalog/blueprints/{BLUEPRINT_ID}/print_providers/{PROVIDER_ID}/shipping.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

### Shops

#### List Shops

```bash
curl "https://api.printify.com/v1/shops.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

### Webhooks

#### List Webhooks

```bash
curl "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/webhooks.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

#### Create Webhook

```bash
curl -X POST "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/webhooks.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Your-Automation/1.0" \
  -d '{
    "topic": "order:shipped",
    "url": "https://your-automation-host.example.com/webhook/printify-fulfillment"
  }'
```

Topics: `order:created`, `order:updated`, `order:shipped`, `order:completed`, `order:cancelled`, `product:publish:started`, `product:publish:succeeded`, `product:publish:failed`

#### Delete Webhook

```bash
curl -X DELETE "https://api.printify.com/v1/shops/$PRINTIFY_SHOP_ID/webhooks/{WEBHOOK_ID}.json" \
  -H "Authorization: Bearer $PRINTIFY_TOKEN" \
  -H "User-Agent: Your-Automation/1.0"
```

## Cost & Profit Tracking

### Extract Production Costs from Orders

```python
def get_order_costs(order):
    """Extract all costs from a Printify order (cents → dollars)."""
    line_items = order.get("line_items", [])
    total_prod_cost = sum(li.get("cost", 0) for li in line_items) / 100
    total_ship_cost = sum(li.get("shipping_cost", 0) for li in line_items) / 100
    return {
        "production_cost": round(total_prod_cost, 2),
        "shipping_cost": round(total_ship_cost, 2),
        "total_cost": round(total_prod_cost + total_ship_cost, 2),
    }
```

### Match Printify Orders to Etsy Receipts

```python
# Printify order.metadata.shop_order_id == Etsy receipt_id
etsy_receipt_id = str(order["metadata"].get("shop_order_id", ""))
```

## Python Helper

```python
def printify_request(method, path, data=None, retries=3):
    """Make an authenticated Printify API request with retry."""
    import urllib.request, json, time
    url = f'https://api.printify.com/v1/{path}'
    headers = {
        'Authorization': f'Bearer {PRINTIFY_TOKEN}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) YourShopName/1.0',
        'Accept': 'application/json',
    }
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", 5))
                time.sleep(wait)
                continue
            if e.code == 403 and attempt < retries - 1:
                time.sleep(3)
                continue
            return {'error': f'{e.code}: {body[:200]}'}
    return {'error': 'max retries exceeded'}
```

## n8n Code Patterns

### Fetch All Products

```javascript
const PRINTIFY_TOKEN = $env.PRINTIFY_TOKEN;
const PRINTIFY_SHOP = $env.PRINTIFY_SHOP_ID;
const headers = {
  'Authorization': `Bearer ${PRINTIFY_TOKEN}`,
  'User-Agent': 'Your-Automation/1.0'
};

let allProducts = [];
let page = 1;
let hasMore = true;
while (hasMore) {
  const resp = await this.helpers.httpRequest({
    method: 'GET',
    url: `https://api.printify.com/v1/shops/${PRINTIFY_SHOP}/products.json?page=${page}&limit=50`,
    headers
  });
  allProducts = allProducts.concat(resp.data || []);
  hasMore = resp.current_page < resp.last_page;
  page++;
}
```

### Fulfillment Webhook Handler

```javascript
const payload = $input.first().json;
const printifyOrderId = payload.resource?.id;

// Fetch full order details
const order = await this.helpers.httpRequest({
  method: 'GET',
  url: `https://api.printify.com/v1/shops/${PRINTIFY_SHOP}/orders/${printifyOrderId}.json`,
  headers: {
    'Authorization': `Bearer ${PRINTIFY_TOKEN}`,
    'User-Agent': 'Your-Automation/1.0'
  }
});

// Extract tracking & costs
const tracking = order.shipments?.[0]?.number;
const carrier = order.shipments?.[0]?.carrier;
const prodCost = order.line_items.reduce((sum, li) => sum + (li.cost || 0), 0) / 100;
const shipCost = order.line_items.reduce((sum, li) => sum + (li.shipping_cost || 0), 0) / 100;
```

## Pagination

Page-based pagination:

- `page`: starts at 1
- `limit`: up to 100 (default 50)
- Response: `current_page`, `last_page`, `data` array
- Stop when `current_page >= last_page`
- Add 0.3-0.5s sleep between pages to avoid rate limits

## Status Reference

| Status | Description |
|--------|-------------|
| `pending` | Order received, not yet in production |
| `on-hold` | Payment or issue hold |
| `sending-to-production` | Being sent to print provider |
| `in-production` | Currently being printed |
| `shipped` | Shipped with tracking |
| `partially-shipped` | Some items shipped |
| `fulfilled` | All items delivered |
| `delivered` | Confirmed delivery |
| `canceled` / `cancelled` | Cancelled (both spellings) |

## Changelog

### v1.0.0

- Initial release with full Printify API v1 coverage
- Products CRUD, publishing, image uploads
- Orders with shipment tracking and cost extraction
- Catalog browsing (blueprints, providers, variants, shipping)
- Webhook management
- Python and n8n code patterns
- Production gotchas and Etsy receipt matching
