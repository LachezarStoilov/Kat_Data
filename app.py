import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os
import glob

# ====================================================================================
# AUTO MOTO SALES BG - CLEAN EXECUTIVE EDITION (V7 - Bugfix Release)
# ====================================================================================

st.set_page_config(page_title="AUTO MOTO SALES BG", page_icon="📊", layout="wide")

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

.kpi-card { 
    background: #ffffff; 
    border: 1px solid #e2e8f0; 
    border-radius: 10px; 
    padding: 1.2rem; 
    border-left: 4px solid #4f46e5; 
    box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
    height: 100%; 
    min-height: 115px; 
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
}
.kpi-label { font-size: 0.75rem; color:#64748b; font-weight:700; text-transform:uppercase; }
.kpi-value { font-size: 1.8rem; font-weight:800; color:#0f172a; margin-top: 4px; }
.kpi-sub { font-size: 0.8rem; font-weight:600; margin-top:5px; min-height: 1.2em; }

.section-title { font-size: 1.2rem; font-weight: 700; color:#1e293b; margin: 1.5rem 0 1rem 0; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0;}

/* =========================================================
   RESPONSIVE / MOBILE
   ========================================================= */

@media (max-width: 768px) {

    /* ---------- HERO ---------- */

    .hero-container {
        flex-direction: column;
        text-align: center;
        padding: 1.25rem 0.9rem;
        gap: 14px;
    }

    .hero-left {
        flex-direction: column;
        gap: 10px;
    }

    .hero-title {
        font-size: 1.55rem;
        line-height: 1.15;
    }

    .hero-sub {
        font-size: 0.78rem;
    }

    .hero-right {
        flex-direction: column;
        width: 100%;
        align-items: stretch;
        text-align: center;
        gap: 8px;
    }

    .meta-badge {
        width: 100%;
        box-sizing: border-box;
        text-align: center;
        padding: 8px 10px;
    }

    .meta-value {
        font-size: 0.78rem;
    }


    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        margin-bottom: 10px;
        min-height: 95px;
        padding: 0.9rem;
    }

    .kpi-value {
        font-size: 1.45rem;
    }

    .kpi-label {
        font-size: 0.68rem;
    }


    /* ---------- TABS ---------- */

    .stTabs [data-baseweb="tab-list"] {
        width: 100%;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        scrollbar-width: none;
        -webkit-overflow-scrolling: touch;
    }

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 0 0 auto !important;
        white-space: nowrap !important;
        min-width: max-content !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        font-size: 0.82rem !important;
    }


    /* ---------- PILLS ---------- */

    [data-testid="stPills"] {
        width: 100%;
        overflow: visible !important;
    }

    [data-testid="stPills"] > div {
        flex-wrap: wrap !important;
        gap: 6px !important;
    }


    /* ---------- STREAMLIT COLUMNS ---------- */

    [data-testid="stHorizontalBlock"] {
        gap: 0.75rem !important;
    }


    /* ---------- PLOTLY ---------- */

    .js-plotly-plot,
    .plot-container,
    .plotly {
        max-width: 100% !important;
    }

    [data-testid="stPlotlyChart"] {
        width: 100% !important;
        overflow: hidden !important;
    }


    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 1rem;
        line-height: 1.35;
        margin-top: 1rem;
    }
}


/* =========================================================
   VERY SMALL PHONES
   ========================================================= */

