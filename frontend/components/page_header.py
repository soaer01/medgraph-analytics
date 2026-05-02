import streamlit as st

# ═══════════════════════════════════════════════════════════════════
# Custom SVG Icons for each page — neon-styled biomedical symbols
# ═══════════════════════════════════════════════════════════════════

_SVG_ABOUT = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 4C20 12 16 16 16 24C16 32 20 36 24 44" stroke="#00f0ff" stroke-width="2" stroke-linecap="round"/>
  <path d="M24 4C28 12 32 16 32 24C32 32 28 36 24 44" stroke="#ff00e5" stroke-width="2" stroke-linecap="round"/>
  <circle cx="20" cy="14" r="2" fill="#00f0ff"/>
  <circle cx="28" cy="14" r="2" fill="#ff00e5"/>
  <circle cx="20" cy="24" r="2" fill="#ff00e5"/>
  <circle cx="28" cy="24" r="2" fill="#00f0ff"/>
  <circle cx="20" cy="34" r="2" fill="#00f0ff"/>
  <circle cx="28" cy="34" r="2" fill="#ff00e5"/>
  <line x1="20" y1="14" x2="28" y2="14" stroke="#39ff14" stroke-width="1.5" opacity="0.6"/>
  <line x1="28" y1="24" x2="20" y2="24" stroke="#39ff14" stroke-width="1.5" opacity="0.6"/>
  <line x1="20" y1="34" x2="28" y2="34" stroke="#39ff14" stroke-width="1.5" opacity="0.6"/>
</svg>'''

_SVG_DASHBOARD = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="28" width="8" height="14" rx="2" fill="#00f0ff" opacity="0.8"/>
  <rect x="18" y="18" width="8" height="24" rx="2" fill="#ff00e5" opacity="0.8"/>
  <rect x="30" y="8" width="8" height="34" rx="2" fill="#39ff14" opacity="0.8"/>
  <path d="M8 24L22 14L34 6" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 3"/>
  <circle cx="8" cy="24" r="3" fill="#00f0ff" stroke="#0a0c14" stroke-width="1"/>
  <circle cx="22" cy="14" r="3" fill="#ff00e5" stroke="#0a0c14" stroke-width="1"/>
  <circle cx="34" cy="6" r="3" fill="#39ff14" stroke="#0a0c14" stroke-width="1"/>
</svg>'''

_SVG_GRAPH = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="5" fill="#00f0ff" opacity="0.9"/>
  <circle cx="10" cy="12" r="3.5" fill="#ff00e5" opacity="0.8"/>
  <circle cx="38" cy="12" r="3.5" fill="#39ff14" opacity="0.8"/>
  <circle cx="10" cy="36" r="3.5" fill="#d500f9" opacity="0.8"/>
  <circle cx="38" cy="36" r="3.5" fill="#ffea00" opacity="0.8"/>
  <line x1="24" y1="24" x2="10" y2="12" stroke="#00f0ff" stroke-width="1.5" opacity="0.5"/>
  <line x1="24" y1="24" x2="38" y2="12" stroke="#00f0ff" stroke-width="1.5" opacity="0.5"/>
  <line x1="24" y1="24" x2="10" y2="36" stroke="#00f0ff" stroke-width="1.5" opacity="0.5"/>
  <line x1="24" y1="24" x2="38" y2="36" stroke="#00f0ff" stroke-width="1.5" opacity="0.5"/>
  <line x1="10" y1="12" x2="38" y2="12" stroke="#ff00e5" stroke-width="1" opacity="0.3"/>
  <line x1="10" y1="36" x2="38" y2="36" stroke="#d500f9" stroke-width="1" opacity="0.3"/>
</svg>'''

_SVG_ML = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="24" cy="24" rx="18" ry="18" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>
  <path d="M24 6C18 14 18 20 24 24C30 28 30 34 24 42" stroke="#00f0ff" stroke-width="2" opacity="0.6"/>
  <path d="M24 6C30 14 30 20 24 24C18 28 18 34 24 42" stroke="#ff00e5" stroke-width="2" opacity="0.6"/>
  <circle cx="24" cy="24" r="4" fill="#39ff14" opacity="0.9"/>
  <circle cx="16" cy="16" r="2" fill="#00f0ff"/>
  <circle cx="32" cy="16" r="2" fill="#ff00e5"/>
  <circle cx="16" cy="32" r="2" fill="#ff00e5"/>
  <circle cx="32" cy="32" r="2" fill="#00f0ff"/>
  <line x1="16" y1="16" x2="24" y2="24" stroke="#39ff14" stroke-width="1" opacity="0.5"/>
  <line x1="32" y1="16" x2="24" y2="24" stroke="#39ff14" stroke-width="1" opacity="0.5"/>
  <line x1="16" y1="32" x2="24" y2="24" stroke="#39ff14" stroke-width="1" opacity="0.5"/>
  <line x1="32" y1="32" x2="24" y2="24" stroke="#39ff14" stroke-width="1" opacity="0.5"/>
</svg>'''

