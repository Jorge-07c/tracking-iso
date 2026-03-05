import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="TrackISO", page_icon="⚙️", layout="wide")

# ════════════════════════════════════
# TEMA VISUAL — CSS INDUSTRIAL
# ════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-base:    #0d0f12;
    --bg-card:    #141720;
    --bg-card2:   #1a1e2a;
    --bg-input:   #1e2230;
    --border:     #2a2f3e;
    --orange:     #ff6b1a;
    --orange-dim: #cc5514;
    --orange-glow:#ff6b1a33;
    --teal:       #00d4aa;
    --yellow:     #ffd166;
    --red:        #ff4757;
    --purple:     #a78bfa;
    --text-main:  #e8eaf0;
    --text-muted: #6b7280;
    --text-dim:   #9ca3af;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: var(--bg-base) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
}

[data-testid="stSidebar"] {
    background: #0a0c10 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }

h1 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; font-size: 2rem !important;
    color: var(--text-main) !important; letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-left: 4px solid var(--orange) !important;
    padding-left: 14px !important; margin-bottom: 4px !important;
}
h2 { font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important;
     color: var(--orange) !important; letter-spacing: 0.5px !important;
     font-size: 1.25rem !important; text-transform: uppercase !important; }
h3 { font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important;
     color: var(--teal) !important; font-size: 1.05rem !important; }

input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important; color: var(--text-main) !important;
    transition: border-color 0.2s !important;
}
input:focus, textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 2px var(--orange-glow) !important;
}
[data-baseweb="select"] > div {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important; color: var(--text-main) !important;
}

[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-dim) 100%) !important;
    color: #fff !important; border: none !important; border-radius: 4px !important;
    font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important;
    font-size: 1rem !important; letter-spacing: 1px !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 15px var(--orange-glow) !important; transition: all 0.2s !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px var(--orange-glow) !important;
}
[data-testid="stButton"] > button[kind="secondary"],
[data-testid="stButton"] > button {
    background: transparent !important; border: 1px solid var(--border) !important;
    color: var(--text-dim) !important; border-radius: 4px !important; transition: all 0.2s !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover,
[data-testid="stButton"] > button:hover {
    border-color: var(--orange) !important; color: var(--orange) !important;
}

[data-testid="stMetric"] {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: 6px !important; padding: 14px 18px !important;
    border-top: 2px solid var(--orange) !important; transition: all 0.2s !important;
}
[data-testid="stMetric"]:hover {
    border-top-color: var(--teal) !important; box-shadow: 0 4px 20px #00d4aa18 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important; font-size: 0.72rem !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
    font-family: 'Share Tech Mono', monospace !important;
}
[data-testid="stMetricValue"] {
    color: var(--text-main) !important; font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; font-size: 1.6rem !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: 6px !important; margin-bottom: 8px !important;
    border-left: 3px solid var(--orange) !important;
}
[data-testid="stExpander"]:hover { border-left-color: var(--teal) !important; }
[data-testid="stExpander"] summary {
    color: var(--text-main) !important; font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important; letter-spacing: 0.5px !important;
}

hr { border-color: var(--border) !important; margin: 18px 0 !important; }

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--orange), var(--teal)) !important;
}
[data-testid="stProgressBar"] > div { background: var(--border) !important; }

[data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important; font-size: 0.78rem !important;
}

code { font-family: 'Share Tech Mono', monospace !important;
       background: var(--bg-card2) !important; color: var(--teal) !important;
       border-radius: 3px !important; padding: 2px 6px !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--orange); }

