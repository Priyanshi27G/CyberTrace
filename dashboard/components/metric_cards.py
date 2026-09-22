import streamlit as st

def render_metric_cards(packets_count: int, alert_count: int, unique_ips: int, protocols_count: int):
    """Custom HTML metric cards with icons and accent colors."""
    
    cards = [
        {
            "icon": "📦", "value": f"{packets_count:,}",
            "label": "Packets", "color": "#10B981"
        },
        {
            "icon": "⚠️", "value": str(alert_count),
            "label": "Active Threats", "color": "#EF4444" if alert_count > 0 else "#10B981"
        },
        {
            "icon": "🌐", "value": str(unique_ips),
            "label": "Unique IPs", "color": "#06B6D4"
        },
        {
            "icon": "📡", "value": str(protocols_count),
            "label": "Protocols", "color": "#F59E0B"
        }
    ]
    
    cols = st.columns(4)
    for i, card in enumerate(cards):
        with cols[i]:
            html = f"""
            <div class="ct-metric" style="border-top: 3px solid {card['color']};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="ct-metric-value">{card['value']}</div>
                        <div class="ct-metric-label">{card['label']}</div>
                    </div>
                    <div class="ct-metric-icon">{card['icon']}</div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