_SVG_DRUG = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="10" width="20" height="28" rx="10" stroke="#00f0ff" stroke-width="2" fill="none"/>
  <line x1="14" y1="24" x2="34" y2="24" stroke="#ff00e5" stroke-width="1.5"/>
  <circle cx="24" cy="17" r="2.5" fill="#00f0ff" opacity="0.7"/>
  <circle cx="20" cy="31" r="1.5" fill="#39ff14" opacity="0.6"/>
  <circle cx="28" cy="31" r="1.5" fill="#39ff14" opacity="0.6"/>
  <line x1="20" y1="31" x2="28" y2="31" stroke="#39ff14" stroke-width="1" opacity="0.4"/>
  <circle cx="8" cy="18" r="2" fill="#d500f9" opacity="0.5"/>
  <line x1="8" y1="18" x2="14" y2="20" stroke="#d500f9" stroke-width="1" opacity="0.4"/>
  <circle cx="40" cy="30" r="2" fill="#ffea00" opacity="0.5"/>
  <line x1="40" y1="30" x2="34" y2="28" stroke="#ffea00" stroke-width="1" opacity="0.4"/>
</svg>'''

_SVG_NETWORK = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="16" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>
  <circle cx="24" cy="24" r="10" stroke="#ff00e5" stroke-width="1" opacity="0.2"/>
  <ellipse cx="24" cy="24" rx="16" ry="8" stroke="#00f0ff" stroke-width="1" opacity="0.3" transform="rotate(60 24 24)"/>
  <ellipse cx="24" cy="24" rx="16" ry="8" stroke="#ff00e5" stroke-width="1" opacity="0.3" transform="rotate(-60 24 24)"/>
  <circle cx="24" cy="8" r="3" fill="#00f0ff" opacity="0.9"/>
  <circle cx="24" cy="40" r="3" fill="#39ff14" opacity="0.9"/>
  <circle cx="10" cy="16" r="2.5" fill="#ff00e5" opacity="0.8"/>
  <circle cx="38" cy="16" r="2.5" fill="#d500f9" opacity="0.8"/>
  <circle cx="10" cy="32" r="2.5" fill="#ffea00" opacity="0.8"/>
  <circle cx="38" cy="32" r="2.5" fill="#ff00e5" opacity="0.8"/>
  <circle cx="24" cy="24" r="3.5" fill="#00f0ff" opacity="0.9"/>
</svg>'''

_SVG_TERMINOLOGY = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="22" height="36" rx="2" stroke="#00f0ff" stroke-width="1.5" fill="none"/>
  <rect x="18" y="10" width="22" height="36" rx="2" stroke="#ff00e5" stroke-width="1.5" fill="none" opacity="0.5"/>
  <line x1="13" y1="16" x2="25" y2="16" stroke="#39ff14" stroke-width="1.5" opacity="0.6"/>
  <line x1="13" y1="22" x2="25" y2="22" stroke="#00f0ff" stroke-width="1" opacity="0.4"/>
  <line x1="13" y1="26" x2="22" y2="26" stroke="#00f0ff" stroke-width="1" opacity="0.4"/>
  <line x1="13" y1="30" x2="25" y2="30" stroke="#00f0ff" stroke-width="1" opacity="0.4"/>
  <line x1="13" y1="34" x2="20" y2="34" stroke="#00f0ff" stroke-width="1" opacity="0.4"/>
  <circle cx="36" cy="14" r="4" stroke="#d500f9" stroke-width="1.5" fill="none"/>
  <line x1="39" y1="17" x2="42" y2="20" stroke="#d500f9" stroke-width="1.5"/>
</svg>'''

# Map page names to SVG icons
PAGE_ICONS = {
    'about': _SVG_ABOUT,
    'dashboard': _SVG_DASHBOARD,
    'graph_analytics': _SVG_GRAPH,
    'ml_predictions': _SVG_ML,
    'drug_explorer': _SVG_DRUG,
    'network_viewer': _SVG_NETWORK,
    'terminology': _SVG_TERMINOLOGY,
}


def render_page_header(title: str, page_key: str, subtitle: str = ""):
    """Render a neon-styled page header with a custom SVG icon.
    
    Args:
        title: The page title text.
        page_key: Key into PAGE_ICONS dict (e.g. 'dashboard').
        subtitle: Optional subtitle text.
    """
    icon_svg = PAGE_ICONS.get(page_key, _SVG_ABOUT)
    subtitle_html = f'<p class="neon-subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="neon-page-header">
        <div class="neon-icon">{icon_svg}</div>
        <div>
            <h1 class="neon-title">{title}</h1>
            {subtitle_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