[data-testid="stMainBlockContainer"] > div > div {
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════
# HELPERS VISUALES
# ════════════════════════════════════
COLORES_ESTADO = {
    "Recibido": "#6b7280", "En Proceso": "#ff6b1a",
    "Control Calidad": "#a78bfa", "Terminación": "#00d4aa", "Despacho": "#ffd166"
}

def badge(texto, color="#ff6b1a"):
    return (f'<span style="background:{color}22;color:{color};border:1px solid {color}55;'
            f'border-radius:3px;padding:2px 8px;font-size:0.68rem;'
            f'font-family:\'Share Tech Mono\',monospace;letter-spacing:1px;'
            f'font-weight:600;text-transform:uppercase;">{texto}</span>')

def tarjeta_orden(serial, cliente, tipo, estado, dias):
    c = COLORES_ESTADO.get(estado, "#6b7280")
    return f"""
    <div style="background:#141720;border:1px solid #2a2f3e;border-left:3px solid {c};
                border-radius:6px;padding:14px 18px;margin-bottom:6px;
                box-shadow:0 2px 12px #00000040;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <div>
                <span style="font-family:'Share Tech Mono',monospace;color:{c};font-size:0.9rem;font-weight:700;">{serial}</span>
                <span style="color:#3a3f50;margin:0 8px;">·</span>
                <span style="color:#e8eaf0;font-weight:600;">{cliente}</span>
            </div>
            <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
                {badge(tipo,"#6b7280")}&nbsp;{badge(estado,c)}
                <span style="color:#6b7280;font-size:0.72rem;font-family:'Share Tech Mono',monospace;">⏱ {dias}d</span>
            </div>
        </div>
    </div>"""

def header_modulo(icono, titulo, subtitulo):
    st.markdown(f"""
    <div style="margin-bottom:22px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="font-size:1.6rem;">{icono}</span>
            <div style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.9rem;
                        color:#e8eaf0;letter-spacing:1px;text-transform:uppercase;
                        border-left:4px solid #ff6b1a;padding-left:12px;">{titulo}</div>
        </div>
        <p style="color:#6b7280;font-size:0.72rem;margin:0;letter-spacing:0.5px;
                  font-family:'Share Tech Mono',monospace;padding-left:4px;">▸ {subtitulo}</p>
    </div>
    <hr style="border-color:#2a2f3e;margin:0 0 20px 0;">
    """, unsafe_allow_html=True)

def checklist_visual(orden):
    ESTADOS_L = ["Recibido", "En Proceso", "Control Calidad", "Terminación", "Despacho"]
    ICONOS_L  = {"Recibido":"📥","En Proceso":"⚙️","Control Calidad":"🔬","Terminación":"✅","Despacho":"🚚"}
    idx = ESTADOS_L.index(orden["estado"])
    items = ""
    for i, etapa in enumerate(ESTADOS_L):
        if i < idx:   bg, col, dot = "#00d4aa15", "#00d4aa", "✓"
        elif i == idx: bg, col, dot = "#ff6b1a22", "#ff6b1a", ICONOS_L[etapa]
        else:          bg, col, dot = "#1a1e2a",   "#3a3f50", "○"
        conector = ""
        if i < len(ESTADOS_L) - 1:
            lc = "#00d4aa" if i < idx else "#2a2f3e"
            conector = f'<div style="flex:1;height:2px;background:{lc};margin:0 3px;"></div>'
        items += f"""<div style="display:flex;align-items:center;flex:1;">
            <div style="background:{bg};border:1px solid {col}44;border-radius:4px;
                        padding:7px 4px;text-align:center;min-width:0;flex:1;">
                <div style="font-size:0.95rem;margin-bottom:2px;">{dot}</div>
                <div style="color:{col};font-size:0.6rem;font-family:'Share Tech Mono',monospace;
                            letter-spacing:0.5px;text-transform:uppercase;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{etapa}</div>
            </div>{conector}</div>"""
    st.markdown(f"""
    <div style="margin:10px 0 14px 0;">
        <div style="color:#6b7280;font-size:0.65rem;font-family:'Share Tech Mono',monospace;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:7px;">▸ ETAPAS DE PRODUCCIÓN</div>
        <div style="display:flex;align-items:center;width:100%;">{items}</div>
    </div>""", unsafe_allow_html=True)

def historial_html(historial):
    ICONOS_MAP = {"Recibido":"📥","En Proceso":"⚙️","Control Calidad":"🔬","Terminación":"✅","Despacho":"🚚"}
    items = ""
    for h in reversed(historial):
        quien = f" · <span style='color:#ff6b1a;'>{h['actualizado_por']}</span>" if h.get("actualizado_por") else ""
        items += f"""<div style="border-left:2px solid #2a2f3e;padding:5px 12px;margin:4px 0;
                        font-family:'Share Tech Mono',monospace;font-size:0.72rem;">
            <span style="color:#ff6b1a;">{ICONOS_MAP.get(h.get('estado',''),'●')}</span>
            <span style="color:#e8eaf0;font-weight:600;"> {h.get('estado','')}</span>
            <span style="color:#3a3f50;"> · {h.get('fecha','')[:16].replace('T',' ')}</span>{quien}
            <br><span style="color:#6b7280;font-style:italic;">{h.get('nota','')}</span>
        </div>"""
    st.markdown(items, unsafe_allow_html=True)

def seccion_label(texto, color="#6b7280"):
    st.markdown(f'<p style="color:{color};font-size:0.7rem;font-family:\'Share Tech Mono\',monospace;letter-spacing:1px;text-transform:uppercase;margin:14px 0 8px 0;">▸ {texto}</p>', unsafe_allow_html=True)


# ════════════════════════════════════
# DATOS Y CONSTANTES
# ════════════════════════════════════
DATA_FILE = Path("ordenes.json")

def cargar():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar(ordenes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, ensure_ascii=False, indent=2)

ESTADOS = ["Recibido", "En Proceso", "Control Calidad", "Terminación", "Despacho"]
TIPOS   = ["Textil", "Impresión", "Promocional"]
ICONOS  = {"Recibido":"📥","En Proceso":"⚙️","Control Calidad":"🔬","Terminación":"✅","Despacho":"🚚"}

USUARIOS = {
    "admin":      {"password": "admin123",  "rol": "Administrador"},
    "ventas":     {"password": "ventas123", "rol": "Ventas"},
    "produccion": {"password": "prod123",   "rol": "Producción"},
}
ACCESOS = {
    "Administrador": ["📋 Cotización", "🏭 Producción", "📊 Dashboard", "🔍 Trazabilidad"],
    "Ventas":        ["📋 Cotización",                  "📊 Dashboard", "🔍 Trazabilidad"],
    "Producción":    [                "🏭 Producción",  "📊 Dashboard", "🔍 Trazabilidad"],
}

for key, default in [("usuario", None), ("rol", None), ("ordenes", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.ordenes is None:
    st.session_state.ordenes = cargar()


# ════════════════════════════════════
# LOGIN
# ════════════════════════════════════
if st.session_state.usuario is None:
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px;">
            <div style="font-family:'Rajdhani',sans-serif;font-size:3rem;font-weight:700;
                        color:#ff6b1a;letter-spacing:4px;text-transform:uppercase;
                        text-shadow:0 0 30px #ff6b1a55;">⚙ TRACKISO</div>
            <div style="font-family:'Share Tech Mono',monospace;color:#6b7280;
                        font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;margin-top:4px;">
                SISTEMA INTERNO · ISO 9001:2015</div>
            <div style="width:60px;height:2px;background:linear-gradient(90deg,transparent,#ff6b1a,transparent);
                        margin:12px auto 0;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style="background:#141720;border:1px solid #2a2f3e;border-top:2px solid #ff6b1a;
                    border-radius:8px;padding:28px 32px;box-shadow:0 8px 40px #00000060;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:#6b7280;
                        letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;">▸ INICIAR SESIÓN</div>""",
                    unsafe_allow_html=True)
        usuario_input  = st.text_input("Usuario", placeholder="Ingresa tu usuario")
        password_input = st.text_input("Contraseña", type="password", placeholder="••••••••")
        if st.button("⚡ ACCEDER AL SISTEMA", use_container_width=True, type="primary"):
            u = USUARIOS.get(usuario_input)
            if u and u["password"] == password_input:
                st.session_state.usuario = usuario_input
                st.session_state.rol     = u["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#0a0c10;border:1px solid #2a2f3e;border-radius:6px;padding:14px 18px;">
            <div style="font-family:'Share Tech Mono',monospace;color:#6b7280;font-size:0.68rem;
                        letter-spacing:1px;margin-bottom:8px;">▸ ACCESOS DE PRUEBA</div>""",
                    unsafe_allow_html=True)
        st.code("admin / admin123      → Administrador\nventas / ventas123   → Ventas\nproduccion / prod123 → Producción", language="text")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ════════════════════════════════════
# FUNCIONES HELPER
# ════════════════════════════════════
def generar_serial(tipo):
    prefijo = {"Textil": "TEX", "Impresión": "IMP", "Promocional": "PRO"}[tipo]
    return f"{prefijo}-{datetime.now().year}-{str(uuid.uuid4())[:4].upper()}"

def get_fecha(orden):
    return orden.get("fecha") or orden.get("fecha_creacion") or "—"

def dias_transcurridos(orden):
    try:
        return (datetime.now() - datetime.fromisoformat(get_fecha(orden))).days
    except:
        return "—"


# ════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════
rol_actual       = st.session_state.rol
modulos_visibles = ACCESOS[rol_actual]
ROL_C = {"Administrador": "#ff6b1a", "Ventas": "#00d4aa", "Producción": "#a78bfa"}
rc    = ROL_C.get(rol_actual, "#6b7280")

with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 0 14px;text-align:center;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.5rem;font-weight:700;
                    color:#ff6b1a;letter-spacing:3px;">⚙ TRACKISO</div>
        <div style="font-family:'Share Tech Mono',monospace;color:#3a3f50;font-size:0.62rem;letter-spacing:2px;">
            ISO 9001:2015</div>
    </div>
    <hr style="border-color:#1e2230;margin:0 0 14px;">
    <div style="background:#141720;border:1px solid #2a2f3e;border-left:3px solid {rc};
                border-radius:4px;padding:10px 14px;margin-bottom:14px;">
        <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">USUARIO ACTIVO</div>
        <div style="color:#e8eaf0;font-weight:600;font-size:0.9rem;">👤 {st.session_state.usuario}</div>
        <div style="margin-top:5px;">
            <span style="background:{rc}22;color:{rc};border:1px solid {rc}44;border-radius:3px;
                         padding:1px 7px;font-size:0.64rem;font-family:'Share Tech Mono',monospace;
                         letter-spacing:1px;text-transform:uppercase;">{rol_actual}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("MÓDULOS", modulos_visibles, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1e2230;margin:14px 0;'>", unsafe_allow_html=True)

    _todas       = st.session_state.ordenes
    _activas     = sum(1 for o in _todas if o["estado"] != "Despacho")
    _despachadas = sum(1 for o in _todas if o["estado"] == "Despacho")

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;margin-bottom:14px;">
        <div style="background:#141720;border:1px solid #2a2f3e;border-top:2px solid #ff6b1a;
                    border-radius:4px;padding:9px 6px;text-align:center;">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;
                        color:#e8eaf0;">{len(_todas)}</div>
            <div style="color:#6b7280;font-size:0.58rem;font-family:'Share Tech Mono',monospace;
                        text-transform:uppercase;">Total</div>
        </div>
        <div style="background:#141720;border:1px solid #2a2f3e;border-top:2px solid #00d4aa;
                    border-radius:4px;padding:9px 6px;text-align:center;">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;
                        color:#e8eaf0;">{_activas}</div>
            <div style="color:#6b7280;font-size:0.58rem;font-family:'Share Tech Mono',monospace;
                        text-transform:uppercase;">Activas</div>
        </div>
        <div style="background:#141720;border:1px solid #2a2f3e;border-top:2px solid #ffd166;
                    border-radius:4px;padding:9px 6px;text-align:center;">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;
                        color:#e8eaf0;">{_despachadas}</div>
            <div style="color:#6b7280;font-size:0.58rem;font-family:'Share Tech Mono',monospace;
                        text-transform:uppercase;">Despach.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Cerrar sesión", use_container_width=True, type="secondary"):
        st.session_state.usuario = None
        st.session_state.rol     = None
        st.rerun()


