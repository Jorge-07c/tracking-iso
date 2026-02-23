import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="TrackISO", page_icon="⚙️", layout="wide")

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
ICONOS  = {
    "Recibido": "📥", "En Proceso": "⚙️",
    "Control Calidad": "🔬", "Terminación": "✅", "Despacho": "🚚"
}

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

# ── Inicializar session state ──
for key, default in [("usuario", None), ("rol", None), ("ordenes", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.ordenes is None:
    st.session_state.ordenes = cargar()


# ════════════════════════════════════
# PANTALLA DE LOGIN
# ════════════════════════════════════
if st.session_state.usuario is None:

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("⚙️ TrackISO")
        st.caption("Sistema Interno de Órdenes — ISO 9001:2015")
        st.divider()

        st.subheader("Iniciar sesión")
        usuario_input  = st.text_input("Usuario", placeholder="Ingresa tu usuario")
        password_input = st.text_input("Contraseña", type="password", placeholder="••••••••")

        if st.button("🔓 Entrar", use_container_width=True):
            u = USUARIOS.get(usuario_input)
            if u and u["password"] == password_input:
                st.session_state.usuario = usuario_input
                st.session_state.rol     = u["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

        st.divider()
        st.caption("💡 Usuarios de prueba para la presentación:")
        st.code(
            "admin / admin123      → Administrador (acceso total)\n"
            "ventas / ventas123   → Cotización + Dashboard + Trazabilidad\n"
            "produccion / prod123 → Producción + Dashboard + Trazabilidad",
            language="text"
        )

    st.stop()


# ════════════════════════════════════
# FUNCIONES HELPER
# ════════════════════════════════════
def generar_serial(tipo):
    prefijo = {"Textil": "TEX", "Impresión": "IMP", "Promocional": "PRO"}[tipo]
    return f"{prefijo}-{datetime.now().year}-{str(uuid.uuid4())[:4].upper()}"

def get_fecha(orden):
    return orden.get("fecha") or orden.get("fecha_creacion") or "—"

def mostrar_checklist(orden):
    st.markdown("**Etapas de producción:**")
    cols = st.columns(len(ESTADOS))
    idx_estado = ESTADOS.index(orden["estado"])
    for j, (col, etapa) in enumerate(zip(cols, ESTADOS)):
        if j < idx_estado:
            col.success(f"✓ {etapa}")
        elif j == idx_estado:
            col.warning(f"{ICONOS[etapa]} {etapa}")
        else:
            col.info(f"○ {etapa}")

def dias_transcurridos(orden):
    try:
        creado = datetime.fromisoformat(get_fecha(orden))
        return (datetime.now() - creado).days
    except:
        return "—"


# ════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════
rol_actual       = st.session_state.rol
modulos_visibles = ACCESOS[rol_actual]

with st.sidebar:
    st.title("⚙️ TrackISO")
    st.caption("ISO 9001:2015")
    st.divider()

    # Info del usuario con badge de rol
    st.markdown(f"👤 **{st.session_state.usuario}**")
    st.caption(f"Rol: {rol_actual}")
    st.divider()

    menu = st.radio("Navegación", modulos_visibles, label_visibility="collapsed")
    st.divider()

    # Estadísticas rápidas
    _todas       = st.session_state.ordenes
    _activas     = sum(1 for o in _todas if o["estado"] != "Despacho")
    _despachadas = sum(1 for o in _todas if o["estado"] == "Despacho")

    st.metric("📦 Total", len(_todas))
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("🏭 Activas",    _activas)
    col_s2.metric("🚚 Despach.",   _despachadas)

    st.divider()

    # ── CERRAR SESIÓN ──
    if st.button("🚪 Cerrar sesión", use_container_width=True, type="secondary"):
        st.session_state.usuario = None
        st.session_state.rol     = None
        st.rerun()


# ════════════════════════════════════
# MÓDULO 1 — COTIZACIÓN
# ════════════════════════════════════
if menu == "📋 Cotización":
    st.title("📋 Nueva Cotización")
    st.caption("Ventas → genera la orden de producción")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        cliente  = st.text_input("Cliente / Empresa")
        tipo     = st.selectbox("Tipo de producto", TIPOS)
        desc     = st.text_input("Descripción del producto")
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, value=1)
        precio   = st.number_input("Precio unitario ($)", min_value=0.0, step=0.01)
        tiempo   = st.number_input("Tiempo estimado (días)", min_value=1, value=7)

    specs  = st.text_area("Especificaciones técnicas", placeholder="Colores, materiales, medidas...")
    imagen = st.file_uploader("Imagen del producto", type=["png", "jpg", "jpeg"])

    if imagen:
        st.image(imagen, width=200, caption="Vista previa del producto")

    st.divider()

    # Preview en tiempo real
    st.subheader("📄 Preview de cotización")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cliente",        cliente or "—")
    c2.metric("Cantidad",       f"{cantidad} unid.")
    c3.metric("Precio unitario", f"${precio:.2f}")
    c4.metric("Total estimado", f"${cantidad * precio:.2f}")

    st.divider()

    if st.button("✅ Generar Orden de Producción", use_container_width=True, type="primary"):
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

            nueva = {
                "serial":     serial,
                "cliente":    cliente.strip(),
                "tipo":       tipo,
                "desc":       desc.strip(),
                "cantidad":   cantidad,
                "precio":     precio,
                "tiempo":     tiempo,
                "specs":      specs.strip(),
                "imagen":     img_b64,
                "estado":     "Recibido",
                "fecha":      ahora,
                "creado_por": st.session_state.usuario,
                "historial":  [{"estado": "Recibido", "fecha": ahora,
                                "nota": f"Orden creada por {st.session_state.usuario}",
                                "actualizado_por": st.session_state.usuario}]
            }

            st.session_state.ordenes.append(nueva)
            guardar(st.session_state.ordenes)
            st.success(f"✅ Orden **{serial}** generada y enviada a Producción.")
            st.balloons()

    # Mis órdenes creadas (solo las del usuario actual si no es admin)
    st.divider()
    mis_ordenes = [o for o in st.session_state.ordenes if o.get("creado_por") == st.session_state.usuario]
    if mis_ordenes:
        st.subheader(f"📋 Mis órdenes creadas ({len(mis_ordenes)})")
        for o in reversed(mis_ordenes[-5:]):
            dias = dias_transcurridos(o)
            st.markdown(
                f"- **{o['serial']}** · {o['cliente']} · `{o['tipo']}` · "
                f"{ICONOS[o['estado']]} {o['estado']} · *hace {dias} día(s)*"
            )


# ════════════════════════════════════
# MÓDULO 2 — PRODUCCIÓN
# ════════════════════════════════════
elif menu == "🏭 Producción":
    st.title("🏭 Departamento de Producción")
    st.caption("Órdenes activas. Las despachadas quedan registradas en Trazabilidad.")
    st.divider()

    ordenes = st.session_state.ordenes
    activas = [o for o in ordenes if o["estado"] != "Despacho"]

    if not ordenes:
        st.warning("No hay órdenes registradas todavía.")
        st.stop()

    if not activas:
        st.success("🎉 ¡Todo despachado! No hay órdenes pendientes.")
        st.info("Consulta el historial completo en **🔍 Trazabilidad**.")
        st.stop()

    # Filtros en columnas
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        estados_activos = [e for e in ESTADOS if e != "Despacho"]
        filtro_estado = st.selectbox("Filtrar por estado", ["Todos"] + estados_activos)
    with col_f2:
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + TIPOS)
    with col_f3:
        buscar_prod = st.text_input("Buscar cliente o serial", placeholder="Buscar...")

    # Aplicar filtros
    lista = activas
    if filtro_estado != "Todos":
        lista = [o for o in lista if o["estado"] == filtro_estado]
    if filtro_tipo != "Todos":
        lista = [o for o in lista if o["tipo"] == filtro_tipo]
    if buscar_prod:
        lista = [o for o in lista if
                 buscar_prod.lower() in o["cliente"].lower() or
                 buscar_prod.upper() in o["serial"]]

    st.caption(f"{len(lista)} orden(es) encontrada(s) · {_despachadas} despachada(s)")
    st.divider()

    for orden in lista:
        idx = st.session_state.ordenes.index(orden)
        dias = dias_transcurridos(orden)

        # Alerta si lleva más días del tiempo pactado
        if isinstance(dias, int) and dias > orden["tiempo"]:
            st.error(f"🚨 **{orden['serial']}** lleva {dias} días — supera el tiempo pactado de {orden['tiempo']} días.")

        st.subheader(f"🔖 {orden['serial']}  |  {orden['cliente']}")
        st.caption(
            f"Tipo: {orden['tipo']} · {orden['desc']} · "
            f"Creado: {get_fecha(orden)[:10]} · Días transcurridos: {dias}"
        )

        if orden.get("imagen"):
            import base64
            from io import BytesIO
            try:
                data = base64.b64decode(orden["imagen"].split(",")[1])
                st.image(BytesIO(data), width=130)
            except:
                pass

        mostrar_checklist(orden)

        col_sel, col_nota = st.columns([2, 3])
        with col_sel:
            nuevo_estado = st.selectbox(
                "Actualizar estado",
                ESTADOS,
                index=ESTADOS.index(orden["estado"]),
                key=f"sel_{orden['serial']}"
            )
        with col_nota:
            nota = st.text_input(
                "Nota del cambio",
                key=f"nota_{orden['serial']}",
                placeholder="Opcional: describe qué se hizo..."
            )

        if nuevo_estado == "Despacho" and orden["estado"] != "Despacho":
            st.warning("⚠️ Al marcar **Despacho**, esta orden saldrá de producción y pasará solo a Trazabilidad.")

        if nuevo_estado != orden["estado"]:
            ahora = datetime.now().isoformat()
            st.session_state.ordenes[idx]["historial"].append({
                "estado":          nuevo_estado,
                "fecha":           ahora,
                "nota":            nota.strip() or f"Cambio a {nuevo_estado}",
                "actualizado_por": st.session_state.usuario
            })
            st.session_state.ordenes[idx]["estado"] = nuevo_estado
            guardar(st.session_state.ordenes)
            st.rerun()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cantidad",  f"{orden['cantidad']} unid.")
        m2.metric("Precio",    f"${orden['precio']:.2f}")
        m3.metric("Total",     f"${orden['cantidad'] * orden['precio']:.2f}")
        m4.metric("Entrega",   f"{orden['tiempo']} días")

        if orden.get("specs"):
            with st.expander("📋 Ver especificaciones técnicas"):
                st.write(orden["specs"])

        with st.expander(f"🕐 Historial ({len(orden['historial'])} eventos)"):
            for h in reversed(orden["historial"]):
                quien = f" · por **{h['actualizado_por']}**" if h.get("actualizado_por") else ""
                st.markdown(
                    f"{ICONOS.get(h['estado'], '●')} **{h['estado']}** "
                    f"— {h['fecha'][:16].replace('T', ' ')}{quien}  \n"
                    f"_{h.get('nota', '')}_"
                )

        st.divider()


# ════════════════════════════════════
# MÓDULO 3 — DASHBOARD
# ════════════════════════════════════
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard General")
    st.caption(f"Resumen en tiempo real — {datetime.now().strftime('%d/%m/%Y %H:%M')} — ISO 9001:2015")
    st.divider()

    ordenes = st.session_state.ordenes

    if not ordenes:
        st.info("Aún no hay órdenes registradas.")
        st.stop()

    # Fila de métricas principales
    cols = st.columns(len(ESTADOS) + 1)
    cols[0].metric("📦 Total", len(ordenes))
    for i, estado in enumerate(ESTADOS):
        n = sum(1 for o in ordenes if o["estado"] == estado)
        cols[i + 1].metric(f"{ICONOS[estado]} {estado}", n)

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Por tipo de producto")
        for tipo in TIPOS:
            n   = sum(1 for o in ordenes if o["tipo"] == tipo)
            pct = int(n / len(ordenes) * 100) if ordenes else 0
            st.metric(tipo, f"{n} orden(es)")
            st.progress(pct / 100)

    with col_b:
        st.subheader("Valor total acumulado")
        total_val    = sum(o["cantidad"] * o["precio"] for o in ordenes)
        despachado   = sum(o["cantidad"] * o["precio"] for o in ordenes if o["estado"] == "Despacho")
        en_proceso_v = total_val - despachado

        st.metric("💰 Total en órdenes",   f"${total_val:,.2f}")
        st.metric("🚚 Valor despachado",   f"${despachado:,.2f}")
        st.metric("🏭 Valor en proceso",   f"${en_proceso_v:,.2f}")

    st.divider()

    # Órdenes con alerta de tiempo
    vencidas = []
    for o in ordenes:
        if o["estado"] == "Despacho":
            continue
        dias = dias_transcurridos(o)
        if isinstance(dias, int) and dias > o["tiempo"]:
            vencidas.append((o, dias))

    if vencidas:
        st.subheader(f"🚨 Órdenes fuera de tiempo ({len(vencidas)})")
        for o, dias in vencidas:
            st.error(f"**{o['serial']}** · {o['cliente']} · lleva {dias} días (pactado: {o['tiempo']} días) · Estado: {o['estado']}")
        st.divider()

    st.subheader("Progreso por etapa")
    for estado in ESTADOS:
        n   = sum(1 for o in ordenes if o["estado"] == estado)
        pct = int(n / len(ordenes) * 100) if ordenes else 0
        st.progress(pct / 100, text=f"{ICONOS[estado]} {estado}: {n} orden(es) ({pct}%)")

    st.divider()
    st.subheader("Últimas 6 órdenes registradas")
    for o in list(reversed(ordenes))[:6]:
        dias    = dias_transcurridos(o)
        creador = f"creado por *{o['creado_por']}*" if o.get("creado_por") else ""
        st.markdown(
            f"- **{o['serial']}** · {o['cliente']} · `{o['tipo']}` · "
            f"{ICONOS[o['estado']]} {o['estado']} · {creador} · *{dias} día(s)*"
        )


# ════════════════════════════════════
# MÓDULO 4 — TRAZABILIDAD
# ════════════════════════════════════
elif menu == "🔍 Trazabilidad":
    st.title("🔍 Trazabilidad")
    st.caption("Historial completo de todas las órdenes — ISO 9001:2015")
    st.divider()

    ordenes     = st.session_state.ordenes
    despachadas = [o for o in ordenes if o["estado"] == "Despacho"]

    # Órdenes despachadas
    if despachadas:
        st.subheader(f"🚚 Órdenes Despachadas ({len(despachadas)})")
        st.caption("Proceso completado. Solo lectura.")

        for orden in reversed(despachadas):
            label = f"✅ {orden['serial']}  |  {orden['cliente']}  |  {orden['tipo']}  —  {get_fecha(orden)[:10]}"
            with st.expander(label):
                mostrar_checklist(orden)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Cantidad",       f"{orden['cantidad']} unid.")
                m2.metric("Total",          f"${orden['cantidad'] * orden['precio']:.2f}")
                m3.metric("Tiempo pactado", f"{orden['tiempo']} días")
                m4.metric("Días reales",    f"{dias_transcurridos(orden)}")

                if orden.get("specs"):
                    st.markdown(f"**Especificaciones:** {orden['specs']}")

                st.markdown("**Historial:**")
                for h in reversed(orden["historial"]):
                    quien = f" · por **{h['actualizado_por']}**" if h.get("actualizado_por") else ""
                    st.markdown(
                        f"- {ICONOS.get(h['estado'], '●')} **{h['estado']}** "
                        f"— {h['fecha'][:16].replace('T', ' ')}{quien} — _{h.get('nota', '')}_"
                    )

        st.divider()

    # Buscar serial
    st.subheader("🔎 Buscar orden por serial o cliente")
    buscar = st.text_input("Buscar", placeholder="Ej: TEX-2025-A1B2 o nombre del cliente")

    if buscar:
        resultados = [
            o for o in ordenes
            if buscar.upper() in o["serial"].upper() or buscar.lower() in o["cliente"].lower()
        ]
        if not resultados:
            st.warning("No se encontró ninguna orden.")
        else:
            st.caption(f"{len(resultados)} resultado(s)")
            for orden in resultados:
                st.subheader(f"🔖 {orden['serial']}")
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Cliente:** {orden['cliente']}")
                c2.write(f"**Tipo:** {orden['tipo']}")
                c3.write(f"**Estado:** {ICONOS[orden['estado']]} {orden['estado']}")

                mostrar_checklist(orden)

                st.markdown("**Historial completo:**")
                for h in reversed(orden["historial"]):
                    quien = f" · por **{h['actualizado_por']}**" if h.get("actualizado_por") else ""
                    st.markdown(
                        f"- {ICONOS.get(h['estado'], '●')} **{h['estado']}** "
                        f"— {h['fecha'][:16].replace('T', ' ')}{quien} — _{h.get('nota', '')}_"
                    )
                st.divider()

    # Log completo
    st.subheader("📜 Log completo de actividad")
    eventos = []
    for o in ordenes:
        for h in o.get("historial", []):
            eventos.append({"serial": o["serial"], "tipo": o["tipo"], "cliente": o["cliente"], **h})

    eventos.sort(key=lambda x: x.get("fecha", ""), reverse=True)

    if not eventos:
        st.info("Sin actividad registrada aún.")
    else:
        for ev in eventos[:40]:
            fecha_ev = (ev.get("fecha") or "—")[:16].replace("T", " ")
            quien    = f" · **{ev['actualizado_por']}**" if ev.get("actualizado_por") else ""
            st.markdown(
                f"- `{ev['serial']}` · {ev['cliente']} · "
                f"{ICONOS.get(ev['estado'], '●')} {ev['estado']}{quien} · {fecha_ev}"
            )