@media (max-width: 480px) {

    .hero-title {
        font-size: 1.35rem;
    }

    .section-title {
        font-size: 0.95rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 0.75rem !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
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
<div class="hero-title">AUTOMOTIVE SALES BG</div>
<div class="hero-sub">Портал за анализ на регистрациите на МПС v0.9</div>
</div>
</div>
<div class="hero-right">
<div class="meta-badge">
<div class="meta-label">Статус на системата</div>
<div class="meta-value" style="color: #10b981;">🟢 Данни от 01.01.2025 до 31.07.2026 </div>
</div>
<div class="meta-badge">
<div class="meta-label">Източник</div>
<div class="meta-value">Официални данни КАТ</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

PLOTLY_CONFIG = {'displayModeBar': False, 'scrollZoom': False}

def apply_plotly_mobile_lock(fig):
    fig.update_layout(dragmode=False)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True, type='category')
    fig.update_traces(textfont_size=15, textposition="outside", cliponaxis=False)
    return fig

def kpi_card(col, label, value, sub=None, sub_color="#64748b", accent="#4f46e5"):
    sub_html = f'<div class="kpi-sub" style="color:{sub_color};">{sub}</div>' if sub else '<div class="kpi-sub">&nbsp;</div>'
    col.markdown(
        f'<div class="kpi-card" style="border-left-color:{accent};">'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True
    )

def fmt_num(x): return f"{x:,.0f}".replace(",", " ")

def get_rgb(hex_col):
    h = hex_col.lstrip('#')
    return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

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
if not selected_cat: st.stop()

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
        
        temp_df["Нови"] = temp_df[item["n_cols"]].sum(axis=1) if item["n_cols"] else 0
        temp_df["Употр"] = temp_df[item["u_cols"]].sum(axis=1) if item["u_cols"] else 0
        temp_df["Други"] = temp_df[item["o_cols"]].sum(axis=1) if item["o_cols"] else 0
        
        temp_df["Total_Cat"] = temp_df["Нови"] + temp_df["Употр"] + temp_df["Други"]
        temp_df = temp_df[temp_df["Total_Cat"] > 0].copy()

        def clean_model(b, m): return m[len(b):].strip() if m.startswith(b) and len(m) > len(b) else m
        temp_df["Model"] = [clean_model(b, m) for b, m in zip(temp_df["Brand"], temp_df["_RawModel"])]
        temp_df["Label"] = temp_df["Brand"] + " " + temp_df["Model"]

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
    df_prev["Употребявани"] = df_prev["Употр_Месец"]
    df_prev["Пререгистрации"] = df_prev["Други_Месец"]
    df_prev["Вторичен Пазар"] = df_prev["Употребявани"] + df_prev["Пререгистрации"]
    df_prev["Всички"] = df_prev["Нови"] + df_prev["Вторичен Пазар"]
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

def render_yoy_trend_chart(df_curr, df_prv, metric, title, key, color_curr, color_prv="#9ca3af"):
    if df_curr.empty:
        return
        
    curr_agg = df_curr.groupby("Месец")[metric].sum().reset_index().sort_values("Месец")
    month_names = {1:"Яну", 2:"Фев", 3:"Мар", 4:"Апр", 5:"Май", 6:"Юни", 7:"Юли", 8:"Авг", 9:"Сеп", 10:"Окт", 11:"Ное", 12:"Дек"}
    curr_agg["Месец_Име"] = curr_agg["Месец"].map(month_names)
    
    fig = go.Figure()
    
    if not df_prv.empty:
        prv_agg = df_prv.groupby("Месец")[metric].sum().reset_index().sort_values("Месец")
        prv_agg["Месец_Име"] = prv_agg["Месец"].map(month_names)
        fig.add_trace(go.Scatter(x=prv_agg["Месец_Име"], y=prv_agg[metric], name="Предходна година", mode="lines+markers",
                                 line=dict(color=color_prv, width=2, shape="spline", dash="dot"), marker=dict(size=6)))
                                 
    fig.add_trace(go.Scatter(x=curr_agg["Месец_Име"], y=curr_agg[metric], name="Текущ период", mode="lines+markers+text",
                             text=curr_agg[metric], textposition="top center", textfont=dict(size=14, color=color_curr),
                             line=dict(color=color_curr, width=3, shape="spline"), marker=dict(size=8),
                             fill="tozeroy", fillcolor=f"rgba({get_rgb(color_curr)},0.08)"))
                             
    fig.update_layout(
        title=title, 
        template="plotly_white", 
        height=360, 
        dragmode=False,
        hovermode="x unified", 
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), 
        margin=dict(t=50, l=10, r=10, b=30)
    )
    
    fig.update_xaxes(fixedrange=True, categoryorder='array', categoryarray=list(month_names.values()))
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, config=PLOTLY_CONFIG, key=key)

# ----------------------------------------------------------------------------------
# 4. ТАБОВЕ ЗА АНАЛИЗ 
# ----------------------------------------------------------------------------------
tab_brand, tab_model, tab_new, tab_used = st.tabs(["📌 Анализ по МАРКИ", "🔍 Анализ по МОДЕЛИ", "🚘🚗 Пазар НОВИ МПС", "♻️ ВТОРИЧЕН Пазар"])