# ════════════════════════════════════
# MÓDULO 1 — COTIZACIÓN
# ════════════════════════════════════
if menu == "📋 Cotización":
    header_modulo("📋", "COTIZACIÓN", "Ventas · Genera la orden de producción")

    col1, col2 = st.columns(2)
    with col1:
        seccion_label("DATOS DEL CLIENTE")
        cliente  = st.text_input("Cliente / Empresa", placeholder="Nombre del cliente o empresa")
        tipo     = st.selectbox("Tipo de producto", TIPOS)
        desc     = st.text_input("Descripción del producto", placeholder="¿Qué se va a fabricar?")
    with col2:
        seccion_label("DATOS DEL PEDIDO")
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
        precio   = st.number_input("Precio unitario ($)", min_value=0.0, step=0.01)
        tiempo   = st.number_input("Tiempo estimado (días)", min_value=1, value=7)

    specs  = st.text_area("Especificaciones técnicas", placeholder="Colores, materiales, tallas, medidas...")
    imagen = st.file_uploader("Imagen de referencia", type=["png", "jpg", "jpeg"])
    if imagen:
        col_img, _ = st.columns([1, 4])
        col_img.image(imagen, caption="Vista previa", use_container_width=True)

    # Preview
    total_est = cantidad * precio
    st.markdown(f"""
    <div style="background:#141720;border:1px solid #2a2f3e;border-radius:6px;
                padding:18px 22px;margin:16px 0 20px;">
        <div style="color:#6b7280;font-size:0.68rem;font-family:'Share Tech Mono',monospace;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">▸ PREVIEW DE COTIZACIÓN</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">
            <div>
                <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Cliente</div>
                <div style="color:#e8eaf0;font-weight:600;overflow:hidden;text-overflow:ellipsis;
                            white-space:nowrap;">{cliente or "—"}</div>
            </div>
            <div>
                <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Cantidad</div>
                <div style="color:#ff6b1a;font-family:'Rajdhani',sans-serif;font-weight:700;
                            font-size:1.3rem;">{cantidad} <span style="font-size:0.75rem;color:#6b7280;">unid.</span></div>
            </div>
            <div>
                <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Precio Unit.</div>
                <div style="color:#ff6b1a;font-family:'Rajdhani',sans-serif;font-weight:700;
                            font-size:1.3rem;">${precio:.2f}</div>
            </div>
            <div>
                <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Total Estimado</div>
                <div style="color:#00d4aa;font-family:'Rajdhani',sans-serif;font-weight:700;
                            font-size:1.5rem;">${total_est:,.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡ GENERAR ORDEN DE PRODUCCIÓN", use_container_width=True, type="primary"):
        if not cliente.strip():
            st.error("⚠️ Ingresa el nombre del cliente.")
        elif not desc.strip():
            st.error("⚠️ Ingresa la descripción del producto.")
        elif precio <= 0:
            st.error("⚠️ El precio debe ser mayor a 0.")
        else:
            import base64
            img_b64 = ""
            if imagen:
                img_b64 = "data:image/" + imagen.name.split(".")[-1] + ";base64," + base64.b64encode(imagen.read()).decode()
            serial = generar_serial(tipo)
            ahora  = datetime.now().isoformat()
            nueva  = {
                "serial": serial, "cliente": cliente.strip(), "tipo": tipo,
                "desc": desc.strip(), "cantidad": cantidad, "precio": precio,
                "tiempo": tiempo, "specs": specs.strip(), "imagen": img_b64,
                "estado": "Recibido", "fecha": ahora,
                "creado_por": st.session_state.usuario,
                "historial": [{"estado": "Recibido", "fecha": ahora,
                               "nota": f"Orden creada por {st.session_state.usuario}",
                               "actualizado_por": st.session_state.usuario}]
            }
            st.session_state.ordenes.append(nueva)
            guardar(st.session_state.ordenes)
            st.success(f"✅ Orden **{serial}** generada y enviada a Producción.")
            st.balloons()

    mis_ordenes = [o for o in st.session_state.ordenes if o.get("creado_por") == st.session_state.usuario]
    if mis_ordenes:
        seccion_label(f"MIS ÓRDENES CREADAS ({len(mis_ordenes)})")
        for o in reversed(mis_ordenes[-5:]):
            st.markdown(tarjeta_orden(o["serial"], o["cliente"], o["tipo"], o["estado"], dias_transcurridos(o)), unsafe_allow_html=True)


# ════════════════════════════════════
# MÓDULO 2 — PRODUCCIÓN
# ════════════════════════════════════
elif menu == "🏭 Producción":
    header_modulo("🏭", "PRODUCCIÓN", "Órdenes activas · Las despachadas pasan a Trazabilidad")

    ordenes = st.session_state.ordenes
    activas = [o for o in ordenes if o["estado"] != "Despacho"]

    if not ordenes:
        st.warning("No hay órdenes registradas todavía.")
        st.stop()
    if not activas:
        st.success("🎉 ¡Todo despachado! No hay órdenes pendientes.")
        st.info("Consulta el historial completo en **🔍 Trazabilidad**.")
        st.stop()

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_estado = st.selectbox("Estado", ["Todos"] + [e for e in ESTADOS if e != "Despacho"])
    with col_f2:
        filtro_tipo = st.selectbox("Tipo", ["Todos"] + TIPOS)
    with col_f3:
        buscar_prod = st.text_input("Buscar", placeholder="Cliente o serial...")

    lista = activas
    if filtro_estado != "Todos": lista = [o for o in lista if o["estado"] == filtro_estado]
    if filtro_tipo   != "Todos": lista = [o for o in lista if o["tipo"]   == filtro_tipo]
    if buscar_prod:
        lista = [o for o in lista if buscar_prod.lower() in o["cliente"].lower() or buscar_prod.upper() in o["serial"]]

    seccion_label(f"{len(lista)} ORDEN(ES) ENCONTRADA(S)")

    for orden in lista:
        idx  = st.session_state.ordenes.index(orden)
        dias = dias_transcurridos(orden)
        c    = COLORES_ESTADO.get(orden["estado"], "#6b7280")

        if isinstance(dias, int) and dias > orden["tiempo"]:
            st.markdown(f"""<div style="background:#ff475715;border:1px solid #ff475740;border-left:3px solid #ff4757;
                border-radius:4px;padding:9px 16px;margin-bottom:8px;
                font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#ff4757;">
                🚨 {orden['serial']} — {dias} días / pactado: {orden['tiempo']} días</div>""",
                unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#141720;border:1px solid #2a2f3e;border-left:3px solid {c};
                    border-radius:6px;padding:16px 20px;margin-bottom:4px;
                    box-shadow:0 4px 20px #00000050;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                <div>
                    <span style="font-family:'Share Tech Mono',monospace;color:{c};font-size:0.95rem;font-weight:700;">{orden['serial']}</span>
                    <span style="color:#3a3f50;margin:0 8px;">·</span>
                    <span style="color:#e8eaf0;font-weight:600;">{orden['cliente']}</span>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
                    {badge(orden['tipo'],"#6b7280")}&nbsp;{badge(orden['estado'],c)}
                    <span style="color:#6b7280;font-size:0.7rem;font-family:'Share Tech Mono',monospace;">⏱ {dias}d</span>
                </div>
            </div>
            <div style="color:#6b7280;font-size:0.75rem;margin-top:5px;font-family:'Share Tech Mono',monospace;">
                {orden['desc']} · {get_fecha(orden)[:10]}</div>
        </div>""", unsafe_allow_html=True)

        if orden.get("imagen"):
            import base64
            from io import BytesIO
            try:
                data = base64.b64decode(orden["imagen"].split(",")[1])
                col_img, _ = st.columns([1, 6])
                col_img.image(BytesIO(data), width=90)
            except: pass

        checklist_visual(orden)

        col_sel, col_nota = st.columns([2, 3])
        with col_sel:
            nuevo_estado = st.selectbox("Actualizar estado", ESTADOS,
                index=ESTADOS.index(orden["estado"]), key=f"sel_{orden['serial']}")
        with col_nota:
            nota = st.text_input("Nota del cambio", key=f"nota_{orden['serial']}",
                placeholder="Opcional: describe qué se hizo...")

        if nuevo_estado == "Despacho" and orden["estado"] != "Despacho":
            st.markdown("""<div style="background:#ffd16615;border:1px solid #ffd16640;
                border-left:3px solid #ffd166;border-radius:4px;padding:9px 16px;margin:8px 0;
                font-size:0.78rem;color:#ffd166;font-family:'Share Tech Mono',monospace;">
                ⚠ Al marcar DESPACHO esta orden saldrá de Producción y pasará a Trazabilidad.</div>""",
                unsafe_allow_html=True)

        if nuevo_estado != orden["estado"]:
            ahora = datetime.now().isoformat()
            st.session_state.ordenes[idx]["historial"].append({
                "estado": nuevo_estado, "fecha": ahora,
                "nota": nota.strip() or f"Cambio a {nuevo_estado}",
                "actualizado_por": st.session_state.usuario
            })
            st.session_state.ordenes[idx]["estado"] = nuevo_estado
            guardar(st.session_state.ordenes)
            st.rerun()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cantidad", f"{orden['cantidad']} unid.")
        m2.metric("Precio",   f"${orden['precio']:.2f}")
        m3.metric("Total",    f"${orden['cantidad'] * orden['precio']:,.2f}")
        m4.metric("Entrega",  f"{orden['tiempo']} días")

        if orden.get("specs"):
            with st.expander("📋 Especificaciones técnicas"):
                st.markdown(f'<span style="color:#9ca3af;font-size:0.88rem;">{orden["specs"]}</span>', unsafe_allow_html=True)

        with st.expander(f"🕐 Historial — {len(orden['historial'])} eventos"):
            historial_html(orden["historial"])

        st.markdown("<hr style='border-color:#1e2230;margin:20px 0;'>", unsafe_allow_html=True)


