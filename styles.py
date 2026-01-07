"""
POE2 Economy Tracker - HTML/CSS Styles
Custom visual components for the dashboard
"""

from config import FARMING_METHODS

# Main CSS styles
MAIN_CSS = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global styles */
    .poe2-tracker * {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Header styles */
    .dashboard-header {
        background: linear-gradient(90deg, #0f0f23 0%, #1a1a3e 100%);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #2a2a4a;
    }

    .dashboard-title {
        font-size: 28px;
        font-weight: 700;
        color: #fff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .dashboard-subtitle {
        color: #8b8ba7;
        font-size: 14px;
        margin-top: 8px;
    }

    /* Card styles */
    .item-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #252550 100%);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #3a3a5c;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .item-card:hover {
        border-color: #5a5a8c;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    .item-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        background: #0a0a1a;
        padding: 4px;
        flex-shrink: 0;
    }

    .item-icon img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .item-info {
        flex-grow: 1;
        min-width: 0;
    }

    .item-name {
        font-size: 15px;
        font-weight: 600;
        color: #fff;
        margin: 0 0 4px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .item-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 12px;
        color: #8b8ba7;
    }

    .item-stats {
        display: flex;
        align-items: center;
        gap: 20px;
        flex-shrink: 0;
    }

    .stat-box {
        text-align: right;
    }

    .stat-label {
        font-size: 11px;
        color: #6b6b8a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stat-value {
        font-size: 16px;
        font-weight: 600;
        color: #fff;
    }

    .stat-value.positive {
        color: #4ade80;
    }

    .stat-value.negative {
        color: #f87171;
    }

    /* Price display */
    .price-display {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .price-display img {
        width: 18px;
        height: 18px;
    }

    /* Farming method badge */
    .farming-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
        background: rgba(255,255,255,0.1);
    }

    .farming-badge img {
        width: 16px;
        height: 16px;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 32px 0 16px 0;
    }

    .section-icon {
        font-size: 24px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #fff;
        margin: 0;
    }

    .section-count {
        background: rgba(255,255,255,0.1);
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        color: #8b8ba7;
    }

    /* Sparkline container */
    .sparkline-container {
        width: 100px;
        height: 40px;
        flex-shrink: 0;
    }

    /* Tab styles */
    .farming-tabs {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }

    .farming-tab {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        border-radius: 8px;
        background: #1e1e3f;
        border: 1px solid #3a3a5c;
        color: #8b8ba7;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .farming-tab:hover {
        border-color: #5a5a8c;
        color: #fff;
    }

    .farming-tab.active {
        background: #2a2a5f;
        border-color: #5a5a8c;
        color: #fff;
    }

    .farming-tab img {
        width: 20px;
        height: 20px;
    }

    /* Stats overview */
    .stats-overview {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .overview-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #252550 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #3a3a5c;
    }

    .overview-label {
        font-size: 12px;
        color: #8b8ba7;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .overview-value {
        font-size: 28px;
        font-weight: 700;
        color: #fff;
    }

    .overview-value.positive {
        color: #4ade80;
    }

    /* Profit score pill */
    .profit-score {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .profit-score.high {
        background: rgba(74, 222, 128, 0.2);
        color: #4ade80;
    }

    .profit-score.medium {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }

    .profit-score.low {
        background: rgba(139, 139, 167, 0.2);
        color: #8b8ba7;
    }

    /* Links */
    .item-links {
        display: flex;
        gap: 8px;
    }

    .item-link {
        font-size: 11px;
        color: #6b8afd;
        text-decoration: none;
        padding: 4px 8px;
        border-radius: 4px;
        background: rgba(107, 138, 253, 0.1);
        transition: all 0.2s ease;
    }

    .item-link:hover {
        background: rgba(107, 138, 253, 0.2);
        color: #8ba5fd;
    }

    /* Loading state */
    .loading-shimmer {
        background: linear-gradient(90deg, #1e1e3f 25%, #2a2a5f 50%, #1e1e3f 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
        height: 60px;
        margin-bottom: 12px;
    }

    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 48px;
        color: #6b6b8a;
    }

    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .item-card {
            flex-direction: column;
            align-items: flex-start;
        }

        .item-stats {
            width: 100%;
            justify-content: space-between;
            margin-top: 12px;
        }

        .sparkline-container {
            display: none;
        }
    }
</style>
"""

# Exalted orb icon for price display
EXALTED_ICON = "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lBZGRNb2RUb1JhcmUiLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/ad7c366789/CurrencyAddModToRare.png"


def render_header(league: str, last_updated: str) -> str:
    """Render the dashboard header"""
    return f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">
            <span>POE2 Economy Tracker</span>
        </h1>
        <p class="dashboard-subtitle">
            League: <strong>{league}</strong> &bull; Last updated: {last_updated} &bull; Data from poe2scout.com
        </p>
    </div>
    """


def render_stats_overview(total_items: int, rising_count: int, avg_change: float) -> str:
    """Render the stats overview cards"""
    change_class = "positive" if avg_change > 0 else ""
    change_sign = "+" if avg_change > 0 else ""

    return f"""
    <div class="stats-overview">
        <div class="overview-card">
            <div class="overview-label">Total Items Tracked</div>
            <div class="overview-value">{total_items:,}</div>
        </div>
        <div class="overview-card">
            <div class="overview-label">Rising Items</div>
            <div class="overview-value positive">{rising_count:,}</div>
        </div>
        <div class="overview-card">
            <div class="overview-label">Avg Price Change (7d)</div>
            <div class="overview-value {change_class}">{change_sign}{avg_change:.1f}%</div>
        </div>
    </div>
    """


def render_section_header(icon: str, title: str, count: int = None) -> str:
    """Render a section header"""
    count_html = f'<span class="section-count">{count} items</span>' if count else ""
    return f"""
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <h2 class="section-title">{title}</h2>
        {count_html}
    </div>
    """


def get_profit_score_class(score: float) -> str:
    """Get CSS class based on profit score"""
    if score >= 50:
        return "high"
    elif score >= 20:
        return "medium"
    return "low"


def render_item_card(item: dict, show_farming_method: bool = True) -> str:
    """Render a single item card"""
    # Determine change class
    change_class = "positive" if item["price_change_pct"] > 0 else "negative" if item["price_change_pct"] < 0 else ""
    change_sign = "+" if item["price_change_pct"] > 0 else ""

    # Farming badge
    farming_badge = ""
    if show_farming_method and item["farming_method"]:
        method_info = FARMING_METHODS.get(item["farming_method"], {})
        method_color = method_info.get("color", "#8b8ba7")
        method_icon = method_info.get("icon", "")
        farming_badge = f"""
        <span class="farming-badge" style="border: 1px solid {method_color}; color: {method_color};">
            <img src="{method_icon}" alt="">
            {item["farming_method"]}
        </span>
        """

    # Profit score
    score_class = get_profit_score_class(item["profit_score"])
    profit_badge = f"""
    <span class="profit-score {score_class}">
        Score: {item["profit_score"]:.0f}
    </span>
    """ if item["profit_score"] > 0 else ""

    return f"""
    <div class="item-card">
        <div class="item-icon">
            <img src="{item['icon_url']}" alt="{item['name']}" loading="lazy">
        </div>
        <div class="item-info">
            <h3 class="item-name">{item['name']}</h3>
            <div class="item-meta">
                {farming_badge}
                {profit_badge}
                <span class="item-links">
                    <a href="{item['wiki_url']}" target="_blank" class="item-link">Wiki</a>
                </span>
            </div>
        </div>
        <div class="item-stats">
            <div class="stat-box">
                <div class="stat-label">Price</div>
                <div class="stat-value price-display">
                    {item['current_price']:.1f}
                    <img src="{EXALTED_ICON}" alt="ex">
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Change</div>
                <div class="stat-value {change_class}">{change_sign}{item['price_change_pct']:.1f}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Volume</div>
                <div class="stat-value">{item['quantity']:,}</div>
            </div>
        </div>
    </div>
    """


def render_item_list(items: list[dict], show_farming_method: bool = True) -> str:
    """Render a list of item cards"""
    if not items:
        return """
        <div class="empty-state">
            <div class="empty-state-icon">📦</div>
            <p>No items found matching your criteria</p>
        </div>
        """

    cards_html = "\n".join([
        render_item_card(item, show_farming_method)
        for item in items
    ])

    return f'<div class="item-list">{cards_html}</div>'


def render_farming_tabs(methods: list[str], selected: str) -> str:
    """Render farming method tabs"""
    tabs_html = ""
    for method in methods:
        method_info = FARMING_METHODS.get(method, {})
        icon = method_info.get("icon", "")
        active_class = "active" if method == selected else ""
        tabs_html += f"""
        <div class="farming-tab {active_class}" data-method="{method}">
            <img src="{icon}" alt="">
            <span>{method}</span>
        </div>
        """

    return f'<div class="farming-tabs">{tabs_html}</div>'


def render_loading() -> str:
    """Render loading state"""
    return """
    <div class="loading-state">
        <div class="loading-shimmer"></div>
        <div class="loading-shimmer"></div>
        <div class="loading-shimmer"></div>
    </div>
    """
