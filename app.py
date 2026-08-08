import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os
import glob

# ====================================================================================
# AUTO MOTO SALES BG - CLEAN EXECUTIVE EDITION (V3 - Fixes)
# ====================================================================================

st.set_page_config(page_title="AUTO MOTO SALES BG", page_icon="📊", layout="wide")

# ----------------------------------------------------------------------------------
# 0. ПРЕМИУМ HERO БАНЕР И РЕСПОНСИВ ДИЗАЙН
# ----------------------------------------------------------------------------------
# ВАЖНО: Тук няма никакви интервали в началото на редовете, за да не се бърка Markdown!
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }

.hero-container {
background-color: #ffffff;
border: 1px solid #e2e8f0;
border-radius: 12px;
padding: 1.8rem 2.2rem;
margin-bottom: 1.5rem;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
display: flex;
align-items: center;
justify-content: space-between;
gap: 20px;
}

.hero-left {
display: flex;
align-items: center;
gap: 20px;
}

.hero-logo-box {
background: #e0e7ff;
color: #4f46e5;
border-radius: 12px;
padding: 14px;
display: flex;
align-items: center;
justify-content: center;
}

.hero-title {
font-size: 2.2rem;
font-weight: 800;
color: #0f172a;
margin: 0;
line-height: 1.1;
letter-spacing: -0.03em;
}

.hero-sub {
font-size: 0.95rem;
color: #64748b;
margin-top: 6px;
font-weight: 500;
}

.hero-right {
display: flex;
gap: 12px;
}

.meta-badge {
background: #f8fafc;
border: 1px solid #e2e8f0;
border-radius: 8px;
padding: 10px 16px;
text-align: right;
}

