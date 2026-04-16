#!/usr/bin/env python3
"""
Price Monitor Script
Monitor product prices from CSV and detect changes
"""

import csv
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

# Mock price data for testing (replace with real API calls in production)
MOCK_PRICES = {
    "amazon": {
        "Apple iPhone 15 Pro 256GB": 999.00,
        "Sony WH-1000XM5": 348.00,
        "PlayStation 5 Slim": 449.00,
    },
    "ebay": {
        "Apple iPhone 15 Pro 256GB": 920.00,
        "Sony WH-1000XM5": 320.00,
        "PlayStation 5 Slim": 429.00,
    },
    "walmart": {
        "Apple iPhone 15 Pro 256GB": 979.00,
        "Sony WH-1000XM5": 349.00,
        "PlayStation 5 Slim": 444.00,
    },
    "bestbuy": {
        "Apple iPhone 15 Pro 256GB": 999.00,
        "Sony WH-1000XM5": 349.00,
        "PlayStation 5 Slim": 449.99,
    }
}

def load_products(csv_path: str) -> List[Dict]:
    """Load products from CSV file"""
    products = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append(row)
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_path}")
        print("📝 Creating sample CSV...")
        create_sample_csv(csv_path)
    return products

def create_sample_csv(path: str):
    """Create a sample CSV file for testing"""
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'selector', 'name', 'min_price', 'max_price'])
        writer.writerow(['https://amazon.com/dp/B0CN', '.a-price-whole', 'Sony WH-1000XM5', '200', '400'])
        writer.writerow(['https://amazon.com/dp/B0CJ', '.priceView-hero-price', 'Apple iPhone 15 Pro', '800', '1200'])
    print(f"✅ Sample CSV created: {path}")

def get_price(product_name: str, platform: str = "amazon") -> Optional[float]:
    """Get current price for a product (mock implementation)"""
    # In production, this would call real APIs
    if platform.lower() in MOCK_PRICES:
        return MOCK_PRICES[platform.lower()].get(product_name)
    return MOCK_PRICES["amazon"].get(product_name)

def compare_prices(product_name: str) -> Dict:
    """Compare prices across all platforms"""
    results = {"product": product_name, "platforms": {}}
    min_price = float('inf')
    max_price = 0
    best_platform = ""
    
    for platform, products in MOCK_PRICES.items():
        price = products.get(product_name)
        if price:
            results["platforms"][platform] = price
            if price < min_price:
                min_price = price
                best_platform = platform
            if price > max_price:
                max_price = price
    
    results["min_price"] = min_price
    results["max_price"] = max_price
    results["best_platform"] = best_platform
    results["price_range"] = max_price - min_price
    
    return results

def monitor_products(csv_path: str, alert_threshold: float = 10.0):
    """Monitor products and detect price changes"""
    products = load_products(csv_path)
    
    if not products:
        print("❌ No products to monitor")
        return
    
    print(f"\n📊 Price Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Monitoring {len(products)} products")
    print("=" * 60)
    
    for product in products:
        name = product.get('name', 'Unknown')
        url = product.get('url', '')
        min_price = float(product.get('min_price', 0))
        max_price = float(product.get('max_price', 999999))
        
        # Compare prices across platforms
        comparison = compare_prices(name)
        
        print(f"\n📦 {name}")
        print(f"   URL: {url}")
        print(f"   Price Range: ¥{min_price:.0f} - ¥{max_price:.0f}")
        
        for platform, price in comparison["platforms"].items():
            status = ""
            if price < min_price:
                status = " ✅ BELOW MIN"
            elif price > max_price:
                status = " ⚠️ ABOVE MAX"
            emoji = "💰" if platform == comparison["best_platform"] else "  "
            print(f"   {emoji} {platform.upper()}: ¥{price:.2f}{status}")
        
        if comparison["price_range"] > 0:
            savings = comparison["max_price"] - comparison["min_price"]
            print(f"   💡 Potential savings: ¥{savings:.2f} (shop at {comparison['best_platform'].upper()})")

def main():
    csv_path = "products.csv"
    alert_threshold = 10.0
    
    # Parse arguments
    args = sys.argv[1:]
    if "--csv" in args:
        idx = args.index("--csv")
        csv_path = args[idx + 1] if idx + 1 < len(args) else csv_path
    if "--alert-threshold" in args:
        idx = args.index("--alert-threshold")
        alert_threshold = float(args[idx + 1]) if idx + 1 < len(args) else alert_threshold
    
    monitor_products(csv_path, alert_threshold)

if __name__ == "__main__":
    main()
