"""Shared CSS styling for Celios 9 Danantara Dashboard."""

def get_danantara_css():
    """Return CSS styling for Danantara Monitor & Green Investment dashboard - matching Celios ECC style."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .org-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        color: #E8F5E9;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        border: 1px solid #4CAF50;
    }
    
    .main-title, .page-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #43A047, #66BB6A, #A5D6A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }
    
    .sub-title, .page-subtitle {
        font-size: 1.05rem;
        color: #B0BEC5;
        font-weight: 300;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: #1A1F2B;
        border: 1px solid #2E3B4E;
        border-radius: 8px;
        padding: 1.3rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #26A69A;
        margin: 0.4rem 0;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #B0BEC5;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    
    .metric-desc {
        font-size: 0.75rem;
        color: #9E9E9E;
        margin-top: 0.6rem;
        line-height: 1.4;
    }
    
    .bento-card {
        background: linear-gradient(135deg, #141A24, #1E2738);
        border: 1px solid #2E3B4E;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 175px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .bento-card:hover {
        border-color: #26A69A;
        transform: translateY(-2px);
    }
    .bento-val {
        font-size: 2.0rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 8px 0;
    }
    .bento-lbl {
        font-size: 0.78rem;
        color: #90A4AE;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .bento-desc {
        font-size: 0.78rem;
        color: #CFD8DC;
        line-height: 1.4;
        text-align: left;
        margin-top: 4px;
    }
    .bento-src {
        font-size: 0.68rem;
        color: #78909C;
        margin-top: 10px;
        padding-top: 6px;
        border-top: 1px dotted #37474F;
        text-align: left;
    }

    .note-box {
        background: #102027;
        border-left: 4px solid #26A69A;
        padding: 14px 18px;
        border-radius: 6px;
        color: #ECEFF1;
        margin: 12px 0 20px 0;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ECEFF1;
        margin: 1.8rem 0 0.8rem 0;
        border-bottom: 1px solid #2E3B4E;
        padding-bottom: 6px;
    }

    .badge-track-a {
        display: inline-block;
        background: rgba(38, 166, 154, 0.15);
        color: #26A69A;
        border: 1px solid rgba(38, 166, 154, 0.4);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .badge-track-b {
        display: inline-block;
        background: rgba(102, 187, 106, 0.15);
        color: #66BB6A;
        border: 1px solid rgba(102, 187, 106, 0.4);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .table-container {
        border: 1px solid #2E3B4E;
        border-radius: 8px;
        background: #141A24;
        padding: 10px;
    }
    </style>
    """
