# Price Tracker

v1.0.0

Monitor product prices across Amazon, eBay, Walmart, and Best Buy to identify arbitrage opportunities and profit margins. Use when finding products to flip, monitoring competitor pricing, tracking price history, identifying arbitrage opportunities, or setting automated price alerts.

## Overview

Track product prices across multiple e-commerce platforms to identify arbitrage opportunities, profit margins, and optimal buying/selling windows. This skill enables automated price monitoring, historical tracking, and revenue-focused decision making.

## Core Capabilities

### 1. Product Discovery & Monitoring
- Search products by keyword across Amazon, eBay, Walmart, Best Buy
- Add products to monitoring lists
- Set target price thresholds
- Configure alert frequency (hourly, daily, weekly)

### 2. Arbitrage Analysis
- Compare identical product prices across platforms
- Calculate profit margins after fees and shipping
- Identify flip-worthy opportunities (20%+ margin after costs)

### 3. Historical Price Tracking
- Track price changes over time (30, 60, 90 days)
- Identify seasonal pricing patterns
- Export historical data for analysis

## Quick Start

### Track a Single Product
```bash
python3 scripts/track_product.py \
  --product "Apple iPhone 15 Pro 256GB" \
  --platforms amazon,ebay \
  --alert-below 800 \
  --alert-margin 0.20
```

### Price Comparison Report
```bash
python3 scripts/compare_prices.py \
  --keyword "Sony WH-1000XM5" \
  --platforms amazon,ebay,walmart,bestbuy \
  --report markdown
```

### Bulk Monitor from CSV
```bash
python3 scripts/bulk_monitor.py \
  --csv products.csv \
  --margin-threshold 0.25 \
  --alert-frequency daily
```

## Limitations

- **Currently uses mock data** - requires API integration for production
- Platform API rate limits may affect search frequency
- Some platforms restrict scraping (comply with ToS)

## Installation

```bash
# Install via clawhub (if not rate limited)
npx clawhub@latest install price-tracker

# Or copy this folder to your workspace skills directory
```
