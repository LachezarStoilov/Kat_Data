import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os
import glob
import base64

# ====================================================================================
# AUTO MARKET INTELLIGENCE BG - FINAL VERSION
# ====================================================================================

st.set_page_config(page_title="Анализ пазар България", page_icon="🏎️", layout="wide")

# ----------------------------------------------------------------------------------
# 0. ПРЕМИУМ ДИЗАЙН & ЛОГО
# ----------------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .hero { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; }
    .hero-title { font-size: 1.8rem; font-weight: 800; color: #FFFFFF; margin: 0; }
    .hero-sub { font-size: 0.9rem; color: #94a3b8; font-weight: 400; }
    .kpi-card { background: #FFFFFF; border-radius: 10px; padding: 1rem; border-top: 4px solid #3B82F6; box-shadow: 0 2px 5px rgba(0,0,0,0.05); min-height: 92px; }
    .kpi-label { font-size: 0.75rem; color:#64748b; font-weight:700; text-transform:uppercase; }
    .kpi-value { font-size: 1.6rem; font-weight:800; color:#0f172a; }
    .kpi-sub { font-size: 0.78rem; font-weight:600; margin-top:3px; }
    .section-title { font-size: 1.3rem; font-weight: 800; color:#1e293b; margin: 1rem 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 5px;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def kpi_card(col, label, value, sub=None, sub_color="#64748b", accent="#3B82F6"):
    sub_html = f'<div class="kpi-sub" style="color:{sub_color};">{sub}</div>' if sub else ""
    col.markdown(
        f'<div class="kpi-card" style="border-top-color:{accent};">'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True
    )

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

img_b64 = get_base64_image("logo.png")

# Ако логото не е намерено, се скрива елегантно
img_html = f'<img src="data:image/png;base64,{img_b64}" width="85" height="85" style="flex-shrink:0; border-radius: 10px; object-fit: contain;">' if img_b64 else ''

st.markdown(f"""
    <div class="hero" style="display:flex; align-items:center; gap:18px;">
        {img_html}
        <div>
            <div class="hero-title">AUTO MOTO SALES BG </div>
            <div class="hero-sub">Анализ на пазара на МПС в България </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# 1. ОБРАБОТКА И ХИГИЕНА НА ДАННИТЕ
# ----------------------------------------------------------------------------------
VEHICLE_CATEGORIES = {
    "Леки автомобили (M1)": ["M1"],
    "Лекотоварни (N1)": ["N1"],
    "Товарни (N2, N3)": ["N2", "N3"],
    "Автобуси (M2, M3)": ["M2", "M3"],
    "Мотоциклети и АТВ (L)": ["L1", "L2", "L3", "L4", "L5", "L6", "L7"],
    "Всички останали": ["O1", "O2", "O3", "O4", "T", "OT"]
}

SUMMARY_ROW_PATTERN = r"ОБЩ|ВСИЧК|TOTAL|SUM"

@st.cache_data(show_spinner=False)
def load_and_process(file_bytes_list, file_names):
    parsed_files = []
    for content, name in zip(file_bytes_list, file_names):
        match = re.search(r'(\d{1,2})[_.-](\d{4})', name)
        if not match: continue
        month, year = int(match.group(1)), int(match.group(2))
        try:
            try: df = pd.read_csv(pd.io.common.BytesIO(content), encoding="utf-8")
            except: df = pd.read_csv(pd.io.common.BytesIO(content), encoding="cp1251")
            df.columns = [c.strip() for c in df.columns]
            parsed_files.append({"year": year, "month": month, "period_str": f"{month:02d}.{year}", "sort_index": year * 100 + month, "df": df})
        except: continue

    if not parsed_files: return None
    parsed_files = sorted(parsed_files, key=lambda x: x["sort_index"])

    all_dfs = []
    for item in parsed_files:
        temp_df = item["df"].copy()
        temp_df["Година"], temp_df["Месец"], temp_df["Период"], temp_df["Sort_Index"] = item["year"], item["month"], item["period_str"], item["sort_index"]

        brand_col = [c for c in temp_df.columns if "МАРКА" in c.upper()][0]
        model_col = [c for c in temp_df.columns if "МОДЕЛ" in c.upper()][0]

        temp_df["Brand"] = temp_df[brand_col].fillna("НЕИЗВЕСТНА").astype(str).str.strip().str.upper()
        temp_df["_RawModel"] = temp_df[model_col].fillna("НЕИЗВЕСТЕН").astype(str).str.strip().str.upper()

        valid_mask = (
            (~temp_df["Brand"].str.contains(SUMMARY_ROW_PATTERN, case=False, na=False, regex=True)) &
            (~temp_df["_RawModel"].str.contains(SUMMARY_ROW_PATTERN, case=False, na=False, regex=True)) &
            (temp_df["Brand"].str.strip() != "")
        )
        temp_df = temp_df[valid_mask].copy()
        if temp_df.empty:
            continue

        def clean_model(b, m):
            return m[len(b):].strip() if m.startswith(b) and len(m) > len(b) else m
        temp_df["Model"] = [clean_model(b, m) for b, m in zip(temp_df["Brand"], temp_df["_RawModel"])]
        temp_df["Label"] = temp_df["Brand"] + " " + temp_df["Model"]
        temp_df.drop(columns=["_RawModel"], inplace=True)

        for cat_name, prefixes in VEHICLE_CATEGORIES.items():
            n_cols = [c for c in temp_df.columns if any(c.startswith(p) for p in prefixes) and 'нови' in c.lower() and 'общо' not in c.lower()]
            u_cols = [c for c in temp_df.columns if any(c.startswith(p) for p in prefixes) and 'употр' in c.lower() and 'общо' not in c.lower()]
            o_cols = [c for c in temp_df.columns if any(c.startswith(p) for p in prefixes) and 'други' in c.lower() and 'общо' not in c.lower()]

            temp_df[f"{cat_name}_Нови"] = temp_df[n_cols].sum(axis=1) if n_cols else 0
            temp_df[f"{cat_name}_Употр"] = temp_df[u_cols].sum(axis=1) if u_cols else 0
            temp_df[f"{cat_name}_Други"] = temp_df[o_cols].sum(axis=1) if o_cols else 0

        all_dfs.append(temp_df)

    if not all_dfs: return None
    raw_df = pd.concat(all_dfs, ignore_index=True)

    agg_cols = [c for c in raw_df.columns if "_Нови" in c or "_Употр" in c or "_Други" in c]
    agg_df = raw_df.groupby(["Sort_Index", "Година", "Месец", "Период", "Brand", "Model", "Label"], as_index=False)[agg_cols].sum()

    agg_df = agg_df.sort_values(by=["Sort_Index", "Brand", "Model"])
    for col in agg_cols:
        agg_df[f"{col}_Месец"] = agg_df.groupby(["Година", "Brand", "Model"])[col].diff().fillna(agg_df[col]).clip(lower=0)

    return agg_df

# Автоматично зареждане на данните от папка "data"
csv_files = glob.glob(os.path.join("data", "*.csv"))

if not csv_files:
    st.info("📂 Няма намерени CSV файлове в папка 'data'. Моля, добави ги.")
    st.stop()

file_bytes_list = []
file_names = []
for file_path in csv_files:
    with open(file_path, "rb") as f:
        file_bytes_list.append(f.read())
    file_names.append(os.path.basename(file_path))

with st.spinner("Хронологизиране и изчистване на данните..."):
    df_full = load_and_process(tuple(file_bytes_list), tuple(file_names))

if df_full is None or df_full.empty:
    st.error("Не успях да разпозная валидни данни в файловете.")
    st.stop()

# ----------------------------------------------------------------------------------
# 2. ГЛОБАЛНИ ФИЛТРИ (SIDEBAR)
# ----------------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Глобални филтри")

selected_cat = st.sidebar.selectbox("Вид превозно средство:", options=list(VEHICLE_CATEGORIES.keys()))

unique_periods = df_full[["Sort_Index", "Период"]].drop_duplicates().sort_values("Sort_Index")
p_opts = unique_periods["Sort_Index"].tolist()
p_lbls = unique_periods["Период"].tolist()

if len(p_opts) > 1:
    opts_2026 = [opt for opt in p_opts if str(opt).startswith("2026")]
    if opts_2026:
        default_start = opts_2026[0]
        default_end = opts_2026[-1]
    else:
        default_start = p_opts[0]
        default_end = p_opts[-1]

    start_idx, end_idx = st.sidebar.select_slider(
        "Времеви прозорец:", 
        options=p_opts, 
        value=(default_start, default_end), 
        format_func=lambda x: unique_periods[unique_periods["Sort_Index"]==x]["Период"].values[0]
    )
else:
    start_idx, end_idx = (p_opts[0], p_opts[0])

df_working = df_full[(df_full["Sort_Index"] >= start_idx) & (df_full["Sort_Index"] <= end_idx)].copy()
df_working["Нови"] = df_working[f"{selected_cat}_Нови_Месец"]
df_working["Употребявани"] = df_working[f"{selected_cat}_Употр_Месец"]
df_working["Пререгистрации"] = df_working[f"{selected_cat}_Други_Месец"]
df_working["Вторичен Пазар"] = df_working["Употребявани"] + df_working["Пререгистрации"]
df_working["Всички"] = df_working["Нови"] + df_working["Вторичен Пазар"]

start_period_str = unique_periods[unique_periods["Sort_Index"] == start_idx]["Период"].values[0]
end_period_str = unique_periods[unique_periods["Sort_Index"] == end_idx]["Период"].values[0]
period_label_full = f"{start_period_str} - {end_period_str}" if start_period_str != end_period_str else start_period_str

period_lookup = dict(zip(p_opts, p_lbls))
selected_sort_indices = sorted(df_working["Sort_Index"].unique().tolist())
prev_sort_indices = sorted([s - 100 for s in selected_sort_indices if (s - 100) in period_lookup])
has_prev_period = len(prev_sort_indices) > 0
is_partial_yoy = has_prev_period and (len(prev_sort_indices) < len(selected_sort_indices))

if has_prev_period:
    df_prev = df_full[df_full["Sort_Index"].isin(prev_sort_indices)].copy()
    df_prev["Нови"] = df_prev[f"{selected_cat}_Нови_Месец"]
    df_prev["Употребявани"] = df_prev[f"{selected_cat}_Употр_Месец"]
    df_prev["Пререгистрации"] = df_prev[f"{selected_cat}_Други_Месец"]
    df_prev["Вторичен Пазар"] = df_prev["Употребявани"] + df_prev["Пререгистрации"]
    prev_labels = [period_lookup[s] for s in prev_sort_indices]
    prev_period_label = f"{prev_labels[0]} - {prev_labels[-1]}" if len(prev_labels) > 1 else prev_labels[0]
else:
    df_prev = pd.DataFrame(columns=list(df_working.columns))
    prev_period_label = None

def pct_value(current, previous):
    if previous is None or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous * 100

def growth_badge(current, previous):
    if previous is None or pd.isna(previous) or previous == 0:
        return "🆕 Ново" if current > 0 else "—"
    pct = (current - previous) / previous * 100
    if pct > 0.5: return f"📈 +{pct:.1f}%"
    if pct < -0.5: return f"📉 {pct:.1f}%"
    return f"➡️ {pct:.1f}%"

def render_kpi_growth(col, label, current_total, prev_total, accent):
    growth_pct = pct_value(current_total, prev_total)
    if growth_pct is None:
        kpi_card(col, label, "—", sub="Няма данни за сравнение", accent="#94a3b8")
        return
    if growth_pct >= 0:
        kpi_card(col, label, f"+{growth_pct:.1f}%", sub=f"📈 спрямо {prev_period_label}", sub_color="#10B981", accent=accent)
    else:
        kpi_card(col, label, f"{growth_pct:.1f}%", sub=f"📉 спрямо {prev_period_label}", sub_color="#EF4444", accent=accent)

def fmt_num(x):
    return f"{x:,.0f}".replace(",", " ")

trend_df = df_working.groupby(["Sort_Index", "Период"])[["Нови", "Вторичен Пазар"]].sum().reset_index().sort_values("Sort_Index")

def render_trend_chart(key):
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend_df["Период"], y=trend_df["Нови"], name="Нови", mode="lines+markers",
                                    line=dict(color="#10B981", width=3, shape="spline"), marker=dict(size=7),
                                    fill="tozeroy", fillcolor="rgba(16,185,129,0.08)"))
    fig_trend.add_trace(go.Scatter(x=trend_df["Период"], y=trend_df["Вторичен Пазар"], name="Вторичен пазар", mode="lines+markers",
                                    line=dict(color="#3B82F6", width=3, shape="spline"), marker=dict(size=7),
                                    fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"))
    fig_trend.update_layout(title="Тренд: Нови vs Вторичен пазар по месеци", template="plotly_white", height=340,
                             hovermode="x unified", legend=dict(orientation="h", y=1.18, x=0), margin=dict(t=60))
    st.plotly_chart(fig_trend, use_container_width=True, key=key)

# ----------------------------------------------------------------------------------
# 3. ТАБОВЕ ЗА АНАЛИЗ
# ----------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🔍 Анализ по Модели", "✨ Пазар НОВИ МПС", "🤝 ВТОРИЧЕН пазар на МПС "])

# ==========================================
# ТАБ 1: DRILL-DOWN ПО МОДЕЛ (С МУЛТИСЕЛЕКТ)
# ==========================================
with tab1:
    st.markdown('<div class="section-title">Анализ и сравнение на конкретни модели във времето</div>', unsafe_allow_html=True)

    model_volumes = df_working.groupby(["Brand", "Label"])["Всички"].sum().reset_index()
    liquid_models = model_volumes[model_volumes["Всички"] >= 15]

    col_f1, col_f2 = st.columns([1, 2])

    available_brands = sorted(liquid_models["Brand"].unique())
    sel_brand = col_f1.selectbox("1. Филтрирай по марка (за по-лесно търсене):", options=["Всички марки"] + available_brands)

    if sel_brand == "Всички марки":
        available_labels = sorted(liquid_models["Label"].unique())
    else:
        available_labels = sorted(liquid_models[liquid_models["Brand"] == sel_brand]["Label"].unique())

    target_models = ["ШКОДА КОДИАК", "ФОЛКСВАГЕН ТАЙРОН", "ХЮНДАЙ САНТА ФЕ", "КИА СОРЕНТО"]
    def_models = [l for l in available_labels if any(t in l for t in target_models)]
    if not def_models and available_labels: def_models = [available_labels[0]]

    sel_models = col_f2.multiselect("2. Избери модели за сравнение (добави няколко):", options=available_labels, default=def_models)

    st.markdown("<br>", unsafe_allow_html=True)
    metric_tab1 = st.pills("Анализирана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Всички")

    if sel_models and metric_tab1:
        m_data = df_working[df_working["Label"].isin(sel_models)].sort_values("Sort_Index")

        fig = go.Figure()
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

        for i, model in enumerate(sel_models):
            model_df = m_data[m_data["Label"] == model]
            fig.add_trace(go.Scatter(
                x=model_df["Период"], y=model_df[metric_tab1], name=model, mode="lines+markers+text",
                text=model_df[metric_tab1], textposition="top center",
                line=dict(width=3, shape="spline", color=colors[i % len(colors)]), marker=dict(size=8)
            ))

        fig.update_layout(title=f"Динамика на продажбите: {metric_tab1}", template="plotly_white", height=420, hovermode="x unified", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ТАБ 2: ПАЗАР "НОВИ" АВТОМОБИЛИ
# ==========================================
with tab2:
    st.markdown(f'<div class="section-title">Лидери при НОВИТЕ автомобили (Данни за периода: {period_label_full})</div>', unsafe_allow_html=True)

    df_new_agg = df_working.groupby(["Brand", "Model"])["Нови"].sum().reset_index()
    total_new_market = df_new_agg["Нови"].sum()

    if total_new_market == 0:
        st.info(f"Няма регистрирани нови превозни средства за периода {period_label_full}.")
    else:
        brand_totals_new = df_new_agg.groupby("Brand")["Нови"].sum().sort_values(ascending=False)
        leader_brand, leader_units = brand_totals_new.index[0], brand_totals_new.iloc[0]
        prev_total_new = df_prev["Нови"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо нови регистрации", fmt_num(total_new_market), accent="#10B981")
        render_kpi_growth(k2, "Ръст спрямо предх. период", total_new_market, prev_total_new, accent="#10B981")
        kpi_card(k3, "Пазарен лидер", leader_brand, sub=f"{fmt_num(leader_units)} бр. ({leader_units/total_new_market:.1%})", accent="#10B981")
        kpi_card(k4, "Активни марки / модели", f"{df_new_agg['Brand'].nunique()} / {df_new_agg['Model'].nunique()}", accent="#10B981")

        st.markdown("<br>", unsafe_allow_html=True)
        render_trend_chart(key="trend_tab2")
        st.markdown("<br>", unsafe_allow_html=True)

        col_m1, col_m2 = st.columns([1, 1])

        top_brands_new = brand_totals_new.reset_index().head(15)
        fig_b_new = px.bar(top_brands_new.sort_values("Нови"), x="Нови", y="Brand", orientation="h", title="Топ 15 Марки (Нови)", text="Нови", color="Нови", color_continuous_scale="greens")
        fig_b_new.update_layout(coloraxis_showscale=False, height=420)
        col_m1.plotly_chart(fig_b_new, use_container_width=True)

        top_models_new = df_new_agg.sort_values("Нови", ascending=False).head(15).copy()
        top_models_new["Име"] = top_models_new["Brand"] + " " + top_models_new["Model"]
        fig_m_new = px.bar(top_models_new.sort_values("Нови"), x="Нови", y="Име", orientation="h", title="Топ 15 Най-продавани Модели (Нови)", text="Нови", color_discrete_sequence=["#10B981"])
        fig_m_new.update_layout(height=420)
        col_m2.plotly_chart(fig_m_new, use_container_width=True)

        pie_data_new = brand_totals_new.reset_index()
        if len(pie_data_new) > 30:
            others_sum = pie_data_new.iloc[30:]["Нови"].sum()
            pie_data_new = pie_data_new.head(30)
            if others_sum > 0:
                pie_data_new = pd.concat([pie_data_new, pd.DataFrame([{"Brand": "ДРУГИ", "Нови": others_sum}])], ignore_index=True)

        fig_pie_new = px.pie(pie_data_new, names="Brand", values="Нови", title="Пазарен дял по марки (Топ 30 + Други)", hole=0.45)
        fig_pie_new.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie_new.update_layout(height=560, showlegend=False)
        st.plotly_chart(fig_pie_new, use_container_width=True)

        st.markdown("##### 📋 Пълна пазарна справка (Нови)")
        market_table_new = df_new_agg[df_new_agg["Нови"] > 0].sort_values("Нови", ascending=False).copy()
        market_table_new["Пазарен Дял"] = (market_table_new["Нови"] / total_new_market) * 100

        col_config_new = {
            "Brand": "Марка", "Model": "Модел", "Нови": st.column_config.NumberColumn("Брой Продажби", format="%d"),
            "Пазарен Дял": st.column_config.ProgressColumn("Пазарен Дял %", format="%.2f%%", min_value=0, max_value=market_table_new["Пазарен Дял"].max())
        }
        if has_prev_period:
            prev_new_agg = df_prev.groupby(["Brand", "Model"])["Нови"].sum().reset_index().rename(columns={"Нови": "Нови_Предх"})
            market_table_new = market_table_new.merge(prev_new_agg, on=["Brand", "Model"], how="left")
            market_table_new["Тенденция"] = [growth_badge(c, p) for c, p in zip(market_table_new["Нови"], market_table_new["Нови_Предх"])]
            market_table_new.drop(columns=["Нови_Предх"], inplace=True)
            col_config_new["Тенденция"] = st.column_config.TextColumn(f"Тенденция (спрямо {prev_period_label})")
            note = f"Тенденцията сравнява текущия период със същите месеци от предходната година: {prev_period_label}."
            if is_partial_yoy:
                note += " ⚠️ За част от месеците няма данни за миналата година — сравнението обхваща само наличните."
            st.caption(note)
        else:
            st.caption("Няма данни за същите месеци от предходната година — колона 'Тенденция' не се показва.")

        st.dataframe(market_table_new, column_config=col_config_new, hide_index=True, use_container_width=True)

# ==========================================
# ТАБ 3: ВТОРИЧЕН ПАЗАР
# ==========================================
with tab3:
    st.markdown(f'<div class="section-title">Вторичен пазар: Употребявани + Пререгистрации (Данни за периода: {period_label_full})</div>', unsafe_allow_html=True)

    df_used_agg = df_working.groupby(["Brand", "Model"])[["Употребявани", "Пререгистрации", "Вторичен Пазар"]].sum().reset_index()
    total_used_market = df_used_agg["Вторичен Пазар"].sum()

    if total_used_market == 0:
        st.info(f"Няма данни за вторичния пазар за периода {period_label_full}.")
    else:
        brand_totals_used = df_used_agg.groupby("Brand")["Вторичен Пазар"].sum().sort_values(ascending=False)
        leader_brand_u, leader_units_u = brand_totals_used.index[0], brand_totals_used.iloc[0]
        prev_total_used = df_prev["Вторичен Пазар"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо вторичен пазар", fmt_num(total_used_market), accent="#3B82F6")
        render_kpi_growth(k2, "Ръст спрямо предх. период", total_used_market, prev_total_used, accent="#3B82F6")
        kpi_card(k3, "Пазарен лидер", leader_brand_u, sub=f"{fmt_num(leader_units_u)} бр. ({leader_units_u/total_used_market:.1%})", accent="#3B82F6")
        kpi_card(k4, "Активни марки / модели", f"{df_used_agg['Brand'].nunique()} / {df_used_agg['Model'].nunique()}", accent="#3B82F6")

        st.markdown("<br>", unsafe_allow_html=True)
        render_trend_chart(key="trend_tab3")
        st.markdown("<br>", unsafe_allow_html=True)

        col_u1, col_u2 = st.columns([1, 1])

        top_brands_used = brand_totals_used.reset_index().head(15)
        fig_b_used = px.bar(top_brands_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Brand", orientation="h", title="Топ 15 Марки (Вторичен пазар)", text="Вторичен Пазар", color="Вторичен Пазар", color_continuous_scale="blues")
        fig_b_used.update_layout(coloraxis_showscale=False, height=420)
        col_u1.plotly_chart(fig_b_used, use_container_width=True)

        top_models_used = df_used_agg.sort_values("Вторичен Пазар", ascending=False).head(15).copy()
        top_models_used["Име"] = top_models_used["Brand"] + " " + top_models_used["Model"]
        fig_m_used = px.bar(top_models_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Име", orientation="h", title="Топ 15 Най-търсени Модели (Вторичен пазар)", text="Вторичен Пазар", color_discrete_sequence=["#3B82F6"])
        fig_m_used.update_layout(height=420)
        col_u2.plotly_chart(fig_m_used, use_container_width=True)

        pie_data_used = brand_totals_used.reset_index()
        if len(pie_data_used) > 30:
            others_sum_u = pie_data_used.iloc[30:]["Вторичен Пазар"].sum()
            pie_data_used = pie_data_used.head(30)
            if others_sum_u > 0:
                pie_data_used = pd.concat([pie_data_used, pd.DataFrame([{"Brand": "ДРУГИ", "Вторичен Пазар": others_sum_u}])], ignore_index=True)

        fig_pie_used = px.pie(pie_data_used, names="Brand", values="Вторичен Пазар", title="Пазарен дял по марки (Топ 30 + Други)", hole=0.45)
        fig_pie_used.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie_used.update_layout(height=560, showlegend=False)
        st.plotly_chart(fig_pie_used, use_container_width=True)

        st.markdown("##### 📋 Справка за ликвидност (Кое се продава най-много втора ръка)")
        market_table_used = df_used_agg[df_used_agg["Вторичен Пазар"] > 0].sort_values("Вторичен Пазар", ascending=False).copy()
        market_table_used["Дял от вторичния пазар"] = (market_table_used["Вторичен Пазар"] / total_used_market) * 100

        col_config_used = {
            "Brand": "Марка", "Model": "Модел",
            "Употребявани": st.column_config.NumberColumn("Нов Внос", format="%d"),
            "Пререгистрации": st.column_config.NumberColumn("Смяна на собственост", format="%d"),
            "Вторичен Пазар": st.column_config.NumberColumn("Общо Вторичен Пазар", width="medium", format="%d"),
            "Дял от вторичния пазар": st.column_config.ProgressColumn("Дял %", format="%.2f%%", min_value=0, max_value=market_table_used["Дял от вторичния пазар"].max())
        }
        if has_prev_period:
            prev_used_agg = df_prev.groupby(["Brand", "Model"])["Вторичен Пазар"].sum().reset_index().rename(columns={"Вторичен Пазар": "Вторичен_Предх"})
            market_table_used = market_table_used.merge(prev_used_agg, on=["Brand", "Model"], how="left")
            market_table_used["Тенденция"] = [growth_badge(c, p) for c, p in zip(market_table_used["Вторичен Пазар"], market_table_used["Вторичен_Предх"])]
            market_table_used.drop(columns=["Вторичен_Предх"], inplace=True)
            col_config_used["Тенденция"] = st.column_config.TextColumn(f"Тенденция (спрямо {prev_period_label})")
            note_u = f"Тенденцията сравнява текущия период със същите месеци от предходната година: {prev_period_label}."
            if is_partial_yoy:
                note_u += " ⚠️ За част от месеците няма данни за миналата година — сравнението обхваща само наличните."
            st.caption(note_u)
        else:
            st.caption("Няма данни за същите месеци от предходната година — колона 'Тенденция' не се показва.")

        st.dataframe(market_table_used, column_config=col_config_used, hide_index=True, use_container_width=True)