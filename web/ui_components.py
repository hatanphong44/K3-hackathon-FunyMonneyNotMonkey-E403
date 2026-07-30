"""
UI Component Helpers and Modern CSS Styling for Streamlit App.
"""

import streamlit as st

def inject_custom_css():
    """Injects high-end modern CSS styles into Streamlit page."""
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Gradient Header Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 16px;
        padding: 2rem 2.2rem;
        color: #ffffff !important;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px -5px rgba(67, 56, 202, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #e0e7ff !important;
        font-weight: 400;
        max-width: 800px;
        line-height: 1.5;
    }

    /* Aggressive High-contrast Dark Text for both Streamlit Dark & Light Themes */
    .glass-card, .glass-card *, .glass-card h3, .glass-card h4, .glass-card p, .glass-card div, .glass-card span, .glass-card b, .glass-card i {
        color: #0f172a !important;
    }

    .glass-card {
        background: #ffffff !important;
        border-radius: 14px;
        padding: 1.4rem;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.2rem;
    }

    /* Metric Cards */
    .metric-box, .metric-box * {
        background: #ffffff !important;
    }
    
    .metric-box {
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #312e81 !important;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-primary { background: #e0e7ff !important; color: #3730a3 !important; }
    .badge-success { background: #dcfce7 !important; color: #166534 !important; }
    .badge-warning { background: #fef9c3 !important; color: #854d0e !important; }
    .badge-info { background: #e0f2fe !important; color: #075985 !important; }

    /* Custom Streamlit Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s ease;
    }

    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        border: none;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    div.stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #312e81 100%);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
    }

    .explanation-box, .explanation-box * {
        color: #1e40af !important;
    }
    .explanation-box {
        background: #eff6ff !important;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.95rem;
        margin-top: 0.8rem;
    }

    .hint-box, .hint-box * {
        color: #854d0e !important;
    }
    .hint-box {
        background: #fefce8 !important;
        border: 1px solid #fef08a;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Status indicator pill */
    .api-status {
        font-size: 0.85rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .api-status-online { background-color: #dcfce7 !important; color: #15803d !important; }
    .api-status-mock { background-color: #fef3c7 !important; color: #b45309 !important; }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header(api_online: bool = True):
    """Renders the main top header with responsive badge."""
    inject_custom_css()
    status_html = '<span class="api-status api-status-online">● FastAPI Online</span>' if api_online else '<span class="api-status api-status-mock">● Mode Streamlit Sandbox (FastAPI offline)</span>'
    
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; justify-space: space-between; align-items: center;">
            <div>
                <div class="hero-title">⚡ VLearn AI Quiz Generator</div>
                <div class="hero-subtitle">
                    Hệ thống AI tự động sinh câu hỏi kiểm tra kiến thức bài giảng cuối buổi cho Sinh viên và Giảng viên.
                </div>
            </div>
        </div>
        <div style="margin-top: 1.2rem;">
            {status_html}
            <span class="badge badge-primary">VLearn AI Tutor Spec</span>
            <span class="badge badge-info">Zero-Lag Synthesis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_box(label: str, value: str, subtext: str = "", color_theme: str = "indigo"):
    """Renders a formatted metric box."""
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div style="font-size: 0.8rem; color: #475569 !important; margin-top: 4px;">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)
