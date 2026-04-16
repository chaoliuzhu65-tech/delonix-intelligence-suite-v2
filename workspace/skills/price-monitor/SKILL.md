# Price Monitor

v1.0.0

Monitor website prices, inventory, and content changes using browser automation. Use when tracking e-commerce prices, competitor monitoring, stock alerts, or any web content change detection. Supports scheduled checks, price history logging, and alert notifications.

## Overview

Automated price and content monitoring skill using agent-browser. Tracks price changes, stock availability, and content updates on any website with configurable alerts and history logging.

## Core Capabilities

### 1. Single Product Price Check
```bash
agent-browser open "https://example.com/product/123"
agent-browser snapshot -i
agent-browser get text @e1  # Get price element
```

### 2. Multi-Product Monitoring
Create a products.csv with URLs and selectors:
```csv
url,selector,name
https://site-a.com/product1,.price-tag,Product A
https://site-b.com/item2,#price,Product B
```

### 3. Stock/Inventory Alerts
Monitor for "In Stock" vs "Out of Stock" status changes.

### 4. Price History Tracking
Automatic logging with timestamp for trend analysis.

## Installation

```bash
# Install via clawhub (if not rate limited)
npx clawhub@latest install price-monitor

# Or copy this folder to your workspace skills directory
```

## Usage

```bash
# Run monitoring script
python scripts/monitor_prices.py products.csv --alert-threshold 10
```

## Data Schema

| Field | Description |
|-------|-------------|
| url | Target product webpage |
| selector | CSS selector for price element |
| name | Human-readable product name |
| timestamp | Check date/time |
| price | Extracted price value |

## Limitations

- Requires agent-browser or Playwright
- CSS selectors must be stable
- Some sites block scraping (respect ToS)
