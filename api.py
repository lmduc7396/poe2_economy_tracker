"""
POE2 Economy Tracker - API Layer
Fetches data from poe2scout.com API
"""

import bisect
import math
from typing import Optional
from datetime import datetime

import requests
import streamlit as st

from config import (
    API_BASE_URL,
    FARMING_METHODS,
    GENERAL_CATEGORIES,
    MIN_VOLUME_THRESHOLD,
    MIN_CHAOS_VALUE,
    ITEM_FARMING_OVERRIDES,
    UNIQUE_ITEM_DROP_SOURCES,
    UNIQUE_CATEGORIES,
    MIN_DIVINE_VALUE,
    FRAGMENT_FARMING_SOURCES,
)


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_leagues() -> list[dict]:
    """Fetch available leagues from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/leagues", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch leagues: {e}")
        return []


@st.cache_data(ttl=1800)
def fetch_categories() -> dict:
    """Fetch all item categories from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/items/categories", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch categories: {e}")
        return {"currency_categories": [], "unique_categories": []}


@st.cache_data(ttl=1800)
def fetch_currency_rates(league: str) -> dict:
    """Fetch currency exchange rates (divine and exalted to chaos)"""
    rates = {"divine_to_chaos": 60.0, "exalted_to_chaos": 0.18}
    try:
        url = f"{API_BASE_URL}/items/currency/currency"
        params = {
            "page": 1,
            "perPage": 50,
            "league": league,
            "referenceCurrency": "chaos"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for item in data.get("items", []):
            name = item.get("text")
            if name == "Divine Orb":
                rates["divine_to_chaos"] = item.get("currentPrice", 0) or 60.0
            elif name == "Exalted Orb":
                rates["exalted_to_chaos"] = item.get("currentPrice", 0) or 0.18

        return rates
    except Exception as e:
        st.warning(f"Failed to fetch currency rates: {e}")
        return rates


def fetch_divine_to_chaos_rate(league: str) -> float:
    """Fetch the divine orb to chaos orb exchange rate"""
    return fetch_currency_rates(league)["divine_to_chaos"]


@st.cache_data(ttl=1800)
def fetch_items_for_category(
    category_type: str,  # "currency" or "unique"
    category_api_id: str,
    league: str,
    page: int = 1,
    per_page: int = 100
) -> dict:
    """Fetch items for a specific category"""
    try:
        if category_type == "currency":
            url = f"{API_BASE_URL}/items/currency/{category_api_id}"
        else:
            url = f"{API_BASE_URL}/items/unique/{category_api_id}"

        params = {
            "page": page,
            "perPage": per_page,
            "league": league,
            "referenceCurrency": "chaos"
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Failed to fetch {category_api_id}: {e}")
        return {"items": [], "total": 0, "pages": 0}


def calculate_price_change(price_logs: list[dict]) -> tuple[float, float]:
    """
    Calculate price change over available history.
    Returns (change_percent, oldest_price)
    """
    # Filter out None entries
    valid_logs = [log for log in price_logs if log is not None]

    if not valid_logs or len(valid_logs) < 2:
        return 0.0, 0.0

    current_price = valid_logs[0].get("price", 0) if valid_logs[0] else 0
    oldest_price = valid_logs[-1].get("price", 0) if valid_logs[-1] else 0

    if oldest_price == 0:
        return 0.0, 0.0

    change_pct = ((current_price - oldest_price) / oldest_price) * 100
    return change_pct, oldest_price


def normalize_volumes(items: list[dict]) -> list[dict]:
    """
    Normalize volume across all items to a 0-1 scale using percentile ranking.
    This prevents high-volume items from dominating the profit score.

    Items below MIN_VOLUME_THRESHOLD get normalized_volume = 0.
    Other items get a percentile rank (0.0 to 1.0) based on their volume.
    """
    # Get volumes for items meeting threshold
    valid_volumes = [
        item["quantity"] for item in items
        if item["quantity"] >= MIN_VOLUME_THRESHOLD
    ]

    if not valid_volumes:
        return items

    # Sort volumes to calculate percentiles
    sorted_volumes = sorted(valid_volumes)

    # Create a mapping from volume to percentile rank
    def get_percentile(volume: int) -> float:
        if volume < MIN_VOLUME_THRESHOLD:
            return 0.0
        # Find position in sorted list (use bisect for efficiency)
        position = bisect.bisect_left(sorted_volumes, volume)
        # Convert to 0-1 scale (add small offset to avoid 0)
        return (position + 1) / len(sorted_volumes)

    # Apply normalized volume and calculate profit score
    for item in items:
        normalized_vol = get_percentile(item["quantity"])
        item["normalized_volume"] = round(normalized_vol, 3)

        # Profit score = price_change_pct * normalized_volume
        # Scale by 100 to make scores more readable
        if item["quantity"] >= MIN_VOLUME_THRESHOLD:
            item["profit_score"] = round(item["price_change_pct"] * normalized_vol, 2)
        else:
            item["profit_score"] = 0.0

    return items


def process_item(
    item: dict,
    farming_method: Optional[str] = None,
    divine_to_chaos: float = 60.0
) -> dict:
    """Process a single item and calculate metrics. Prices are already in chaos."""
    price_logs = item.get("priceLogs", []) or []
    # Price is already in chaos (referenceCurrency=chaos)
    current_price_chaos = item.get("currentPrice", 0) or 0

    # Filter out None entries from price_logs
    valid_logs = [log for log in price_logs if log is not None]

    # Get latest quantity and data age
    quantity = 0
    data_age_hours = None
    if valid_logs and valid_logs[0]:
        quantity = valid_logs[0].get("quantity", 0) or 0
        # Calculate how old the quantity data is
        log_time = valid_logs[0].get("time")
        if log_time:
            try:
                log_dt = datetime.fromisoformat(log_time.replace("Z", "+00:00"))
                now = datetime.now(log_dt.tzinfo) if log_dt.tzinfo else datetime.now()
                data_age_hours = (now - log_dt).total_seconds() / 3600
            except (ValueError, TypeError):
                data_age_hours = None

    # Calculate price change
    price_change_pct, oldest_price = calculate_price_change(valid_logs)

    # Profit score will be calculated after volume normalization
    profit_score = 0.0

    # Extract price history for sparkline (already in chaos)
    price_history = [
        {"time": log.get("time"), "price": log.get("price", 0) or 0}
        for log in reversed(valid_logs)  # Oldest first for chart
        if log is not None
    ]

    # Get item name and apply farming method override if needed
    item_name = item.get("text", "Unknown")
    final_farming_method = ITEM_FARMING_OVERRIDES.get(item_name, farming_method)

    return {
        "id": item.get("id"),
        "name": item_name,
        "icon_url": item.get("iconUrl", ""),
        "current_price": current_price_chaos,
        "quantity": quantity,
        "data_age_hours": round(data_age_hours, 1) if data_age_hours else None,
        "price_change_pct": round(price_change_pct, 2),
        "profit_score": round(profit_score, 2),
        "price_history": price_history,
        "farming_method": final_farming_method,
        "category_api_id": item.get("categoryApiId", ""),
        "wiki_url": f"https://www.poe2wiki.net/wiki/{item_name.replace(' ', '_')}",
        "trade_url": f"https://www.pathofexile.com/trade2/search/poe2",
    }


def get_category_to_farming_method_map() -> dict:
    """Create a reverse mapping from category API ID to farming method"""
    category_map = {}
    for method_name, method_info in FARMING_METHODS.items():
        for category in method_info["categories"]:
            category_map[category] = method_name
    return category_map


@st.cache_data(ttl=60)  # Reduced to 1 min for testing - change back to 1800 later
def fetch_all_farming_items(league: str) -> list[dict]:
    """
    Fetch all items from farming-related categories.
    Returns processed items with farming method assignments.
    Prices are in chaos orbs (fetched directly), items < MIN_CHAOS_VALUE are filtered out.
    """
    all_items = []
    category_map = get_category_to_farming_method_map()

    # Fetch divine to chaos rate for filtering uniques
    divine_to_chaos = fetch_divine_to_chaos_rate(league)
    min_divine_chaos = MIN_DIVINE_VALUE * divine_to_chaos

    # Get all currency categories that map to farming methods
    farming_categories = set()
    for method_info in FARMING_METHODS.values():
        farming_categories.update(method_info["categories"])

    # Fetch items from each farming category
    for category_api_id in farming_categories:
        farming_method = category_map.get(category_api_id)

        # Fetch all pages for this category
        page = 1
        while True:
            # Determine if it's a currency or unique category
            if category_api_id in ["jewel"]:
                data = fetch_items_for_category("unique", category_api_id, league, page, 100)
            else:
                data = fetch_items_for_category("currency", category_api_id, league, page, 100)

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                processed = process_item(item, farming_method, divine_to_chaos)
                # Filter out items below minimum chaos value
                if processed["current_price"] >= MIN_CHAOS_VALUE:
                    all_items.append(processed)

            # Check if there are more pages
            if page >= data.get("pages", 1):
                break
            page += 1

    # Fetch fragments with their farming method mappings
    page = 1
    while True:
        data = fetch_items_for_category("currency", "fragments", league, page, 100)
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            item_name = item.get("text", "")
            # Get farming method from fragment mapping
            farming_method = FRAGMENT_FARMING_SOURCES.get(item_name, None)
            processed = process_item(item, farming_method, divine_to_chaos)
            if processed["current_price"] >= MIN_CHAOS_VALUE:
                all_items.append(processed)

        if page >= data.get("pages", 1):
            break
        page += 1

    # Fetch valuable unique items (> 1 divine)
    for category_api_id in UNIQUE_CATEGORIES:
        page = 1
        while True:
            data = fetch_items_for_category("unique", category_api_id, league, page, 100)
            items = data.get("items", [])
            if not items:
                break

            for item in items:
                item_name = item.get("text", "")
                # Check if this unique has a specific drop source
                farming_method = UNIQUE_ITEM_DROP_SOURCES.get(item_name, None)

                processed = process_item(item, farming_method, divine_to_chaos)

                # Only include uniques worth > 1 divine
                if processed["current_price"] >= min_divine_chaos:
                    processed["is_unique"] = True
                    all_items.append(processed)

            if page >= data.get("pages", 1):
                break
            page += 1

    # Normalize volumes and calculate profit scores
    all_items = normalize_volumes(all_items)

    return all_items, divine_to_chaos


def get_top_rising_items(items: list[dict], limit: int = 20) -> list[dict]:
    """Get top rising items by profit score"""
    # Filter items with positive profit score
    rising = [i for i in items if i["profit_score"] > 0]
    # Sort by profit score descending
    rising.sort(key=lambda x: x["profit_score"], reverse=True)
    return rising[:limit]


def get_items_by_farming_method(items: list[dict], method: str) -> list[dict]:
    """Filter items by farming method"""
    method_items = [i for i in items if i["farming_method"] == method]
    # Sort by profit score
    method_items.sort(key=lambda x: x["profit_score"], reverse=True)
    return method_items


def get_falling_items(items: list[dict], limit: int = 10) -> list[dict]:
    """Get items with biggest price drops (potential buy opportunities)"""
    falling = [i for i in items if i["price_change_pct"] < -10 and i["quantity"] >= MIN_VOLUME_THRESHOLD]
    falling.sort(key=lambda x: x["price_change_pct"])
    return falling[:limit]


def calculate_farming_method_profitability(items: list[dict]) -> list[dict]:
    """
    Calculate profitability ranking for each farming method.
    Uses sum of profit scores of ALL items in each method.

    Returns list of dicts sorted by profitability score descending:
    {
        "method": str,
        "profitability_score": float,  # Sum of profit scores of all items
        "rising_items": int,  # Count of items with positive change
        "total_items": int,
        "avg_change_pct": float,
        "total_volume": int,
        "top_item": dict,  # Best item in this method
    }
    """
    method_stats = {}

    # Group items by farming method
    for item in items:
        method = item["farming_method"]
        if not method:
            continue

        if method not in method_stats:
            method_stats[method] = {
                "items": [],
                "rising_count": 0,
                "total_change": 0,
                "total_volume": 0,
                "total_profit_score": 0,
            }

        method_stats[method]["items"].append(item)
        if item["price_change_pct"] > 0:
            method_stats[method]["rising_count"] += 1
        method_stats[method]["total_change"] += item["price_change_pct"]
        method_stats[method]["total_volume"] += item["quantity"]
        method_stats[method]["total_profit_score"] += item["profit_score"]

    # Calculate profitability for each method
    results = []
    for method, stats in method_stats.items():
        items_list = stats["items"]
        total_items = len(items_list)

        if total_items == 0:
            continue

        # Sort by profit score to find top item
        items_list.sort(key=lambda x: x["profit_score"], reverse=True)

        # Sum of all profit scores in this method
        total_profit_score = stats["total_profit_score"]

        # Get best item (list is sorted by profit_score descending)
        top_item = items_list[0] if items_list else None

        results.append({
            "method": method,
            "profitability_score": round(total_profit_score, 2),
            "rising_items": stats["rising_count"],
            "total_items": total_items,
            "avg_change_pct": round(stats["total_change"] / total_items, 2),
            "total_volume": stats["total_volume"],
            "top_item": top_item,
            "color": FARMING_METHODS.get(method, {}).get("color", "#808080"),
            "icon": FARMING_METHODS.get(method, {}).get("icon", ""),
        })

    # Sort by profitability score descending
    results.sort(key=lambda x: x["profitability_score"], reverse=True)

    return results
