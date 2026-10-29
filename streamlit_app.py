"""
🔐 Visual Cryptography Suite • Next-Gen Studio
A high-performance, dark-themed Visual Secret Sharing web application.
Features top-bar navigation (no intrusive sidebar), obsidian glassmorphism,
real-time XOR cryptographic engine, and instant lossless share reconstruction.
"""

import os
import io
import uuid
import sqlite3
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
import pandas as pd
import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------------------------------------------------------
# 1. PAGE SETUP & TOP-LEVEL CONFIG
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Visual Cryptography Suite • Studio",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------------------------
# 2. PATHS SETUP
# ------------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_FOLDER = os.path.join(STATIC_DIR, "uploads")
SHARES_FOLDER = os.path.join(STATIC_DIR, "shares")
DB_PATH = os.path.join(BASE_DIR, "users.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SHARES_FOLDER, exist_ok=True)

# ------------------------------------------------------------------------------
# 3. OBSIDIAN CYBER UI / UX THEME (CSS)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Colors */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9;
    }

    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Background Glow */
    .stApp {
        background-color: #080c14;
        background-image:
            radial-gradient(at 10% 15%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
            radial-gradient(at 90% 20%, rgba(6, 182, 212, 0.10) 0px, transparent 40%),
            radial-gradient(at 50% 80%, rgba(236, 72, 153, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
    }

    /* Hide default sidebar toggle if desired, or style it cleanly */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Brand Header Bar */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-icon {
        font-size: 1.9rem;
        filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.6));
    }
    .brand-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }
    .brand-tagline {
        font-size: 0.8rem;
        color: #94a3b8;
        margin: 0;
        letter-spacing: 0.02em;
    }
    .user-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #e2e8f0;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    /* Cyber Glass Cards */
    .cyber-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.2rem;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .cyber-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }

    /* Top Navigation Tabs Styling */
    div[data-testid="stHorizontalBlock"] button[role="tab"] {
        font-weight: 600;
        font-size: 0.95rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 10px;
        padding: 0 18px;
        background-color: transparent;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }

    /* Share Presentation Tags */
    .tag-original {
        display: inline-block;
        background: rgba(51, 65, 85, 0.5);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
    }
    .tag-share1 {
        display: inline-block;
        background: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.15);
    }
    .tag-share2 {
        display: inline-block;
        background: rgba(236, 72, 153, 0.15);
        color: #f472b6;
        border: 1px solid rgba(244, 114, 182, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
        box-shadow: 0 0 12px rgba(236, 72, 153, 0.15);
    }

    /* Step Workflow Bar */
    .step-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .step-box {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        text-align: center;
    }
    .step-box.active {
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(99, 102, 241, 0.08);
    }
    .step-badge {
        font-size: 0.75rem;
        font-weight: 700;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .step-desc {
        font-size: 0.85rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-top: 2px;
    }

    /* Alert Banners */
    .glow-banner-success {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(6, 95, 70, 0.2) 100%);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        color: #a7f3d0;
        margin: 1.2rem 0;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.1);
    }
    .glow-banner-info {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(30, 64, 175, 0.2) 100%);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        color: #bae6fd;
        margin: 1.2rem 0;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #f8fafc !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(51, 65, 85, 0.9) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
    }

    /* Metric Containers */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 4. DATABASE INTEGRATION (users.db)