with tab_brand:
    st.markdown('<div class="section-title">Цялостен анализ на портфолиото на избрана марка</div>', unsafe_allow_html=True)
    all_brands_list = sorted(df_working["Brand"].unique())
    
    col_b1, col_b2 = st.columns([1, 2])
    default_b = "ШКОДА" if "ШКОДА" in all_brands_list else all_brands_list[0]
    
    selected_brand = col_b1.selectbox("Избери марка за детайлен преглед:", options=all_brands_list, index=all_brands_list.index(default_b))
    metric_brand = st.pills("Изследвана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Всички", key="pill_brand")
    
    if selected_brand and metric_brand:
        brand_data = df_working[df_working["Brand"] == selected_brand]
        brand_data_prev = df_prev[df_prev["Brand"] == selected_brand] if has_prev_period else pd.DataFrame(columns=df_working.columns)
        
        total_market_metric = df_working[metric_brand].sum()
        brand_total = brand_data[metric_brand].sum()
        brand_prev_total = brand_data_prev[metric_brand].sum() if has_prev_period else None
        brand_share = (brand_total / total_market_metric) * 100 if total_market_metric > 0 else 0
        active_models_count = brand_data[brand_data[metric_brand] > 0]["Model"].nunique()
        
        accent_brand = "#4f46e5"
        kb1, kb2, kb3, kb4 = st.columns(4)
        kpi_card(kb1, "Общо продажби", fmt_num(brand_total), accent=accent_brand)
        render_kpi_growth(kb2, "Ръст (YoY)", brand_total, brand_prev_total, accent=accent_brand)
        kpi_card(kb3, "Пазарен дял", f"{brand_share:.1f}%", sub=f"от общо {fmt_num(total_market_metric)}", accent=accent_brand)
        kpi_card(kb4, "Активни модели", str(active_models_count), sub="с регистрации за периода", accent=accent_brand)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_yoy_trend_chart(
            df_curr=brand_data, 
            df_prv=brand_data_prev, 
            metric=metric_brand, 
            title=f"Динамика на продажбите (YoY): {metric_brand} за {selected_brand}", 
            key="yoy_brand_chart", 
            color_curr=accent_brand
        )
        
        st.markdown(f"**Топ модели на {selected_brand} за периода ({start_period_str} - {end_period_str})**")
        brand_models = brand_data.groupby("Model")[metric_brand].sum().reset_index()
        brand_models = brand_models[brand_models[metric_brand] > 0].sort_values(metric_brand, ascending=False).head(20)
        brand_models["Model"] = brand_models["Model"].astype(str) 
        
        fig_b_models = px.bar(
            brand_models.sort_values(metric_brand), 
            x=metric_brand, y="Model", orientation="h", text=metric_brand, 
            color=metric_brand, color_continuous_scale=["#c7d2fe", "#6366f1", "#4338ca"]
        )
        fig_b_models.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False)
        fig_b_models = apply_plotly_mobile_lock(fig_b_models)
        st.plotly_chart(fig_b_models, config=PLOTLY_CONFIG)

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
        colors = ["#4f46e5", "#10b981", "#f59e0b", "#0ea5e9", "#ef4444"]

        for i, model in enumerate(sel_models):
            model_df = m_data[m_data["Label"] == model]
            fig.add_trace(go.Scatter(
                x=model_df["Период"], y=model_df[metric_tab1], name=model, mode="lines+markers+text",
                text=model_df[metric_tab1], textposition="top center", textfont=dict(size=14, color=colors[i % len(colors)]),
                line=dict(width=3, shape="spline", color=colors[i % len(colors)]), marker=dict(size=8)
            ))

        fig.update_layout(template="plotly_white", height=400, hovermode="x unified", legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), margin=dict(t=20, l=10, r=10, b=30), dragmode=False)
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig, config=PLOTLY_CONFIG)

