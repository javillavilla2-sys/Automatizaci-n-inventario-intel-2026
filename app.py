import streamlit as st
import os
from datetime import datetime
from intel import process_intel_sales, process_intel_inventory

# ── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Generación Reporte a Fabricantes",
    layout="wide",
    initial_sidebar_state="expanded",
)

now_str = datetime.now().strftime("%d %b %Y  ·  %H:%M")
output_path = os.path.join(os.getcwd(), "output")

# ── ESTILOS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:         #f4f7fb;
    --white:      #ffffff;
    --navy:       #002d62;
    --navy-mid:   #0050a0;
    --blue:       #0068b5;
    --teal:       #00aeef;
    --text-h:     #0d1b2a;
    --text-body:  #374151;
    --text-muted: #94a3b8;
    --border:     #dde5f0;
    --sh-sm:      0 1px 8px rgba(0,45,98,0.08);
    --sh-md:      0 4px 20px rgba(0,45,98,0.12);
    --sh-lg:      0 12px 40px rgba(0,45,98,0.16);
    --r:          14px;
    --r-sm:       10px;
}

/* GLOBAL */
html, body, .stApp { background: var(--bg) !important; font-family: 'Inter', sans-serif !important; color: var(--text-body) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1240px !important; }

/* ANIMATIONS */
@keyframes fadeDown { from{opacity:0;transform:translateY(-12px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeUp   { from{opacity:0;transform:translateY(12px)}  to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn   { from{opacity:0} to{opacity:1} }
@keyframes pulsBtn  {
    0%,100%{ box-shadow: 0 4px 16px rgba(0,104,181,0.28); }
    50%    { box-shadow: 0 4px 24px rgba(0,104,181,0.45); }
}
@keyframes barWidth { from{width:0%} }

/* ═══ HEADER ═══════════════════════════════════ */
.top-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 55%, var(--blue) 100%);
    border-radius: 0 0 18px 18px;
    padding: 20px 32px;
    margin: -1rem -2rem 28px -2rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: var(--sh-lg);
    animation: fadeDown 0.5s cubic-bezier(0.22,1,0.36,1) both;
    position: relative; overflow: hidden;
}
.top-header::after {
    content:''; position:absolute; top:-50%; right:-4%;
    width:240px; height:240px;
    background: radial-gradient(circle, rgba(0,174,239,0.20) 0%, transparent 70%);
    pointer-events:none;
}
.hbrand { display:flex; align-items:center; gap:14px; }
.hbrand-icon {
    width:44px; height:44px; border-radius:12px;
    background:rgba(255,255,255,0.13); border:1px solid rgba(255,255,255,0.22);
    display:flex; align-items:center; justify-content:center; font-size:20px;
}
.hbrand-sup  { font-size:10px; color:rgba(255,255,255,0.5); letter-spacing:3px; text-transform:uppercase; font-weight:600; }
.hbrand-name { font-family:'Syne',sans-serif; font-size:20px; font-weight:800; color:#fff; margin:2px 0 0; letter-spacing:-0.2px; }
.hright { text-align:right; }
.hright-pill {
    display:inline-block;
    background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.24);
    color:#fff; font-family:'Syne',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:2px; padding:4px 12px; border-radius:20px; text-transform:uppercase; margin-bottom:5px;
}
.hright-ts { font-size:11px; color:rgba(255,255,255,0.42); }

/* ═══ INFO CHIPS ════════════════════════════════ */
.chips-row {
    display:flex; gap:8px; flex-wrap:wrap; margin-bottom:22px;
    animation: fadeUp 0.45s 0.1s cubic-bezier(0.22,1,0.36,1) both;
}
.chip {
    display:inline-flex; align-items:center; gap:6px;
    background:#edf3fb; border:1px solid #cddcef; border-radius:20px;
    padding:5px 13px; font-size:12px; font-weight:500; color:var(--blue);
}
.chip-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }

/* ═══ SECTION TITLE ════════════════════════════ */
.sec-wrap {
    display:flex; align-items:center; gap:10px;
    margin: 24px 0 14px;
    animation: fadeIn 0.4s ease both;
}
.sec-icon { font-size:15px; }
.sec-title {
    font-family:'Syne',sans-serif; font-size:12px; font-weight:700;
    color:var(--text-h); text-transform:uppercase; letter-spacing:2.5px; white-space:nowrap;
}
.sec-line { flex:1; height:1px; background:linear-gradient(90deg,var(--border),transparent); }

/* ═══ MODULE CARD ═══════════════════════════════ */
.mod-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 28px 32px;
    box-shadow: var(--sh-sm);
    position: relative; overflow: hidden;
    animation: fadeUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
    transition: box-shadow 0.2s ease;
}
.mod-card:hover { box-shadow: var(--sh-md); }
.mod-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg, var(--blue), var(--teal));
}
.mod-head { display:flex; align-items:flex-start; gap:14px; margin-bottom:22px; }
.mod-icon {
    width:48px; height:48px; border-radius:12px; flex-shrink:0;
    background:linear-gradient(135deg,#ddeaf9,#c5d8f2);
    display:flex; align-items:center; justify-content:center; font-size:22px;
}
.mod-title { font-family:'Syne',sans-serif; font-size:17px; font-weight:800; color:var(--text-h); margin:0 0 4px; }
.mod-sub   { font-size:13px; color:var(--text-muted); line-height:1.5; }
.upload-lbl {
    font-size:11px; font-weight:600; color:var(--text-muted);
    text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px;
}
.divider { height:1px; background:linear-gradient(90deg,var(--border),transparent); margin:18px 0; }

/* ═══ STREAMLIT FILE UPLOADER ════════════════════ */
[data-testid="stFileUploader"] > div {
    background: #f7faff !important;
    border: 2px dashed #b8cfe8 !important;
    border-radius: 12px !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--blue) !important;
    background: #eef4fc !important;
}