# ------------------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(150) NOT NULL UNIQUE,
            email VARCHAR(200) NOT NULL UNIQUE,
            password VARCHAR(256) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def authenticate_user(login_identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    if "@" in login_identifier:
        cursor.execute("SELECT * FROM user WHERE LOWER(email) = ?", (login_identifier.lower(),))
    else:
        cursor.execute("SELECT * FROM user WHERE username = ?", (login_identifier,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password"], password):
        return dict(user)
    return None

def register_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE username = ? OR LOWER(email) = ?", (username, email.lower()))
    if cursor.fetchone():
        conn.close()
        return False, "Username or Email already registered!"

    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO user (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username, email.lower(), hashed_pw, datetime.utcnow())
        )
        conn.commit()
        conn.close()
        return True, "Account registered successfully! You can now log in."
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"


# ------------------------------------------------------------------------------
# 5. CRYPTOGRAPHIC FUNCTIONS
# ------------------------------------------------------------------------------
def decode_image_bytes(file_bytes_data):
    file_bytes = np.asarray(bytearray(file_bytes_data), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def encrypt_image_shares(img_bgr):
    rows, cols, ch = img_bgr.shape
    share1 = np.random.randint(0, 256, size=(rows, cols, ch), dtype=np.uint8)
    share2 = cv2.bitwise_xor(img_bgr, share1)
    return share1, share2

def decrypt_image_shares(s1_bgr, s2_bgr):
    if s1_bgr.shape != s2_bgr.shape:
        s2_bgr = cv2.resize(s2_bgr, (s1_bgr.shape[1], s1_bgr.shape[0]))
    return cv2.bitwise_xor(s1_bgr, s2_bgr)

def cv2_to_png_bytes(img_bgr):
    success, buffer = cv2.imencode(".png", img_bgr)
    return buffer.tobytes() if success else None

def cv2_to_rgb(img_bgr):
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def compute_entropy(channel_data):
    hist, _ = np.histogram(channel_data.flatten(), bins=256, range=[0, 256], density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))


# ------------------------------------------------------------------------------
# 6. SESSION STATE SETUP
# ------------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = "Guest"
if "s1_data" not in st.session_state:
    st.session_state["s1_data"] = None
if "s2_data" not in st.session_state:
    st.session_state["s2_data"] = None
if "orig_data" not in st.session_state:
    st.session_state["orig_data"] = None
if "orig_name" not in st.session_state:
    st.session_state["orig_name"] = "sample"


# ------------------------------------------------------------------------------
# 7. MODERN TOP BRAND HEADER
# ------------------------------------------------------------------------------
user_badge = f'<span class="status-dot"></span> Authenticated: <b>{st.session_state["username"]}</b>' if st.session_state["authenticated"] else '<span class="status-dot" style="background:#38bdf8; box-shadow: 0 0 8px #38bdf8;"></span> <b>Guest Access</b>'

st.markdown(f"""
<div class="brand-bar">
    <div class="brand-logo">
        <div class="brand-icon">🛡️</div>
        <div>
            <h1 class="brand-title">VISUAL CRYPTOGRAPHY SUITE</h1>
            <p class="brand-tagline">Next-Generation (2, 2) Visual Secret Sharing • Lossless Bitwise XOR Engine</p>
        </div>
    </div>
    <div class="user-pill">
        {user_badge}
    </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 8. SLEEK TOP-NAV TABS (NO INTRUSIVE SIDEBAR)
# ------------------------------------------------------------------------------
tab_encrypt, tab_decrypt, tab_entropy, tab_auth, tab_theory = st.tabs([
    "🔐  Encrypt Studio",
    "🔓  Decrypt & Reconstruct",
    "🔬  Entropy & Telemetry Lab",
    "👤  Credential Vault",
    "📚  Theory & Architecture"
])


# ==============================================================================
# TAB 1: ENCRYPT STUDIO
# ==============================================================================
with tab_encrypt:
    st.markdown("""
    <div class="step-grid">
        <div class="step-box active">
            <div class="step-badge">Phase 01</div>
            <div class="step-desc">Input Secret Image</div>
        </div>
        <div class="step-box active">
            <div class="step-badge">Phase 02</div>
            <div class="step-desc">Matrix Inspection</div>
        </div>
        <div class="step-box active">
            <div class="step-badge">Phase 03</div>
            <div class="step-desc">One-Time Pad Split</div>
        </div>
        <div class="step-box active">
            <div class="step-badge">Phase 04</div>
            <div class="step-desc">Lossless PNG Export</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_input1, c_input2 = st.columns([1, 1.2])

    with c_input1:
        st.markdown("#### 1️⃣ Select Input Image")
        source_type = st.radio(
            "Source Selection:",
            ["📤 Upload from Device", "🖼️ Quick Repository Sample"],
            horizontal=True
        )

        chosen_bgr = None
        img_title = "confidential_image"

        if source_type == "📤 Upload from Device":
            up_file = st.file_uploader(
                "Upload Image (PNG, JPG, JPEG, BMP, WEBP):",
                type=["png", "jpg", "jpeg", "bmp", "webp"]
            )
            if up_file:
                chosen_bgr = decode_image_bytes(up_file.getvalue())
                img_title = up_file.name.rsplit(".", 1)[0]
        else:
            sample_folder = os.path.join(STATIC_DIR, "uploads")
            available_samples = [f for f in os.listdir(sample_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))] if os.path.exists(sample_folder) else []
            if available_samples:
                sel = st.selectbox("Choose sample from server:", available_samples[:5])
                chosen_bgr = cv2.imread(os.path.join(sample_folder, sel))
                img_title = sel.rsplit(".", 1)[0]
            else:
                demo_mat = np.zeros((240, 360, 3), dtype=np.uint8)
                cv2.rectangle(demo_mat, (30, 30), (330, 210), (180, 50, 40), -1)
                cv2.putText(demo_mat, "SECRET", (85, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3)
                chosen_bgr = demo_mat
                img_title = "sample_secret"

    with c_input2:
        if chosen_bgr is not None:
            st.markdown("#### 2️⃣ Image Matrix Preview")
            st.image(cv2_to_rgb(chosen_bgr), caption=f"Confidential Image: {img_title}", use_container_width=True)

            h, w, c = chosen_bgr.shape
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Width × Height", f"{w} × {h} px")
            m_col2.metric("Color Depth", f"{c} Channels (BGR)")
            m_col3.metric("Raw Size", f"{(chosen_bgr.nbytes / 1024):.1f} KB")

            sync_disk = st.checkbox("Mirror backup copy to `static/shares/`", value=True)

            if st.button("🚀 Encrypt & Generate 2 Secret Shares", use_container_width=True):
                with st.spinner("Generating One-Time Pad noise and bitwise residue..."):
                    s1, s2 = encrypt_image_shares(chosen_bgr)
                    st.session_state["orig_data"] = chosen_bgr
                    st.session_state["s1_data"] = s1
                    st.session_state["s2_data"] = s2
                    st.session_state["orig_name"] = img_title

                    if sync_disk:
                        tag = st.session_state["username"] if st.session_state["authenticated"] else "guest"
                        u = uuid.uuid4().hex[:8]
                        cv2.imwrite(os.path.join(SHARES_FOLDER, f"{tag}_s1_{u}.png"), s1)
                        cv2.imwrite(os.path.join(SHARES_FOLDER, f"{tag}_s2_{u}.png"), s2)

                    st.toast("🎉 Shares generated successfully!", icon="🔐")

    # Output Display
    if st.session_state["s1_data"] is not None and st.session_state["s2_data"] is not None:
        st.markdown("---")
        st.markdown("### 3️⃣ Generated Secret Shares")

        st.markdown("""
        <div class="glow-banner-success">
            <strong>✅ Encryption Accomplished:</strong>
            The confidential image has been divided into two separate matrices.
            Share 1 represents purely independent uniform noise ($S_1 \sim U(0, 255)$), and Share 2 holds the complementary XOR residue ($S_2 = I \oplus S_1$).
        </div>
        """, unsafe_allow_html=True)

        o_col, s1_col, s2_col = st.columns(3)

        with o_col:
            st.markdown('<span class="tag-original">SOURCE SECRET IMAGE</span>', unsafe_allow_html=True)
            st.image(cv2_to_rgb(st.session_state["orig_data"]), use_container_width=True)
            st.caption(f"Original: {st.session_state['orig_name']}")

        with s1_col:
            st.markdown('<span class="tag-share1">SHARE 1 • UNIFORM NOISE MASK</span>', unsafe_allow_html=True)
            st.image(cv2_to_rgb(st.session_state["s1_data"]), use_container_width=True)
            st.caption("Contains zero mutual information with secret")
            s1_bytes = cv2_to_png_bytes(st.session_state["s1_data"])
            st.download_button(
                label="⬇️ Download Share 1 (PNG)",
                data=s1_bytes,
                file_name=f"share_1_{st.session_state['orig_name']}.png",
                mime="image/png",
                use_container_width=True
            )

        with s2_col:
            st.markdown('<span class="tag-share2">SHARE 2 • RESIDUE MATRIX</span>', unsafe_allow_html=True)
            st.image(cv2_to_rgb(st.session_state["s2_data"]), use_container_width=True)
            st.caption("XOR complementary residue matrix")
            s2_bytes = cv2_to_png_bytes(st.session_state["s2_data"])
            st.download_button(
                label="⬇️ Download Share 2 (PNG)",
                data=s2_bytes,
                file_name=f"share_2_{st.session_state['orig_name']}.png",
                mime="image/png",
                use_container_width=True
            )

        st.write("")
        with st.expander("⚡ Real-Time Proof: Instant Verification & Zero-Loss Check", expanded=True):
            test_rec = decrypt_image_shares(st.session_state["s1_data"], st.session_state["s2_data"])
            exact_match = np.array_equal(st.session_state["orig_data"], test_rec)
            v_col1, v_col2 = st.columns([1, 2.5])
            with v_col1:
                st.image(cv2_to_rgb(test_rec), caption="Reconstructed via S1 ⊕ S2", width=240)
            with v_col2:
                if exact_match:
                    st.success("🎯 **Mathematical Proof Confirmed**: 100.00% of reconstructed pixels match bit-for-bit!")
                    st.markdown("""
                    - **Bit Error Rate (BER):** `0.0000%`
                    - **Mean Squared Error (MSE):** `0.000`
                    - **Peak Signal-to-Noise Ratio (PSNR):** `∞ dB` (Lossless)
                    """)


# ==============================================================================
# TAB 2: DECRYPT & RECONSTRUCT
# ==============================================================================
with tab_decrypt:
    st.markdown("### 🔓 Image Decryption & Matrix Recombination")
    st.markdown(
        "Upload the two secret shares (**Share 1** and **Share 2**). "
        "The system calculates their pixel-wise XOR overlay to reveal the hidden image."
    )

    has_active_shares = (st.session_state["s1_data"] is not None and st.session_state["s2_data"] is not None)
    use_active = False

    if has_active_shares:
        st.markdown("""
        <div class="glow-banner-info">
            💡 <strong>Shares Ready in Memory!</strong> You can instantly use the shares generated in the Encrypt Studio without having to upload files from disk.
        </div>
        """, unsafe_allow_html=True)
        use_active = st.toggle("⚡ Use Active Session Shares", value=False)

    sh1 = None
    sh2 = None

    if use_active and has_active_shares:
        sh1 = st.session_state["s1_data"]
        sh2 = st.session_state["s2_data"]
        p1, p2 = st.columns(2)
        with p1:
            st.markdown('<span class="tag-share1">SESSION SHARE 1</span>', unsafe_allow_html=True)
            st.image(cv2_to_rgb(sh1), use_container_width=True)
        with p2:
            st.markdown('<span class="tag-share2">SESSION SHARE 2</span>', unsafe_allow_html=True)
            st.image(cv2_to_rgb(sh2), use_container_width=True)
    else:
        u1, u2 = st.columns(2)
        with u1:
            st.markdown("##### 📥 Drop Share 1")
            f1 = st.file_uploader("Upload Share 1 (PNG):", type=["png", "jpg", "jpeg", "bmp"], key="t2_s1")
            if f1:
                sh1 = decode_image_bytes(f1.getvalue())
                if sh1 is not None:
                    st.image(cv2_to_rgb(sh1), caption="Share 1 Input", use_container_width=True)
        with u2:
            st.markdown("##### 📥 Drop Share 2")
            f2 = st.file_uploader("Upload Share 2 (PNG):", type=["png", "jpg", "jpeg", "bmp"], key="t2_s2")
            if f2:
                sh2 = decode_image_bytes(f2.getvalue())
                if sh2 is not None:
                    st.image(cv2_to_rgb(sh2), caption="Share 2 Input", use_container_width=True)

    if sh1 is not None and sh2 is not None:
        st.markdown("---")

        with st.expander("🔬 Interactive Transparency Overlay Simulator", expanded=False):
            st.markdown("Simulate physically stacking transparency sheets together:")
            slider_val = st.slider("Transparency Overlay Alpha", 0.0, 1.0, 0.5, 0.05)
            s2_aligned = sh2
            if sh1.shape != s2_aligned.shape:
                s2_aligned = cv2.resize(s2_aligned, (sh1.shape[1], sh1.shape[0]))
            blended = cv2.addWeighted(sh1, slider_val, s2_aligned, 1.0 - slider_val, 0)
            st.image(cv2_to_rgb(blended), caption=f"Analog Overlay Preview (Alpha = {slider_val:.2f})", width=420)
            st.caption("Note: Linear analog blending only produces a gray blur; true digital reconstruction requires bitwise XOR.")

        st.write("")
        if st.button("🔓 Execute Cryptographic Decryption (XOR Overlay)", use_container_width=True):
            with st.spinner("Executing bitwise matrix XOR reconstruction..."):
                if sh1.shape != sh2.shape:
                    st.warning(f"⚠️ Resolution Mismatch: Share 1 is {sh1.shape} vs Share 2 is {sh2.shape}. Resized Share 2.")
                recovered_mat = decrypt_image_shares(sh1, sh2)
                recovered_png = cv2_to_png_bytes(recovered_mat)

                rec_tag = st.session_state["username"] if st.session_state["authenticated"] else "guest"
                rec_filename = f"reconstructed_{rec_tag}_{uuid.uuid4().hex[:8]}.png"
                cv2.imwrite(os.path.join(SHARES_FOLDER, rec_filename), recovered_mat)

            st.balloons()
            st.markdown("""
            <div class="glow-banner-success">
                <strong>🎉 Secret Image Successfully Recovered!</strong><br>
                Both shares have been combined with full mathematical integrity. Download the recovered image below.
            </div>
            """, unsafe_allow_html=True)

            r_col1, r_col2 = st.columns([1.3, 1])
            with r_col1:
                st.image(cv2_to_rgb(recovered_mat), caption="Recovered Image", use_container_width=True)
            with r_col2:
                st.markdown("#### 📋 Reconstruction Details")
                st.write(f"- **Resolution:** `{recovered_mat.shape[1]} × {recovered_mat.shape[0]} px`")
                st.write(f"- **Channels:** `{recovered_mat.shape[2]} (BGR)`")
                st.write(f"- **Cache:** `static/shares/{rec_filename}`")
                st.download_button(
                    label="⬇️ Download Reconstructed Image (PNG)",
                    data=recovered_png,
                    file_name="recovered_secret_image.png",
                    mime="image/png",
                    use_container_width=True
                )
    else:
        st.info("👆 Please supply both Share 1 and Share 2 above (or toggle active session shares) to unlock decryption.")


# ==============================================================================
# TAB 3: ENTROPY & TELEMETRY LAB
# ==============================================================================
with tab_entropy:
    st.markdown("### 🔬 Cybersecurity & Shannon Entropy Laboratory")
    st.markdown(
        "In cryptography, secrecy is formally proven through **Entropy** and **Correlation Analysis**. "
        "A secure secret sharing scheme must guarantee that individual shares exhibit maximum entropy "
        "and zero correlation with the underlying secret."
    )

    if st.session_state["orig_data"] is not None and st.session_state["s1_data"] is not None:
        im = st.session_state["orig_data"]
        s1 = st.session_state["s1_data"]
        s2 = st.session_state["s2_data"]

        e_orig = compute_entropy(im)
        e_s1 = compute_entropy(s1)
        e_s2 = compute_entropy(s2)

        orig_f = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).flatten().astype(float)
        s1_f = cv2.cvtColor(s1, cv2.COLOR_BGR2GRAY).flatten().astype(float)
        s2_f = cv2.cvtColor(s2, cv2.COLOR_BGR2GRAY).flatten().astype(float)

        c1 = np.corrcoef(orig_f, s1_f)[0, 1]
        c2 = np.corrcoef(orig_f, s2_f)[0, 1]

        st.markdown("#### 1. Information Entropy (Bits / Pixel)")
        e1, e2, e3 = st.columns(3)
        e1.metric("Original Image Entropy", f"{e_orig:.3f} bits/px", help="Structured Content")
        e2.metric("Share 1 Entropy", f"{e_s1:.3f} bits/px", help="Ideal Maximum ≈ 8.000 (Pure White Noise)")
        e3.metric("Share 2 Entropy", f"{e_s2:.3f} bits/px", help="Ideal Maximum ≈ 8.000 (Pure White Noise)")

        st.markdown("#### 2. Statistical Correlation with Secret")
        k1, k2 = st.columns(2)
        k1.metric("Pearson Correlation (Original ↔ Share 1)", f"{c1:.4f}", help="r ≈ 0.00 proves zero visual leakage")
        k2.metric("Pearson Correlation (Original ↔ Share 2)", f"{c2:.4f}", help="r ≈ 0.00 proves zero visual leakage")

        st.markdown("#### 3. Pixel Intensity Distribution (Histogram)")
        ho, _ = np.histogram(orig_f, bins=64, range=[0, 256])
        h1, _ = np.histogram(s1_f, bins=64, range=[0, 256])
        h2, _ = np.histogram(s2_f, bins=64, range=[0, 256])

        chart = pd.DataFrame({
            "Original Image": ho,
            "Share 1 (Noise)": h1,
            "Share 2 (Residue)": h2
        })
        st.line_chart(chart)
        st.caption("A completely flat histogram line demonstrates equal probability across all 256 intensity states (Maximum Entropy).")
    else:
        st.info("ℹ️ Please navigate to **🔐 Encrypt Studio** and encrypt an image first. Live statistical metrics and correlation charts will automatically populate here!")


# ==============================================================================
# TAB 4: CREDENTIAL VAULT
# ==============================================================================
with tab_auth:
    st.markdown("### 🗄️ SQLite Credential Vault (`users.db`)")
    st.markdown("Authentication system connected directly to the repository database with secure Werkzeug password hashing.")

    v_tab1, v_tab2, v_tab3 = st.tabs(["🔑 Sign In", "📝 Create Account", "📊 Active Database Records"])

    with v_tab1:
        st.markdown("##### Log in with existing credentials")
        lid = st.text_input("Username or Email Address:", placeholder="e.g. 221fa18128 or punatiravish@gmail.com")
        lpw = st.text_input("Password:", type="password", key="v_lpw")

        if st.button("Authenticate", use_container_width=True):
            if not lid or not lpw:
                st.warning("Please supply both credentials.")
            else:
                user = authenticate_user(lid, lpw)
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user["username"]
                    st.success(f"Welcome back, **{user['username']}**! Authentication verified.")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify your username/email and password.")

    with v_tab2:
        st.markdown("##### Register a new account")
        r_user = st.text_input("Choose Username:", placeholder="e.g. security_auditor")
        r_email = st.text_input("Email Address:", placeholder="e.g. user@domain.com")
        r_pw1 = st.text_input("Password:", type="password", key="v_rpw1")
        r_pw2 = st.text_input("Confirm Password:", type="password", key="v_rpw2")

        if st.button("Register Account", use_container_width=True):
            if not r_user or not r_email or not r_pw1:
                st.warning("All fields are required.")
            elif r_pw1 != r_pw2:
                st.error("Passwords do not match!")
            else:
                ok, msg = register_user(r_user, r_email, r_pw1)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    with v_tab3:
        st.markdown("##### Registered Entities in `users.db`")
        try:
            conn = get_db_connection()
            rows = conn.cursor().execute("SELECT id, username, email, created_at FROM user").fetchall()
            conn.close()
            if rows:
                data = [{"User ID": r["id"], "Username": r["username"], "Email": r["email"], "Created At": r["created_at"]} for r in rows]
                st.dataframe(data, use_container_width=True)
            else:
                st.info("Database table is currently empty.")
        except Exception as ex:
            st.error(f"Error querying SQLite: {str(ex)}")


# ==============================================================================
# TAB 5: THEORY & WHITEPAPER
# ==============================================================================
with tab_theory:
    st.markdown("### 📚 Theoretical Framework & Mathematical Proofs")
    st.markdown("""
    #### 1. Fundamental Concept
    Visual Cryptography was introduced by **Moni Naor and Adi Shamir** in 1994 as a cryptographic paradigm
    where visual secrets can be decoded directly by the human visual system (or bitwise hardware operations)
    without requiring complex decryption calculations.

    #### 2. The $(k, n)$ Threshold Architecture
    In a $(k, n)$ threshold scheme:
    - An image is partitioned into $n$ distinct shares.
    - Any subset of $k$ shares is sufficient to fully reconstruct the secret image.
    - Any collection of $k - 1$ or fewer shares yields **absolute zero mutual information** ($I(X; Y) = 0$).

    This application implements an optimized **$(2, 2)$ Threshold Scheme**:
    """)
    st.latex(r"I(x, y, c) \longrightarrow \{ S_1(x, y, c), \; S_2(x, y, c) \}")

    st.markdown("""
    #### 3. Mathematical Rigor: The Bitwise XOR One-Time Pad
    Let each pixel channel $I(x, y, c) \\in \\{0, 1, \\dots, 255\\}$ be represented as an 8-bit byte $\\mathbf{b} \\in \\mathbb{F}_2^8$:

    **Encryption Step:**
    $$\\mathbf{s}_1 \\xleftarrow{R} \\{0, 1\\}^8 \\quad (\\text{Uniform Random Sample})$$
    $$\\mathbf{s}_2 = \\mathbf{b} \\oplus \\mathbf{s}_1$$

    **Decryption Step:**
    $$\\mathbf{r} = \\mathbf{s}_1 \\oplus \\mathbf{s}_2 = \\mathbf{s}_1 \\oplus (\\mathbf{b} \\oplus \\mathbf{s}_1) = (\\mathbf{s}_1 \\oplus \\mathbf{s}_1) \\oplus \\mathbf{b} = \\mathbf{0} \\oplus \\mathbf{b} = \\mathbf{b}$$

    #### 4. Why Lossless Formats (PNG) Are Mandatory
    JPEG or WebP lossy compression uses discrete cosine transforms (DCT) and quantization, which alters pixel values by even a single bit:
    $$\\text{If } \\mathbf{s}_1' \\neq \\mathbf{s}_1 \\implies \\mathbf{s}_1' \\oplus \\mathbf{s}_2 \\neq \\mathbf{b}$$
    A single modified bit in XOR creates severe chromatic visual distortion. Hence, this application strictly uses **Lossless PNG**.
    """)

# ------------------------------------------------------------------------------
# 9. MINIMAL FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 8px 0;">
    Visual Cryptography Studio • Lossless (2, 2) Visual Secret Sharing • Built with Streamlit, OpenCV & NumPy
</div>
""", unsafe_allow_html=True)