.meta-label { font-size: 0.7rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.meta-value { font-size: 0.9rem; color: #0f172a; font-weight: 700; margin-top: 2px; }

.kpi-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; border-left: 4px solid #4f46e5; box-shadow: 0 1px 3px rgba(0,0,0,0.05); min-height: 92px; }
.kpi-label { font-size: 0.75rem; color:#64748b; font-weight:700; text-transform:uppercase; }
.kpi-value { font-size: 1.8rem; font-weight:800; color:#0f172a; margin-top: 4px; }
.kpi-sub { font-size: 0.8rem; font-weight:600; margin-top:5px; }

.section-title { font-size: 1.2rem; font-weight: 700; color:#1e293b; margin: 1.5rem 0 1rem 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0;}

@media (max-width: 768px) {
.hero-container { flex-direction: column; text-align: center; padding: 1.5rem 1rem; }
.hero-left { flex-direction: column; }
.hero-right { flex-direction: column; width: 100%; align-items: stretch; text-align: center; }
.meta-badge { text-align: center; }
.kpi-card { margin-bottom: 15px; }
}

header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

svg_logo = """
<svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>
<circle cx="7" cy="17" r="2"/>
<path d="M9 17h6"/>
<circle cx="17" cy="17" r="2"/>
</svg>
"""

st.markdown(f"""
<div class="hero-container">
<div class="hero-left">
<div class="hero-logo-box">
{svg_logo}
</div>
<div>
<div class="hero-title">AUTO MOTO SALES BG</div>
<div class="hero-sub">Професионален BI портал за анализ на регистрациите на МПС</div>
</div>
</div>
<div class="hero-right">
<div class="meta-badge">
<div class="meta-label">Статус на системата</div>
<div class="meta-value" style="color: #10b981;">🟢 Оптимизиран режим</div>
</div>
<div class="meta-badge">
<div class="meta-label">Източник</div>
<div class="meta-value">Официални данни КАТ</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

def kpi_card(col, label, value, sub=None, sub_color="#64748b", accent="#4f46e5"):
    sub_html = f'<div class="kpi-sub" style="color:{sub_color};">{sub}</div>' if sub else ""
    col.markdown(
        f'<div class="kpi-card" style="border-left-color:{accent};">'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True
    )

def fmt_num(x): return f"{x:,.0f}".replace(",", " ")

# ----------------------------------------------------------------------------------
# 1. ГЛАВНО МЕНЮ И ВРЕМЕВИ ПРОЗОРЕЦ 
# ----------------------------------------------------------------------------------
VEHICLE_CATEGORIES = {
    "Леки автомобили (M1)": ["M1"],
    "Лекотоварни (N1)": ["N1"],
    "Товарни (N2, N3)": ["N2", "N3"],
    "Мотори и АТВ (L)": ["L1", "L2", "L3", "L4", "L5", "L6", "L7"],
    "Други": ["M2", "M3", "O1", "O2", "O3", "O4", "T", "OT"]
}

col_cat, col_time = st.columns([1, 1])

with col_cat:
    st.markdown("##### 📑 Изберете категория:")
    selected_cat = st.pills("Категория", options=list(VEHICLE_CATEGORIES.keys()), default="Леки автомобили (M1)", label_visibility="collapsed")

if not selected_cat:
    st.stop()

# ----------------------------------------------------------------------------------
# 2. ОПТИМИЗИРАНА ОБРАБОТКА НА ДАННИТЕ
# ----------------------------------------------------------------------------------
SUMMARY_ROW_PATTERN = r"ОБЩ|ВСИЧК|TOTAL|SUM"

@st.cache_data(show_spinner=False)
def load_and_process(file_bytes_list, file_names, category_name):
    parsed_files = []
    prefixes = VEHICLE_CATEGORIES[category_name]
    
    for content, name in zip(file_bytes_list, file_names):
        match = re.search(r'(\d{1,2})[_.-](\d{4})', name)
        if not match: continue
        month, year = int(match.group(1)), int(match.group(2))
        try:
            try: df = pd.read_csv(pd.io.common.BytesIO(content), encoding="utf-8")
            except: df = pd.read_csv(pd.io.common.BytesIO(content), encoding="cp1251")
            
            df.columns = [c.strip() for c in df.columns]
            brand_col = [c for c in df.columns if "МАРКА" in c.upper()][0]
            model_col = [c for c in df.columns if "МОДЕЛ" in c.upper()][0]
            
            n_cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes) and 'нови' in c.lower() and 'общо' not in c.lower()]
            u_cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes) and 'употр' in c.lower() and 'общо' not in c.lower()]
            o_cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes) and 'други' in c.lower() and 'общо' not in c.lower()]
            
            cols_to_keep = [brand_col, model_col] + n_cols + u_cols + o_cols
            df = df[cols_to_keep].copy()
            
            parsed_files.append({
                "year": year, "month": month, 
                "period_str": f"{month:02d}.{year}", "sort_index": year * 100 + month, 
                "df": df, "n_cols": n_cols, "u_cols": u_cols, "o_cols": o_cols,
                "b_col": brand_col, "m_col": model_col
            })
        except: continue

    if not parsed_files: return None
    parsed_files = sorted(parsed_files, key=lambda x: x["sort_index"])

    all_dfs = []
    for item in parsed_files:
        temp_df = item["df"].copy()
        temp_df["Година"], temp_df["Месец"], temp_df["Период"], temp_df["Sort_Index"] = item["year"], item["month"], item["period_str"], item["sort_index"]

        temp_df["Brand"] = temp_df[item["b_col"]].fillna("НЕИЗВЕСТНА").astype(str).str.strip().str.upper()
        temp_df["_RawModel"] = temp_df[item["m_col"]].fillna("НЕИЗВЕСТЕН").astype(str).str.strip().str.upper()

        valid_mask = (
            (~temp_df["Brand"].str.contains(SUMMARY_ROW_PATTERN, case=False, na=False, regex=True)) &
            (~temp_df["_RawModel"].str.contains(SUMMARY_ROW_PATTERN, case=False, na=False, regex=True)) &
            (temp_df["Brand"].str.strip() != "")
        )
        temp_df = temp_df[valid_mask].copy()
        if temp_df.empty: continue

        def clean_model(b, m): return m[len(b):].strip() if m.startswith(b) and len(m) > len(b) else m
        temp_df["Model"] = [clean_model(b, m) for b, m in zip(temp_df["Brand"], temp_df["_RawModel"])]
        temp_df["Label"] = temp_df["Brand"] + " " + temp_df["Model"]
        
        temp_df["Нови"] = temp_df[item["n_cols"]].sum(axis=1) if item["n_cols"] else 0
        temp_df["Употр"] = temp_df[item["u_cols"]].sum(axis=1) if item["u_cols"] else 0
        temp_df["Други"] = temp_df[item["o_cols"]].sum(axis=1) if item["o_cols"] else 0

        clean_df = temp_df[["Sort_Index", "Година", "Месец", "Период", "Brand", "Model", "Label", "Нови", "Употр", "Други"]]
        all_dfs.append(clean_df)

    if not all_dfs: return None
    raw_df = pd.concat(all_dfs, ignore_index=True)

    agg_df = raw_df.groupby(["Sort_Index", "Година", "Месец", "Период", "Brand", "Model", "Label"], as_index=False)[["Нови", "Употр", "Други"]].sum()
    agg_df = agg_df.sort_values(by=["Sort_Index", "Brand", "Model"])
    
    for col in ["Нови", "Употр", "Други"]:
        agg_df[f"{col}_Месец"] = agg_df.groupby(["Година", "Brand", "Model"])[col].diff().fillna(agg_df[col]).clip(lower=0)

    return agg_df

csv_files = glob.glob(os.path.join("data", "*.csv")) + glob.glob(os.path.join("data", "*.gz")) + glob.glob(os.path.join("data", "*.zip"))

if not csv_files:
    st.info("📂 Няма намерени CSV/ZIP файлове в папка 'data'. Моля, добави ги през GitHub.")
    st.stop()

file_bytes_list, file_names = [], []
for file_path in csv_files:
    with open(file_path, "rb") as f: file_bytes_list.append(f.read())
    file_names.append(os.path.basename(file_path))

with st.spinner(f"Зареждане и оптимизиране на данни за {selected_cat}..."):
    df_full = load_and_process(tuple(file_bytes_list), tuple(file_names), selected_cat)

if df_full is None or df_full.empty:
    st.error(f"Няма налични данни за категория '{selected_cat}'.")
    st.stop()

# ----------------------------------------------------------------------------------
# ВРЕМЕВИ ПРОЗОРЕЦ 
# ----------------------------------------------------------------------------------
unique_periods = df_full[["Sort_Index", "Период"]].drop_duplicates().sort_values("Sort_Index")
p_opts = unique_periods["Sort_Index"].tolist()
p_lbls = unique_periods["Период"].tolist()

with col_time:
    st.markdown("##### ⚙️ Времеви прозорец:")
    if len(p_opts) > 1:
        opts_2026 = [opt for opt in p_opts if str(opt).startswith("2026")]
        default_start, default_end = (opts_2026[0], opts_2026[-1]) if opts_2026 else (p_opts[0], p_opts[-1])

        start_idx, end_idx = st.select_slider(
            "Избери период", options=p_opts, value=(default_start, default_end), 
            format_func=lambda x: unique_periods[unique_periods["Sort_Index"]==x]["Период"].values[0],
            label_visibility="collapsed"
        )
    else:
        start_idx, end_idx = (p_opts[0], p_opts[0])
        st.info(f"Наличен е само един период: {unique_periods['Период'].values[0]}")

st.markdown("---") 

df_working = df_full[(df_full["Sort_Index"] >= start_idx) & (df_full["Sort_Index"] <= end_idx)].copy()
df_working["Нови"] = df_working["Нови_Месец"]
df_working["Употребявани"] = df_working["Употр_Месец"]
df_working["Пререгистрации"] = df_working["Други_Месец"]
df_working["Вторичен Пазар"] = df_working["Употребявани"] + df_working["Пререгистрации"]
df_working["Всички"] = df_working["Нови"] + df_working["Вторичен Пазар"]

start_period_str = unique_periods[unique_periods["Sort_Index"] == start_idx]["Период"].values[0]
end_period_str = unique_periods[unique_periods["Sort_Index"] == end_idx]["Период"].values[0]
period_label_full = f"{start_period_str} - {end_period_str}" if start_period_str != end_period_str else start_period_str

period_lookup = dict(zip(p_opts, p_lbls))
selected_sort_indices = sorted(df_working["Sort_Index"].unique().tolist())
prev_sort_indices = sorted([s - 100 for s in selected_sort_indices if (s - 100) in period_lookup])
has_prev_period = len(prev_sort_indices) > 0

if has_prev_period:
    df_prev = df_full[df_full["Sort_Index"].isin(prev_sort_indices)].copy()
    df_prev["Нови"] = df_prev["Нови_Месец"]
    df_prev["Вторичен Пазар"] = df_prev["Употр_Месец"] + df_prev["Други_Месец"]
    prev_labels = [period_lookup[s] for s in prev_sort_indices]
    prev_period_label = f"{prev_labels[0]} - {prev_labels[-1]}" if len(prev_labels) > 1 else prev_labels[0]
else:
    df_prev = pd.DataFrame(columns=list(df_working.columns))
    prev_period_label = None

def get_growth_data(current, previous):
    if previous is None or pd.isna(previous) or previous == 0: return None
    return (current - previous) / previous * 100

def render_kpi_growth(col, label, current_total, prev_total, accent):
    growth_pct = get_growth_data(current_total, prev_total)
    if growth_pct is None:
        kpi_card(col, label, "—", sub="Няма данни", accent="#94a3b8")
    elif growth_pct >= 0:
        kpi_card(col, label, f"+{growth_pct:.1f}%", sub=f"📈 спрямо {prev_period_label}", sub_color="#10B981", accent=accent)
    else:
        kpi_card(col, label, f"{growth_pct:.1f}%", sub=f"📉 спрямо {prev_period_label}", sub_color="#EF4444", accent=accent)

def render_trend_chart(trend_df, title, key):
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend_df["Период"], y=trend_df["Нови"], name="Нови", mode="lines+markers",
                                    line=dict(color="#4f46e5", width=3, shape="spline"), marker=dict(size=7),
                                    fill="tozeroy", fillcolor="rgba(79,70,229,0.08)"))
    fig_trend.add_trace(go.Scatter(x=trend_df["Период"], y=trend_df["Вторичен Пазар"], name="Вторичен пазар", mode="lines+markers",
                                    line=dict(color="#0ea5e9", width=3, shape="spline"), marker=dict(size=7),
                                    fill="tozeroy", fillcolor="rgba(14,165,233,0.08)"))
    fig_trend.update_layout(title=title, template="plotly_white", height=320,
                             hovermode="x unified", legend=dict(orientation="h", y=1.18, x=0), margin=dict(t=50, l=10, r=10))
    st.plotly_chart(fig_trend, key=key)

# ----------------------------------------------------------------------------------
# 4. ТАБОВЕ ЗА АНАЛИЗ 
# ----------------------------------------------------------------------------------
tab_brand, tab_model, tab_new, tab_used = st.tabs(["🏢 Анализ по Марки", "🔍 Анализ по Модели", "✨ Пазар НОВИ МПС", "🤝 ВТОРИЧЕН Пазар"])

with tab_brand:
    st.markdown('<div class="section-title">Цялостен анализ на портфолиото на избрана марка</div>', unsafe_allow_html=True)
    all_brands_list = sorted(df_working["Brand"].unique())
    
    col_b1, col_b2 = st.columns([1, 2])
    default_b = "ПЕЖО" if "ПЕЖО" in all_brands_list else all_brands_list[0]
    
    selected_brand = col_b1.selectbox("Избери марка за детайлен преглед:", options=all_brands_list, index=all_brands_list.index(default_b))
    metric_brand = st.pills("Изследвана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Всички", key="pill_brand")
    
    if selected_brand and metric_brand:
        brand_data = df_working[df_working["Brand"] == selected_brand]
        
        brand_trend = brand_data.groupby(["Sort_Index", "Период"])[metric_brand].sum().reset_index().sort_values("Sort_Index")
        fig_b_trend = go.Figure()
        fig_b_trend.add_trace(go.Scatter(x=brand_trend["Период"], y=brand_trend[metric_brand], mode="lines+markers+text", 
                                         text=brand_trend[metric_brand], textposition="top center",
                                         line=dict(width=3, shape="spline", color="#4f46e5"), marker=dict(size=8), fill="tozeroy", fillcolor="rgba(79,70,229,0.08)"))
        fig_b_trend.update_layout(title=f"Динамика на продажбите ({metric_brand}) за марка {selected_brand}", template="plotly_white", height=380, hovermode="x unified", margin=dict(t=40, l=10, r=10))
        st.plotly_chart(fig_b_trend)
        
        st.markdown(f"**Топ модели на {selected_brand} за периода ({start_period_str} - {end_period_str})**")
        brand_models = brand_data.groupby("Model")[metric_brand].sum().reset_index()
        brand_models = brand_models[brand_models[metric_brand] > 0].sort_values(metric_brand, ascending=False).head(20)
        
        fig_b_models = px.bar(brand_models.sort_values(metric_brand), x=metric_brand, y="Model", orientation="h", text=metric_brand, color_discrete_sequence=["#6366f1"])
        fig_b_models.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10))
        st.plotly_chart(fig_b_models)

with tab_model:
    st.markdown('<div class="section-title">Сравнителен анализ на конкретни модели</div>', unsafe_allow_html=True)
    model_volumes = df_working.groupby(["Brand", "Label"])["Всички"].sum().reset_index()
    liquid_models = model_volumes[model_volumes["Всички"] >= 5]

    col_f1, col_f2 = st.columns([1, 2])
    available_brands = sorted(liquid_models["Brand"].unique())
    sel_brand = col_f1.selectbox("1. Филтър по марка (опционално):", options=["Всички марки"] + available_brands)

    if sel_brand == "Всички марки": available_labels = sorted(liquid_models["Label"].unique())
    else: available_labels = sorted(liquid_models[liquid_models["Brand"] == sel_brand]["Label"].unique())

    target_models = ["ШКОДА КОДИАК", "ФОЛКСВАГЕН ТАЙРОН", "ХЮНДАЙ САНТА ФЕ", "КИА СОРЕНТО"]
    def_models = [l for l in available_labels if any(t in l for t in target_models)]
    if not def_models and available_labels: def_models = [available_labels[0]]

    sel_models = col_f2.multiselect("2. Избери модели за сравнение:", options=available_labels, default=def_models)

    st.markdown("<br>", unsafe_allow_html=True)
    metric_tab1 = st.pills("Изследвана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Всички", key="pill_model")

    if sel_models and metric_tab1:
        m_data = df_working[df_working["Label"].isin(sel_models)].sort_values("Sort_Index")
        fig = go.Figure()
        colors = ["#4f46e5", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444"]

        for i, model in enumerate(sel_models):
            model_df = m_data[m_data["Label"] == model]
            fig.add_trace(go.Scatter(
                x=model_df["Период"], y=model_df[metric_tab1], name=model, mode="lines+markers+text",
                text=model_df[metric_tab1], textposition="top center",
                line=dict(width=3, shape="spline", color=colors[i % len(colors)]), marker=dict(size=8)
            ))

        fig.update_layout(template="plotly_white", height=400, hovermode="x unified", legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=20, l=10, r=10))
        st.plotly_chart(fig)

with tab_new:
    st.markdown(f'<div class="section-title">Пазарен дял и лидери (НОВИ МПС) <span style="font-size:0.85rem; color:#64748b; font-weight:normal;">| Период: {period_label_full}</span></div>', unsafe_allow_html=True)

    df_new_agg = df_working.groupby(["Brand", "Model"])["Нови"].sum().reset_index()
    total_new_market = df_new_agg["Нови"].sum()

    if total_new_market == 0:
        st.info(f"Няма регистрирани нови МПС от тази категория за периода {period_label_full}.")
    else:
        brand_totals_new = df_new_agg.groupby("Brand")["Нови"].sum().sort_values(ascending=False)
        leader_brand, leader_units = brand_totals_new.index[0], brand_totals_new.iloc[0]
        prev_total_new = df_prev["Нови"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо нови", fmt_num(total_new_market), accent="#4f46e5")
        render_kpi_growth(k2, "Ръст (YoY)", total_new_market, prev_total_new, accent="#4f46e5")
        kpi_card(k3, "Пазарен лидер", leader_brand, sub=f"Дял: {leader_units/total_new_market:.1%}", accent="#4f46e5")
        kpi_card(k4, "Активни марки", str(df_new_agg['Brand'].nunique()), accent="#4f46e5")

        st.markdown("<br>", unsafe_allow_html=True)
        trend_df = df_working.groupby(["Sort_Index", "Период"])[["Нови", "Вторичен Пазар"]].sum().reset_index().sort_values("Sort_Index")
        render_trend_chart(trend_df, "Тренд: Нови спрямо Вторичен пазар", "trend_tab2")
        
        col_m1, col_m2 = st.columns([1, 1])
        top_brands_new = brand_totals_new.reset_index().head(15)
        fig_b_new = px.bar(top_brands_new.sort_values("Нови"), x="Нови", y="Brand", orientation="h", title="Топ 15 Марки", text="Нови", color_discrete_sequence=["#4f46e5"])
        fig_b_new.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10))
        col_m1.plotly_chart(fig_b_new)

        top_models_new = df_new_agg.sort_values("Нови", ascending=False).head(15).copy()
        top_models_new["Име"] = top_models_new["Brand"] + " " + top_models_new["Model"]
        fig_m_new = px.bar(top_models_new.sort_values("Нови"), x="Нови", y="Име", orientation="h", title="Топ 15 Модели", text="Нови", color_discrete_sequence=["#6366f1"])
        fig_m_new.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10))
        col_m2.plotly_chart(fig_m_new)

        st.markdown("##### Детайлна справка (Нови)")
        market_table_new = df_new_agg[df_new_agg["Нови"] > 0].sort_values("Нови", ascending=False).copy()
        market_table_new["Дял %"] = (market_table_new["Нови"] / total_new_market) * 100
        
        st.dataframe(market_table_new, hide_index=True, width="stretch", column_config={
            "Нови": st.column_config.NumberColumn("Брой", format="%d"),
            "Дял %": st.column_config.ProgressColumn("Пазарен Дял", format="%.2f%%", min_value=0, max_value=market_table_new["Дял %"].max())
        })

with tab_used:
    st.markdown(f'<div class="section-title">Вторичен пазар (Употребявани + Пререгистрации) <span style="font-size:0.85rem; color:#64748b; font-weight:normal;">| Период: {period_label_full}</span></div>', unsafe_allow_html=True)

    df_used_agg = df_working.groupby(["Brand", "Model"])[["Употребявани", "Пререгистрации", "Вторичен Пазар"]].sum().reset_index()
    total_used_market = df_used_agg["Вторичен Пазар"].sum()

    if total_used_market == 0:
        st.info(f"Няма данни за вторичния пазар за периода {period_label_full}.")
    else:
        brand_totals_used = df_used_agg.groupby("Brand")["Вторичен Пазар"].sum().sort_values(ascending=False)
        leader_brand_u, leader_units_u = brand_totals_used.index[0], brand_totals_used.iloc[0]
        prev_total_used = df_prev["Вторичен Пазар"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо вторичен пазар", fmt_num(total_used_market), accent="#0ea5e9")
        render_kpi_growth(k2, "Ръст (YoY)", total_used_market, prev_total_used, accent="#0ea5e9")
        kpi_card(k3, "Пазарен лидер", leader_brand_u, sub=f"Дял: {leader_units_u/total_used_market:.1%}", accent="#0ea5e9")
        kpi_card(k4, "Активни марки", str(df_used_agg['Brand'].nunique()), accent="#0ea5e9")

        st.markdown("<br>", unsafe_allow_html=True)
        trend_df = df_working.groupby(["Sort_Index", "Период"])[["Нови", "Вторичен Пазар"]].sum().reset_index().sort_values("Sort_Index")
        render_trend_chart(trend_df, "Тренд: Нови спрямо Вторичен пазар", "trend_tab3")
        
        col_u1, col_u2 = st.columns([1, 1])
        top_brands_used = brand_totals_used.reset_index().head(15)
        fig_b_used = px.bar(top_brands_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Brand", orientation="h", title="Топ 15 Марки", text="Вторичен Пазар", color_discrete_sequence=["#0ea5e9"])
        fig_b_used.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10))
        col_u1.plotly_chart(fig_b_used)

        top_models_used = df_used_agg.sort_values("Вторичен Пазар", ascending=False).head(15).copy()
        top_models_used["Име"] = top_models_used["Brand"] + " " + top_models_used["Model"]
        fig_m_used = px.bar(top_models_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Име", orientation="h", title="Топ 15 Модели", text="Вторичен Пазар", color_discrete_sequence=["#38bdf8"])
        fig_m_used.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10))
        col_u2.plotly_chart(fig_m_used)

        st.markdown("##### Детайлна справка (Вторичен Пазар)")
        market_table_used = df_used_agg[df_used_agg["Вторичен Пазар"] > 0].sort_values("Вторичен Пазар", ascending=False).copy()
        market_table_used["Дял %"] = (market_table_used["Вторичен Пазар"] / total_used_market) * 100

        st.dataframe(market_table_used, hide_index=True, width="stretch", column_config={
            "Употребявани": st.column_config.NumberColumn("Нов Внос", format="%d"),
            "Пререгистрации": st.column_config.NumberColumn("Смяна на собственост", format="%d"),
            "Вторичен Пазар": st.column_config.NumberColumn("Общо Вторичен Пазар", format="%d"),
            "Дял %": st.column_config.ProgressColumn("Пазарен Дял", format="%.2f%%", min_value=0, max_value=market_table_used["Дял %"].max())
        })