with tab_new:
    st.markdown(f'<div class="section-title">Пазарен дял и лидери (НОВИ МПС) <span style="font-size:0.85rem; color:#64748b; font-weight:normal;">| Период: {period_label_full}</span></div>', unsafe_allow_html=True)

    df_new_agg = df_working.groupby(["Brand", "Model"])["Нови"].sum().reset_index()
    total_new_market = df_new_agg["Нови"].sum()
    
    accent_new = "#10b981" 
    green_gradient = ["#a7f3d0", "#10b981", "#047857"]

    if total_new_market == 0:
        st.info(f"Няма регистрирани нови МПС от тази категория за периода {period_label_full}.")
    else:
        brand_totals_new = df_new_agg.groupby("Brand")["Нови"].sum().sort_values(ascending=False)
        leader_brand, leader_units = brand_totals_new.index[0], brand_totals_new.iloc[0]
        prev_total_new = df_prev["Нови"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо нови", fmt_num(total_new_market), accent=accent_new)
        render_kpi_growth(k2, "Ръст (YoY)", total_new_market, prev_total_new, accent=accent_new)
        kpi_card(k3, "Пазарен лидер", leader_brand, sub=f"Дял: {leader_units/total_new_market:.1%}", accent=accent_new)
        kpi_card(k4, "Активни марки", str(df_new_agg['Brand'].nunique()), accent=accent_new)

        st.markdown("<br>", unsafe_allow_html=True)
        render_yoy_trend_chart(df_working, df_prev, "Нови", "Тренд Нови МПС: Текуща спрямо Предходна година", "yoy_new", color_curr=accent_new)
        
        col_m1, col_m2 = st.columns([1, 1])
        top_brands_new = brand_totals_new.reset_index().head(15)
        fig_b_new = px.bar(top_brands_new.sort_values("Нови"), x="Нови", y="Brand", orientation="h", title="Топ 15 Марки", text="Нови", color="Нови", color_continuous_scale=green_gradient)
        fig_b_new.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False)
        fig_b_new = apply_plotly_mobile_lock(fig_b_new)
        col_m1.plotly_chart(fig_b_new, config=PLOTLY_CONFIG)

        top_models_new = df_new_agg.sort_values("Нови", ascending=False).head(15).copy()
        top_models_new["Име"] = (top_models_new["Brand"] + " " + top_models_new["Model"]).astype(str)
        fig_m_new = px.bar(top_models_new.sort_values("Нови"), x="Нови", y="Име", orientation="h", title="Топ 15 Модели", text="Нови", color="Нови", color_continuous_scale=green_gradient)
        fig_m_new.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False)
        fig_m_new = apply_plotly_mobile_lock(fig_m_new)
        col_m2.plotly_chart(fig_m_new, config=PLOTLY_CONFIG)

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
    
    accent_used = "#0ea5e9"
    blue_gradient = ["#bae6fd", "#0ea5e9", "#0369a1"]

    if total_used_market == 0:
        st.info(f"Няма данни за вторичния пазар за периода {period_label_full}.")
    else:
        brand_totals_used = df_used_agg.groupby("Brand")["Вторичен Пазар"].sum().sort_values(ascending=False)
        leader_brand_u, leader_units_u = brand_totals_used.index[0], brand_totals_used.iloc[0]
        prev_total_used = df_prev["Вторичен Пазар"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо вторичен пазар", fmt_num(total_used_market), accent=accent_used)
        render_kpi_growth(k2, "Ръст (YoY)", total_used_market, prev_total_used, accent=accent_used)
        kpi_card(k3, "Пазарен лидер", leader_brand_u, sub=f"Дял: {leader_units_u/total_used_market:.1%}", accent=accent_used)
        kpi_card(k4, "Активни марки", str(df_used_agg['Brand'].nunique()), accent=accent_used)

        st.markdown("<br>", unsafe_allow_html=True)
        render_yoy_trend_chart(df_working, df_prev, "Вторичен Пазар", "Тренд Вторичен Пазар: Текуща спрямо Предходна година", "yoy_used", color_curr=accent_used)
        
        col_u1, col_u2 = st.columns([1, 1])
        top_brands_used = brand_totals_used.reset_index().head(15)
        fig_b_used = px.bar(top_brands_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Brand", orientation="h", title="Топ 15 Марки", text="Вторичен Пазар", color="Вторичен Пазар", color_continuous_scale=blue_gradient)
        fig_b_used.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False)
        fig_b_used = apply_plotly_mobile_lock(fig_b_used)
        col_u1.plotly_chart(fig_b_used, config=PLOTLY_CONFIG)

        top_models_used = df_used_agg.sort_values("Вторичен Пазар", ascending=False).head(15).copy()
        top_models_used["Име"] = (top_models_used["Brand"] + " " + top_models_used["Model"]).astype(str)
        fig_m_used = px.bar(top_models_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Име", orientation="h", title="Топ 15 Модели", text="Вторичен Пазар", color="Вторичен Пазар", color_continuous_scale=blue_gradient)
        fig_m_used.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False)
        fig_m_used = apply_plotly_mobile_lock(fig_m_used)
        col_u2.plotly_chart(fig_m_used, config=PLOTLY_CONFIG)

        st.markdown("##### Детайлна справка (Вторичен Пазар)")
        market_table_used = df_used_agg[df_used_agg["Вторичен Пазар"] > 0].sort_values("Вторичен Пазар", ascending=False).copy()
        market_table_used["Дял %"] = (market_table_used["Вторичен Пазар"] / total_used_market) * 100

        st.dataframe(market_table_used, hide_index=True, width="stretch", column_config={
            "Употребявани": st.column_config.NumberColumn("Нов Внос", format="%d"),
            "Пререгистрации": st.column_config.NumberColumn("Смяна на собственост", format="%d"),
            "Вторичен Пазар": st.column_config.NumberColumn("Общо Вторичен Пазар", format="%d"),
            "Дял %": st.column_config.ProgressColumn("Пазарен Дял", format="%.2f%%", min_value=0, max_value=market_table_used["Дял %"].max())
        })