/* ═══ BUTTONS ══════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--blue), var(--navy-mid)) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important; font-weight: 700 !important;
    border: none !important; border-radius: var(--r-sm) !important;
    padding: 10px 26px !important; cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(0,104,181,0.28) !important;
    transition: transform 0.18s, box-shadow 0.18s, opacity 0.18s !important;
    animation: pulsBtn 2.5s ease infinite !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(0,104,181,0.38) !important;
}
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #059669, #047857) !important;
    color: #fff !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: var(--r-sm) !important; padding: 10px 26px !important;
    box-shadow: 0 4px 16px rgba(5,150,105,0.28) !important;
    transition: transform 0.18s, box-shadow 0.18s !important;
}
[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(5,150,105,0.38) !important;
}

/* ═══ ALERTS ═══════════════════════════════════ */
[data-testid="stAlert"] { border-radius: var(--r-sm) !important; animation: fadeUp 0.3s ease both !important; }

/* ═══ SIDEBAR ══════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: var(--sh-sm) !important;
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

/* Sidebar radio → nav style */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    display: flex !important; flex-direction: column !important; gap: 3px !important; padding: 0 !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    display: flex !important; align-items: center !important; gap: 9px !important;
    padding: 9px 13px !important; border-radius: var(--r-sm) !important;
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-body) !important; cursor: pointer !important;
    transition: background 0.18s, color 0.18s !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: #edf3fb !important; color: var(--blue) !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {
    background: #ddeaf8 !important; color: var(--blue) !important; font-weight: 600 !important;
}