# ════════════════════════════════════
# MÓDULO 3 — DASHBOARD
# ════════════════════════════════════
elif menu == "📊 Dashboard":
    header_modulo("📊", "DASHBOARD", f"Tiempo real · {datetime.now().strftime('%d/%m/%Y %H:%M')} · ISO 9001:2015")

    ordenes = st.session_state.ordenes
    if not ordenes:
        st.info("Aún no hay órdenes registradas.")
        st.stop()

    cols = st.columns(len(ESTADOS) + 1)
    cols[0].metric("📦 Total", len(ordenes))
    for i, estado in enumerate(ESTADOS):
        cols[i+1].metric(f"{ICONOS[estado]} {estado}", sum(1 for o in ordenes if o["estado"] == estado))

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        seccion_label("POR TIPO DE PRODUCTO")
        ct = {"Textil": "#ff6b1a", "Impresión": "#00d4aa", "Promocional": "#a78bfa"}
        for tipo in TIPOS:
            n   = sum(1 for o in ordenes if o["tipo"] == tipo)
            pct = int(n / len(ordenes) * 100) if ordenes else 0
            c   = ct[tipo]
            st.markdown(f"""
            <div style="background:#141720;border:1px solid #2a2f3e;border-radius:4px;
                        padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
                    <span style="color:#e8eaf0;font-weight:600;">{tipo}</span>
                    <span style="color:{c};font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.1rem;">
                        {n} <span style="font-size:0.72rem;color:#6b7280;">orden(es)</span></span>
                </div>
                <div style="background:#2a2f3e;border-radius:2px;height:5px;">
                    <div style="width:{pct}%;background:linear-gradient(90deg,{c},{c}77);height:5px;border-radius:2px;"></div>
                </div>
                <div style="color:#6b7280;font-size:0.62rem;font-family:'Share Tech Mono',monospace;margin-top:3px;">{pct}%</div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        seccion_label("VALOR ACUMULADO")
        total_val    = sum(o["cantidad"] * o["precio"] for o in ordenes)
        despachado   = sum(o["cantidad"] * o["precio"] for o in ordenes if o["estado"] == "Despacho")
        en_proceso_v = total_val - despachado
        for label, valor, color in [("💰 Total en órdenes", total_val, "#e8eaf0"),
                                     ("🚚 Valor despachado",   despachado,   "#00d4aa"),
                                     ("🏭 Valor en proceso",   en_proceso_v, "#ff6b1a")]:
            st.markdown(f"""
            <div style="background:#141720;border:1px solid #2a2f3e;border-left:3px solid {color};
                        border-radius:4px;padding:14px 18px;margin-bottom:8px;">
                <div style="color:#6b7280;font-size:0.65rem;font-family:'Share Tech Mono',monospace;
                            letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">{label}</div>
                <div style="color:{color};font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.5rem;">
                    ${valor:,.2f}</div>
            </div>""", unsafe_allow_html=True)

    vencidas = [(o, dias_transcurridos(o)) for o in ordenes
                if o["estado"] != "Despacho" and isinstance(dias_transcurridos(o), int) and dias_transcurridos(o) > o["tiempo"]]
    if vencidas:
        seccion_label(f"🚨 ÓRDENES FUERA DE TIEMPO ({len(vencidas)})", "#ff4757")
        for o, dias in vencidas:
            st.markdown(f"""<div style="background:#ff475710;border:1px solid #ff475740;border-left:3px solid #ff4757;
                border-radius:4px;padding:9px 16px;margin-bottom:5px;
                font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#ff4757;">
                {o['serial']} · {o['cliente']} · {dias}d / pactado {o['tiempo']}d · {o['estado']}</div>""",
                unsafe_allow_html=True)

    seccion_label("PROGRESO POR ETAPA")
    cp = {"Recibido":"#6b7280","En Proceso":"#ff6b1a","Control Calidad":"#a78bfa","Terminación":"#00d4aa","Despacho":"#ffd166"}
    for estado in ESTADOS:
        n   = sum(1 for o in ordenes if o["estado"] == estado)
        pct = int(n / len(ordenes) * 100) if ordenes else 0
        c   = cp[estado]
        st.markdown(f"""<div style="margin-bottom:7px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="color:#9ca3af;font-size:0.78rem;">{ICONOS[estado]} {estado}</span>
                <span style="color:{c};font-family:'Share Tech Mono',monospace;font-size:0.72rem;">{n} ({pct}%)</span>
            </div>
            <div style="background:#2a2f3e;border-radius:2px;height:6px;">
                <div style="width:{pct}%;background:{c};height:6px;border-radius:2px;"></div>
            </div></div>""", unsafe_allow_html=True)

    seccion_label("ÚLTIMAS 6 ÓRDENES")
    for o in list(reversed(ordenes))[:6]:
        st.markdown(tarjeta_orden(o["serial"], o["cliente"], o["tipo"], o["estado"], dias_transcurridos(o)), unsafe_allow_html=True)


# ════════════════════════════════════
# MÓDULO 4 — TRAZABILIDAD
# ════════════════════════════════════
elif menu == "🔍 Trazabilidad":
    header_modulo("🔍", "TRAZABILIDAD", "Historial completo de todas las órdenes · ISO 9001:2015")

    ordenes     = st.session_state.ordenes
    despachadas = [o for o in ordenes if o["estado"] == "Despacho"]

    if despachadas:
        seccion_label(f"🚚 ÓRDENES DESPACHADAS ({len(despachadas)})", "#ffd166")
        for orden in reversed(despachadas):
            with st.expander(f"✅  {orden['serial']}  ·  {orden['cliente']}  ·  {orden['tipo']}  ·  {get_fecha(orden)[:10]}"):
                checklist_visual(orden)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Cantidad",       f"{orden['cantidad']} unid.")
                m2.metric("Total",          f"${orden['cantidad'] * orden['precio']:,.2f}")
                m3.metric("Tiempo pactado", f"{orden['tiempo']} días")
                m4.metric("Días reales",    f"{dias_transcurridos(orden)}")
                if orden.get("specs"):
                    st.markdown(f'<span style="color:#6b7280;font-size:0.8rem;font-family:\'Share Tech Mono\',monospace;">SPECS · {orden["specs"]}</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                historial_html(orden["historial"])
        st.markdown("<hr style='border-color:#1e2230;margin:20px 0;'>", unsafe_allow_html=True)

    seccion_label("BUSCAR ORDEN")
    buscar = st.text_input("Buscar", placeholder="Serial o nombre del cliente...")
    if buscar:
        resultados = [o for o in ordenes
                      if buscar.upper() in o["serial"].upper() or buscar.lower() in o["cliente"].lower()]
        if not resultados:
            st.warning("No se encontró ninguna orden.")
        else:
            st.markdown(f'<span style="color:#6b7280;font-size:0.7rem;font-family:\'Share Tech Mono\',monospace;">{len(resultados)} resultado(s)</span>', unsafe_allow_html=True)
            for orden in resultados:
                c = COLORES_ESTADO.get(orden["estado"], "#6b7280")
                st.markdown(f"""<div style="background:#141720;border:1px solid #2a2f3e;border-left:3px solid {c};
                    border-radius:6px;padding:14px 18px;margin:10px 0;box-shadow:0 4px 20px #00000050;">
                    <span style="font-family:'Share Tech Mono',monospace;color:{c};font-size:0.9rem;font-weight:700;">{orden['serial']}</span>
                    <span style="color:#3a3f50;margin:0 8px;">·</span>
                    <span style="color:#e8eaf0;font-weight:600;">{orden['cliente']}</span>
                    <span style="color:#3a3f50;margin:0 8px;">·</span>
                    <span style="color:#9ca3af;font-size:0.85rem;">{orden['tipo']}</span>
                </div>""", unsafe_allow_html=True)
                checklist_visual(orden)
                historial_html(orden["historial"])
                st.markdown("<hr style='border-color:#1e2230;margin:12px 0;'>", unsafe_allow_html=True)

    seccion_label("LOG COMPLETO DE ACTIVIDAD")
    eventos = []
    for o in ordenes:
        for h in o.get("historial", []):
            eventos.append({"serial": o["serial"], "tipo": o["tipo"], "cliente": o["cliente"], **h})
    eventos.sort(key=lambda x: x.get("fecha", ""), reverse=True)

    if not eventos:
        st.info("Sin actividad registrada aún.")
    else:
        lineas = ""
        cp2 = {"Recibido":"#6b7280","En Proceso":"#ff6b1a","Control Calidad":"#a78bfa","Terminación":"#00d4aa","Despacho":"#ffd166"}
        for ev in eventos[:40]:
            fecha_ev = (ev.get("fecha") or "—")[:16].replace("T", " ")
            quien    = f" <span style='color:#ff6b1a;'>{ev['actualizado_por']}</span>" if ev.get("actualizado_por") else ""
            c2       = cp2.get(ev.get("estado",""), "#6b7280")
            lineas  += f"""<div style="border-bottom:1px solid #1a1e2a;padding:6px 0;
                font-family:'Share Tech Mono',monospace;font-size:0.7rem;
                display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
                <span style="color:{c2};">{ICONOS.get(ev.get('estado',''),'●')}</span>
                <span style="color:#9ca3af;font-weight:600;min-width:110px;">{ev['serial']}</span>
                <span style="color:#6b7280;min-width:130px;">{ev['cliente']}</span>
                <span style="color:{c2};">{ev.get('estado','')}</span>
                {quien}
                <span style="color:#3a3f50;margin-left:auto;">{fecha_ev}</span>
            </div>"""
        st.markdown(f'<div style="background:#0a0c10;border:1px solid #1e2230;border-radius:6px;padding:14px 18px;">{lineas}</div>', unsafe_allow_html=True)