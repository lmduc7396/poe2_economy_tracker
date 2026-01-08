"""
POE2 Economy Tracker - Main Streamlit App
Track POE2 economy by farming method and identify profitable opportunities
"""

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from config import FARMING_METHODS, DEFAULT_LEAGUE
from api import (
    fetch_leagues,
    fetch_all_farming_items,
    fetch_currency_rates,
    get_top_rising_items,
    get_items_by_farming_method,
    get_falling_items,
    calculate_farming_method_profitability,
)

# Page config
st.set_page_config(
    page_title="POE2 Economy Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark theme
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Item card */
    .item-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #252550 100%);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #3a3a5c;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .item-card:hover {
        border-color: #5a5a8c;
    }

    .item-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        background: #0a0a1a;
        padding: 4px;
    }

    .item-name {
        font-size: 15px;
        font-weight: 600;
        color: #fff;
        margin: 0;
    }

    .positive { color: #4ade80 !important; }
    .negative { color: #f87171 !important; }

    .stat-value {
        font-size: 18px;
        font-weight: 600;
    }

    .farming-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
        margin-left: 8px;
    }

    .overview-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #252550 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #3a3a5c;
        text-align: center;
    }

    .overview-label {
        font-size: 12px;
        color: #8b8ba7;
        text-transform: uppercase;
    }

    .overview-value {
        font-size: 28px;
        font-weight: 700;
        color: #fff;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* GLOBAL: Force text to be light (except inputs) */
    .stApp p, .stApp span, .stApp label, .stApp div:not([data-baseweb]) {
        color: #e8e8e8 !important;
    }

    /* Headers gold/yellow */
    h1, h2, h3, .stApp h1, .stApp h2, .stApp h3 {
        color: #fbbf24 !important;
    }

    /* Green for positive changes */
    [data-testid="stMetricDelta"][data-testid-direction="up"],
    [data-testid="stMetricDelta"][data-testid-direction="up"] * {
        color: #4ade80 !important;
    }

    /* Red for negative changes */
    [data-testid="stMetricDelta"][data-testid-direction="down"],
    [data-testid="stMetricDelta"][data-testid-direction="down"] * {
        color: #f87171 !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #e8e8e8 !important;
    }

    /* Keep button/tag colors */
    .stMultiSelect span[data-baseweb="tag"] {
        color: white !important;
    }

    /* Dark input backgrounds */
    [data-baseweb="select"], [data-baseweb="input"] {
        background-color: #1e1e3f !important;
    }
    [data-baseweb="select"] div, [data-baseweb="popover"] {
        background-color: #1e1e3f !important;
        color: #e8e8e8 !important;
    }
</style>
""", unsafe_allow_html=True)


def create_sparkline(price_history: list[dict], color: str = "#4ade80") -> go.Figure:
    """Create a mini sparkline chart for price history"""
    if not price_history:
        return None

    prices = [p["price"] for p in price_history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=prices,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor='rgba(74, 222, 128, 0.1)' if color == "#4ade80" else 'rgba(248, 113, 113, 0.1)',
        hoverinfo='skip'
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=50,
        width=120,
    )

    return fig


def render_item(item: dict, show_method: bool = True, key_prefix: str = ""):
    """Render a single item using Streamlit columns"""
    col1, col2, col3, col4, col5, col6 = st.columns([0.5, 3, 1.5, 1, 1, 1.5])

    item_key = f"{key_prefix}_{item['id']}_{item['name'][:10]}"

    with col1:
        st.image(item["icon_url"], width=40)

    with col2:
        st.markdown(f"**{item['name']}**")
        if show_method and item["farming_method"]:
            st.caption(f"🎯 {item['farming_method']}")

    with col3:
        # Display price in chaos (with exalted equivalent for high values)
        chaos_price = item['current_price']
        if chaos_price >= 100:
            st.metric("Price", f"{chaos_price:,.0f} c")
        else:
            st.metric("Price", f"{chaos_price:.1f} c")

    with col4:
        change_delta = f"{item['price_change_pct']:+.1f}%"
        st.metric("7d Change", change_delta, delta=change_delta)

    with col5:
        # Show volume with data age indicator if stale (>6 hours old)
        data_age = item.get("data_age_hours")
        if data_age and data_age > 6:
            st.metric("Volume", f"{item['quantity']:,}")
            st.caption(f"⏱️ {data_age:.0f}h ago")
        else:
            st.metric("Volume", f"{item['quantity']:,}")

    with col6:
        if item["price_history"]:
            color = "#4ade80" if item["price_change_pct"] > 0 else "#f87171"
            fig = create_sparkline(item["price_history"], color)
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"chart_{item_key}")


def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        # Fetch leagues
        leagues = fetch_leagues()
        league_names = [l["value"] for l in leagues] if leagues else [DEFAULT_LEAGUE]

        # League selector
        selected_league = st.selectbox(
            "League",
            options=league_names,
            index=league_names.index(DEFAULT_LEAGUE) if DEFAULT_LEAGUE in league_names else 0
        )

        st.markdown("---")

        # Farming method filter
        st.markdown("### 🎯 Farming Methods")
        farming_methods = list(FARMING_METHODS.keys())

        selected_methods = st.multiselect(
            "Filter by method",
            options=farming_methods,
            default=farming_methods,
            help="Select which farming methods to display"
        )

        st.markdown("---")

        # Filters
        st.markdown("### 📊 Filters")

        min_volume = st.slider(
            "Minimum Volume",
            min_value=1,
            max_value=100,
            value=5,
            help="Filter out items with low market volume"
        )

        min_profit_score = st.slider(
            "Minimum Profit Score",
            min_value=0,
            max_value=100,
            value=0,
            help="Filter by minimum profit score"
        )

        sort_by = st.selectbox(
            "Sort By",
            options=["Profit Score", "Price Change %", "Volume", "Price"],
            index=0
        )

        st.markdown("---")

        # Info
        st.markdown("""
        ### ℹ️ About

        **Profit Score** = change% × normalized_volume

        Higher score = better opportunity

        **Volume** = # of listings (not trade volume)

        ⏱️ = volume data >6h old

        ---

        Data from [poe2scout.com](https://poe2scout.com)
        """)

    # Main content
    st.title("💰 POE2 Economy Tracker")

    # Fetch all items
    with st.spinner("Loading economy data..."):
        all_items, divine_to_chaos = fetch_all_farming_items(selected_league)

    st.caption(f"League: **{selected_league}** • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} • Data from poe2scout.com")

    # Apply filters
    filtered_items = [
        item for item in all_items
        if item["quantity"] >= min_volume
        and item["profit_score"] >= min_profit_score
        and (not selected_methods or item["farming_method"] in selected_methods)
    ]

    # Sort items
    sort_key_map = {
        "Profit Score": lambda x: x["profit_score"],
        "Price Change %": lambda x: x["price_change_pct"],
        "Volume": lambda x: x["quantity"],
        "Price": lambda x: x["current_price"],
    }
    filtered_items.sort(key=sort_key_map[sort_by], reverse=True)

    # Calculate stats
    total_items = len(filtered_items)
    rising_count = len([i for i in filtered_items if i["price_change_pct"] > 0])
    avg_change = sum(i["price_change_pct"] for i in filtered_items) / max(total_items, 1)

    # Fetch currency rates
    currency_rates = fetch_currency_rates(selected_league)

    # Currency icons
    DIVINE_ICON = "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lNb2RWYWx1ZXMiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/2986e220b3/CurrencyModValues.png"
    EXALTED_ICON = "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lBZGRNb2RUb1JhcmUiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/ad7c366789/CurrencyAddModToRare.png"
    CHAOS_ICON = "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lSZXJvbGxSYXJlIiwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/c0ca392a78/CurrencyRerollRare.png"

    # Stats overview with exchange rates
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <img src="{DIVINE_ICON}" width="28">
            <span style="font-size: 14px;"><b>1 Divine</b> = {currency_rates['divine_to_chaos']:.1f} c</span>
            <img src="{CHAOS_ICON}" width="20">
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <img src="{EXALTED_ICON}" width="28">
            <span style="font-size: 14px;"><b>1 Exalted</b> = {currency_rates['exalted_to_chaos']:.2f} c</span>
            <img src="{CHAOS_ICON}" width="20">
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.metric("Rising Items", f"{rising_count:,}", delta=f"{rising_count}")
    with col4:
        st.metric("Avg Change (7d)", f"{avg_change:+.1f}%", delta=f"{avg_change:+.1f}%")

    st.markdown("---")

    # Farming Method Profitability Ranking
    st.subheader("🏆 Most Profitable Farming Methods")
    st.caption("Ranked by average profit score of all items per method")

    method_rankings = calculate_farming_method_profitability(filtered_items)

    if method_rankings:
        # Create columns for the ranking cards
        cols = st.columns(len(method_rankings))

        for i, (col, ranking) in enumerate(zip(cols, method_rankings)):
            with col:
                # Rank badge
                rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"

                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #1e1e3f 0%, #252550 100%);
                            border-radius: 12px; padding: 16px; border: 1px solid #3a3a5c;
                            text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 24px; color: #fff;">{rank_emoji}</div>
                    <div style="font-size: 16px; font-weight: 600; color: {ranking['color']};">{ranking['method']}</div>
                    <div style="font-size: 24px; font-weight: 700; color: #4ade80;">+{ranking['profitability_score']:.0f}</div>
                    <div style="font-size: 11px; color: #b8b8d0;">Profit Score</div>
                </div>
                """, unsafe_allow_html=True)

                # Stats below the card
                st.caption(f"📈 {ranking['rising_items']}/{ranking['total_items']} rising")
                st.caption(f"Avg: {ranking['avg_change_pct']:+.1f}%")

                if ranking['top_item']:
                    st.caption(f"Best: {ranking['top_item']['name'][:20]}...")

    st.markdown("---")

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔥 Top Rising", "📂 By Farming Method", "📉 Falling Prices"])

    with tab1:
        st.subheader("🔥 Top Rising Items")
        st.caption("Items with highest profit score (price increase × volume)")

        top_rising = get_top_rising_items(filtered_items, limit=20)

        if top_rising:
            for i, item in enumerate(top_rising):
                with st.container():
                    render_item(item, show_method=True, key_prefix=f"rising_{i}")
                    st.markdown("---")
        else:
            st.info("No rising items found with current filters")

    with tab2:
        st.subheader("📂 Items by Farming Method")

        # Farming method selector
        if selected_methods:
            current_method = st.selectbox(
                "Select Farming Method",
                options=selected_methods,
                key="method_selector"
            )

            if current_method:
                method_info = FARMING_METHODS.get(current_method, {})

                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    st.image(method_info.get("icon", ""), width=50)
                with col2:
                    st.markdown(f"### {current_method}")
                    st.caption(method_info.get("description", ""))

                method_items = get_items_by_farming_method(filtered_items, current_method)

                if method_items:
                    for i, item in enumerate(method_items[:20]):
                        with st.container():
                            render_item(item, show_method=False, key_prefix=f"method_{i}")
                            st.markdown("---")
                else:
                    st.info(f"No items found for {current_method}")
        else:
            st.warning("Select at least one farming method from the sidebar")

    with tab3:
        st.subheader("📉 Falling Prices")
        st.caption("Items with significant price drops - potential buying opportunities")

        falling_items = get_falling_items(filtered_items, limit=15)

        if falling_items:
            st.warning("⚠️ Items with >10% price drop. Could be buying opportunities or declining demand.")

            for i, item in enumerate(falling_items):
                with st.container():
                    render_item(item, show_method=True, key_prefix=f"falling_{i}")
                    st.markdown("---")
        else:
            st.info("No significantly falling items found")

    # Footer
    st.markdown("---")
    st.caption("POE2 Economy Tracker • Data from [poe2scout.com](https://poe2scout.com) • Not affiliated with Grinding Gear Games")


if __name__ == "__main__":
    main()