/* ═══ FOOTER ════════════════════════════════════ */
.footer {
    margin-top: 48px; padding: 16px 0;
    border-top: 1px solid var(--border); text-align: center;
    font-size: 11px; color: var(--text-muted); letter-spacing: 0.8px;
    animation: fadeIn 0.5s ease both;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# SIDEBAR  (solo Streamlit nativo — sin HTML custom)
# ═══════════════════════════════════════════════
with st.sidebar:

    # ── Logo / Brand ──
    st.markdown(
        "<div style='text-align:center;padding:0 8px 20px;border-bottom:1px solid #dde5f0;margin-bottom:18px'>"
        "<span style='font-size:30px'>🖥</span><br>"
        "<span style='font-family:Syne,sans-serif;font-size:14px;font-weight:800;color:#0d1b2a'>GESTIÓN REPORTE A FABRICANTES</span><br>"
        "<span style='font-size:10px;color:#94a3b8;letter-spacing:2px;text-transform:uppercase'>Platform 2026</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Label módulos activos ──
    st.markdown(
        "<p style='font-size:10px;color:#94a3b8;text-transform:uppercase;"
        "letter-spacing:2px;font-weight:600;margin:0 0 8px 4px'>Módulos Activos</p>",
        unsafe_allow_html=True,
    )

    opcion = st.radio(
        "Selecciona proceso:",
        ["Ventas Intel", "Inventario Intel"],
        label_visibility="collapsed",
    )

    # ── Separador ──
    st.markdown(
        "<hr style='border:none;border-top:1px solid #dde5f0;margin:20px 0 14px'>",
        unsafe_allow_html=True,
    )

    # ── Label próximamente ──
    st.markdown(
        "<p style='font-size:10px;color:#94a3b8;text-transform:uppercase;"
        "letter-spacing:2px;font-weight:600;margin:0 0 10px 4px'>Próximamente</p>",
        unsafe_allow_html=True,
    )

    # ── Tarjetas "pronto" — inline styles, sin clases externas ──
    BRANDS = [("💻", "Lenovo"), ("🖨️", "Epson"), ("🖱️", "HP Inc.")]
    for icon, name in BRANDS:
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;"
            f"padding:9px 12px;background:#f7faff;border:1px solid #dde5f0;"
            f"border-radius:10px;margin-bottom:6px;opacity:0.75'>"
            f"<span style='font-size:15px'>{icon}</span>"
            f"<span style='font-size:12px;font-weight:600;color:#374151;flex:1'>{name}</span>"
            f"<span style='font-size:9px;font-weight:700;letter-spacing:1px;"
            f"text-transform:uppercase;background:#ddeaf8;color:#0068b5;"
            f"padding:2px 8px;border-radius:10px'>Pronto</span>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════
st.markdown(f"""
<div class="top-header">
    <div class="hbrand">
        <div class="hbrand-icon">🖥</div>
        <div>
            <div class="hbrand-sup">Automation Platform</div>
            <div class="hbrand-name">GESTIÓN REPORTE A FABRICANTES 2026 2026</div>
        </div>
    </div>
    <div class="hright">
        <div class="hright-pill">2026</div><br>
        <div class="hright-ts">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chips de estado ──
st.markdown("""
<div class="chips-row">
    <span class="chip"><span class="chip-dot" style="background:#00aeef"></span>Intel — Activo</span>
    <span class="chip"><span class="chip-dot" style="background:#d97706"></span>Lenovo — Próximamente</span>
    <span class="chip"><span class="chip-dot" style="background:#d97706"></span>Epson — Próximamente</span>
    <span class="chip"><span class="chip-dot" style="background:#d97706"></span>HP Inc. — Próximamente</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# HELPER – section title
# ═══════════════════════════════════════════════
def section(icon, title):
    st.markdown(f"""
    <div class="sec-wrap">
        <span class="sec-icon">{icon}</span>
        <span class="sec-title">{title}</span>
        <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# MÓDULO: VENTAS INTEL
# ═══════════════════════════════════════════════
if opcion == "Ventas Intel":

    section("📊", "Ventas Intel")

    # Card header (solo HTML estático, sin widgets dentro del div)
    st.markdown("""
    <div class="mod-card">
        <div class="mod-head">
            <div class="mod-icon">📊</div>
            <div>
                <p class="mod-title">Procesar Ventas Intel</p>
                <p class="mod-sub">Carga tu archivo Excel de ventas y genera el reporte procesado automáticamente.</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Contenido interactivo fuera del div HTML (así Streamlit lo renderiza bien)
    with st.container():
        st.markdown(
            "<p class='upload-lbl'>📎 &nbsp;Archivo de entrada</p>",
            unsafe_allow_html=True,
        )
        file = st.file_uploader(
            "Sube archivo Ventas Intel", type=["xlsx"], label_visibility="collapsed"
        )

        if file is not None:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            col_btn, _ = st.columns([1, 4])
            with col_btn:
                procesar = st.button("⚡  Procesar archivo", key="btn_ventas")

            if procesar:
                with open("temp.xlsx", "wb") as f:
                    f.write(file.getbuffer())
                with st.spinner("Procesando ventas Intel…"):
                    ok, msg, out_file = process_intel_sales("temp.xlsx", output_path)
                if ok:
                    st.success(f"✅  {msg}")
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    col_dl, _ = st.columns([1, 4])
                    with col_dl:
                        with open(out_file, "rb") as f:
                            st.download_button(
                                label="⬇  Descargar Resultado",
                                data=f,
                                file_name=os.path.basename(out_file),
                                key="dl_ventas",
                            )
                else:
                    st.error(f"❌  {msg}")


# ═══════════════════════════════════════════════
# MÓDULO: INVENTARIO INTEL
# ═══════════════════════════════════════════════
elif opcion == "Inventario Intel":

    section("📦", "Inventario Intel")

    st.markdown("""
    <div class="mod-card">
        <div class="mod-head">
            <div class="mod-icon">📦</div>
            <div>
                <p class="mod-title">Procesar Inventario Intel</p>
                <p class="mod-sub">Carga tu archivo Excel de inventario y genera el reporte procesado automáticamente.</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        st.markdown(
            "<p class='upload-lbl'>📎 &nbsp;Archivo de entrada</p>",
            unsafe_allow_html=True,
        )
        file = st.file_uploader(
            "Sube archivo Inventario", type=["xlsx"], label_visibility="collapsed"
        )

        if file is not None:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            col_btn, _ = st.columns([1, 4])
            with col_btn:
                procesar = st.button("⚡  Procesar archivo", key="btn_inv")

            if procesar:
                with open("temp_inv.xlsx", "wb") as f:
                    f.write(file.getbuffer())
                with st.spinner("Procesando inventario Intel…"):
                    ok, msg, out_file = process_intel_inventory("temp_inv.xlsx", output_path)
                if ok:
                    st.success(f"✅  {msg}")
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    col_dl, _ = st.columns([1, 4])
                    with col_dl:
                        with open(out_file, "rb") as f:
                            st.download_button(
                                label="⬇  Descargar Resultado",
                                data=f,
                                file_name=os.path.basename(out_file),
                                key="dl_inv",
                            )
                else:
                    st.error(f"❌  {msg}")


# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
    Propieda SED INTERNATIONAL EQUIPO TRANSFORMACIÓN DIGITAL &nbsp;·&nbsp; 2026 &nbsp;·&nbsp; {now_str}
</div>
""", unsafe_allow_html=True)