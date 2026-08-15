import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ====================================================================================
# AUTO MOTO SALES BG - DASHBOARD PANEL EDITION (V15 - Perfectly Aligned BI)
# ====================================================================================

st.set_page_config(page_title="AUTO MOTO SALES BG", page_icon="📊", layout="wide")

# ----------------------------------------------------------------------------------
# ДИЗАЙН ТОКЕНИ (цвят / типография)
# ----------------------------------------------------------------------------------
TAB_ACCENT_OVERVIEW = "#0f5257" # тийл - раздел ОБЗОР
TAB_ACCENT_BRAND = "#0f5257"    # тъмен петрол-тийл - раздел МАРКИ
TAB_ACCENT_MODEL = "#334155"    # неутрален графит - раздел МОДЕЛИ
TAB_ACCENT_NEW = "#b45309"      # кехлибар/ръжда - раздел НОВИ
TAB_ACCENT_USED = "#2563a6"     # стоманено синьо - раздел ВТОРИЧЕН ПАЗАР

CHART_FONT = dict(family="Manrope, sans-serif", size=12, color="#14181f")
TITLE_FONT = dict(family="Oswald, sans-serif", size=15, color="#14181f")
BRAND_HEATMAP_SCALE = [
    [0.0, "#dcece9"],
    [0.25, "#a8d3cb"],
    [0.5, "#5fa39c"],
    [0.75, "#1f6b66"],
    [1.0, "#0f5257"]
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root {
    color-scheme: light;
    --ink: #10141c;
    --panel: #101a23;
    --panel-2: #16232e;
    --slate: #64748b;
    --border: #e7eaf0;
    --surface: #ffffff;
    --app-bg: #f5f6f8;
    --brand: #0f5257;
    --brand-glow: #14b8a6;
    --amber: #b45309;
    --steel: #2563a6;
    --success: #059669;
    --danger: #b91c1c;
    --muted: #94a3b8;

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 22px;

    --shadow-sm: 0 1px 2px rgba(16,24,40,0.05);
    --shadow-md: 0 8px 20px -6px rgba(16,24,40,0.12), 0 2px 6px -2px rgba(16,24,40,0.06);
    --shadow-lg: 0 20px 40px -12px rgba(16,24,40,0.22);
}

html, body, [class*="css"] { font-family: 'Manrope', sans-serif; background-color: var(--app-bg); color: var(--ink); }

*:focus-visible { outline: 2px solid var(--brand); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }

/* HERO / DASHBOARD PANEL */
.hero-container {
    background:
        radial-gradient(120% 160% at 100% 0%, rgba(20,184,166,0.22) 0%, rgba(16,26,35,0) 55%),
        linear-gradient(135deg, #101a23 0%, #16232e 60%, #16232e 100%);
    border-radius: var(--radius-xl);
    padding: 1.85rem 2.4rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hero-container::after {
    content: "";
    position: absolute; left: 0; right: 0; bottom: 0; height: 3px;
    background: linear-gradient(90deg, var(--amber), var(--brand-glow));
}
.hero-left { display: flex; align-items: center; gap: 20px; }
.hero-logo-box {
    background: rgba(180, 83, 9, 0.15);
    color: var(--amber);
    border: 1px solid rgba(180, 83, 9, 0.35);
    border-radius: 10px;
    padding: 12px;
    display: flex; align-items: center; justify-content: center;
}
.hero-title {
    font-family: 'Oswald', sans-serif;
    font-size: 2.1rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.02em; color: #ffffff; margin: 0; line-height: 1.1;
}
.hero-sub { font-size: 0.92rem; color: #97a1b0; margin-top: 6px; font-weight: 500; }
.hero-right { display: flex; gap: 12px; }
.meta-badge {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px; padding: 10px 16px; text-align: right;
}
.meta-label { font-size: 0.68rem; color: #97a1b0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }
.meta-value { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #f5c992; font-weight: 600; margin-top: 3px; }
.status-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e; margin-right: 7px; box-shadow: 0 0 6px rgba(34,197,94,.8);
}

/* KPI CARDS */
.kpi-card {
    position: relative; overflow: hidden;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.15rem 1.3rem 1.05rem 1.4rem;
    box-shadow: var(--shadow-sm);
    height: 100%; min-height: 128px;
    display: flex; flex-direction: column; justify-content: center;
    transition: box-shadow .18s ease, transform .18s ease;
}
.kpi-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.kpi-card::before {
    content: ""; position: absolute; top: 0; left: 0; bottom: 0; width: 4px;
    background: var(--tab-accent, var(--brand));
}
.kpi-label { font-size: 0.72rem; color: var(--slate); font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; }
.kpi-value-wrap { margin-top: 0.45rem; }
.kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 700; color: var(--ink); letter-spacing: -0.01em; font-variant-numeric: tabular-nums; }
.kpi-sub { font-size: 0.8rem; font-weight: 600; margin-top: 8px; min-height: 1.2em; }

/* CHART CARD WRAPPER */
[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 0.6rem 0.6rem 0.1rem;
    box-shadow: var(--shadow-sm);
}

/* SECTION TITLES */
.section-title {
    font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 0.02em;
    font-size: 1.1rem; font-weight: 600; color: var(--ink);
    margin: 1.2rem 0 0.8rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 0.55rem;
}
.section-title::before { content: ""; width: 4px; height: 18px; border-radius: 3px; background: var(--tab-accent, var(--brand)); flex-shrink: 0; }

/* TABS - УГОЛЕМЕНИ И ИЗПЪКВАЩИ ГЛАВНИ ТАБОВЕ */
div[data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid var(--border);
    padding-bottom: 2px;
    margin-bottom: 1rem;
}
button[role="tab"] {
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    color: var(--slate) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 10px 18px !important;
    margin-right: 12px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all .18s ease;
}
button[role="tab"][aria-selected="true"] {
    color: var(--brand) !important;
    border-bottom: 3px solid var(--amber) !important;
    background: rgba(15, 82, 87, 0.05) !important;
}
button[role="tab"]:hover {
    color: var(--ink) !important;
    background: rgba(15, 82, 87, 0.08) !important;
}

/* PILLS */
[data-testid="stPills"] button[aria-pressed="true"],
[data-testid="stPills"] button[aria-checked="true"] {
    background: var(--brand) !important;
    color: #fff !important;
    border-color: var(--brand) !important;
}

/* MULTISELECT ТАГОВЕ */
[data-baseweb="tag"] {
    background-color: rgba(15, 82, 87, 0.10) !important;
    border: 1px solid rgba(15, 82, 87, 0.35) !important;
    border-radius: 8px !important;
    color: #0f5257 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    padding: 1px 4px !important;
}
[data-baseweb="tag"] svg { fill: #0f5257 !important; }
[data-baseweb="tag"]:hover { background-color: rgba(15, 82, 87, 0.18) !important; }

[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: var(--border) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 1px rgba(15,82,87,0.25) !important;
}

/* DATA TABLES */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }

/* MOBILE / RESPONSIVE FIX */
@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] { overflow-x: hidden !important; }
    [data-testid="stMainBlockContainer"] { padding-left: 0.75rem !important; padding-right: 0.75rem !important; max-width: 100% !important; }

    .hero-container { flex-direction: column; text-align: center; padding: 1.25rem 0.85rem; gap: 14px; }
    .hero-left { flex-direction: column; gap: 10px; }
    .hero-title { font-size: 1.5rem; line-height: 1.15; }
    .hero-sub { font-size: 0.82rem; }
    .hero-right { flex-direction: column; width: 100%; align-items: stretch; text-align: center; gap: 8px; }
    .meta-badge { text-align: center; padding: 8px 10px; }

    [data-testid="stHorizontalBlock"], div[data-testid="stHorizontalBlock"], .stHorizontalBlock {
        flex-direction: column !important; flex-wrap: nowrap !important; width: 100% !important; gap: 0.85rem !important; align-items: stretch !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"], [data-testid="stHorizontalBlock"] > div[data-testid="column"], .stHorizontalBlock > div {
        width: 100% !important; min-width: 100% !important; max-width: 100% !important; flex: 1 1 100% !important;
    }

    .kpi-card { width: 100% !important; box-sizing: border-box !important; margin-bottom: 0 !important; min-height: 100px; padding: 1rem; }
    .kpi-value { font-size: 1.3rem; }

    div[data-baseweb="tab-list"] {
        display: flex !important; flex-wrap: nowrap !important;
        overflow-x: auto !important; overflow-y: hidden !important;
        width: 100% !important; max-width: 100% !important;
        gap: 4px !important; padding: 4px 2px 8px 2px !important;
        scrollbar-width: none !important; -webkit-overflow-scrolling: touch !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar { display: none !important; }
    div[data-baseweb="tab-list"] > div { display: flex !important; flex-wrap: nowrap !important; width: max-content !important; min-width: max-content !important; }

    button[role="tab"] { flex: 0 0 auto !important; width: auto !important; min-width: max-content !important; white-space: nowrap !important; padding: 9px 12px !important; margin-right: 10px !important; font-size: 0.95rem !important; line-height: 1.2 !important; }
    button[role="tab"] p { white-space: nowrap !important; overflow: visible !important; text-overflow: clip !important; margin: 0 !important; }

    [data-testid="stPills"] { max-width: 100% !important; overflow-x: auto !important; overflow-y: hidden !important; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    [data-testid="stPills"]::-webkit-scrollbar { display: none; }

    [data-testid="stPlotlyChart"] { max-width: 100% !important; width: 100% !important; overflow: visible !important; }
    .js-plotly-plot, .plot-container { max-width: 100% !important; width: 100% !important; overflow-x: hidden !important; overflow-y: visible !important; }
    [data-testid="stDataFrame"] { max-width: 100% !important; overflow-x: auto !important; }

    .section-title { font-size: 1rem; line-height: 1.35; margin-top: 1rem; }
    .stMarkdown, .stText, label, p, h1, h2, h3, h4, h5, h6 { max-width: 100%; overflow-wrap: anywhere; }
}
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

svg_logo = """
<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
<div class="hero-sub">Портал за анализ на регистрациите на МПС</div>
</div>
</div>
<div class="hero-right">
<div class="meta-badge">
<div class="meta-label">Статус на системата</div>
<div class="meta-value"><span class="status-dot"></span>Данни: 04.2022 до 07.2026</div>
</div>
<div class="meta-badge">
<div class="meta-label">Източник</div>
<div class="meta-value">Официални данни КАТ</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# ПОМОЩНИ ФУНКЦИИ И КОНФИГУРАЦИИ ЗА ПЛОТЛИ
# ----------------------------------------------------------------------------------
PLOTLY_CONFIG = {'displayModeBar': False, 'scrollZoom': False}

def apply_plotly_mobile_lock(fig):
    fig.update_layout(
        dragmode=False, font=CHART_FONT,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e7eaf0", font=dict(family="Manrope, sans-serif", size=12, color="#10141c"))
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True, type='category')
    fig.update_traces(textfont_size=15, textposition="outside", cliponaxis=False, marker=dict(line=dict(width=0), cornerradius=6))
    return fig

def kpi_card(col, label, value, sub=None, sub_color="#64748b", accent="#0f5257"):
    sub_html = f'<div class="kpi-sub" style="color:{sub_color};">{sub}</div>' if sub else '<div class="kpi-sub">&nbsp;</div>'
    col.markdown(
        f'<div class="kpi-card" style="--tab-accent:{accent};">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value-wrap"><span class="kpi-value">{value}</span></div>'
        f'{sub_html}</div>',
        unsafe_allow_html=True
    )

def hex_to_rgba(hex_color, alpha=0.14):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def fmt_num(x): return f"{x:,.0f}".replace(",", " ")

def get_growth_data(current, previous):
    if previous is None or pd.isna(previous) or previous == 0: return None
    return (current - previous) / previous * 100

def render_kpi_growth(col, label, current_total, prev_total, accent, prev_label="предходна година"):
    growth_pct = get_growth_data(current_total, prev_total)
    sub_text = f"спрямо {prev_label}" if prev_label else "спрямо предходен период"
    if growth_pct is None:
        kpi_card(col, label, "—", sub="Няма данни", sub_color="#94a3b8", accent="#94a3b8")
    elif growth_pct >= 0:
        kpi_card(col, label, f"+{growth_pct:.1f}%", sub=f"▲ {sub_text}", sub_color="#059669", accent=accent)
    else:
        kpi_card(col, label, f"{growth_pct:.1f}%", sub=f"▼ {sub_text}", sub_color="#b91c1c", accent=accent)

def render_multi_year_yoy_chart(df_input, metric, title, key, primary_color="#0f5257"):
    if df_input.empty:
        st.info("Няма налични данни за избрания филтър.")
        return

    agg_df = df_input.groupby(["Година", "Месец"])[metric].sum().reset_index()
    month_names = {1:"Яну", 2:"Фев", 3:"Мар", 4:"Апр", 5:"Май", 6:"Юни", 7:"Юли", 8:"Авг", 9:"Сеп", 10:"Окт", 11:"Ное", 12:"Дек"}
    agg_df["Месец_Име"] = agg_df["Месец"].map(month_names)

    fig = go.Figure()
    years = sorted(agg_df["Година"].unique())
    
    color_map = {2026: primary_color, 2025: "#2563a6", 2024: "#b45309", 2023: "#64748b", 2022: "#94a3b8"}
    past_colors = ["#94a3b8", "#64748b", "#475569", "#2563a6", "#3b82f6", "#b45309"]

    max_val = agg_df[metric].max() if not agg_df.empty else 10

    for idx, yr in enumerate(years):
        yr_data = agg_df[agg_df["Година"] == yr].sort_values("Месец")
        is_latest = (yr == max(years))
        
        line_color = color_map.get(yr, past_colors[idx % len(past_colors)])
        line_width = 3.5 if is_latest else 2
        line_dash = "solid" if is_latest else "dot"
        
        fig.add_trace(go.Scatter(
            x=yr_data["Месец_Име"], y=yr_data[metric], name=str(yr),
            mode="lines+markers+text" if is_latest else "lines+markers",
            text=yr_data[metric] if is_latest else None,
            textposition="top center", textfont=dict(size=13, color=line_color),
            line=dict(color=line_color, width=line_width, dash=line_dash, shape="spline"),
            marker=dict(size=7 if is_latest else 5),
            fill="tozeroy" if is_latest else None,
            fillcolor=hex_to_rgba(line_color, 0.12) if is_latest else None,
            hovertemplate="%{y:,.0f} бр.<extra>%{fullData.name}</extra>"
        ))

    fig.update_layout(
        title=dict(text=title.upper(), font=TITLE_FONT),
        template="plotly_white", height=380, dragmode=False, font=CHART_FONT,
        hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e7eaf0", font=dict(family="Manrope, sans-serif", size=12, color="#10141c")),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"), margin=dict(t=65, l=10, r=10, b=30)
    )

    fig.update_xaxes(fixedrange=True, categoryorder='array', categoryarray=list(month_names.values()))
    fig.update_yaxes(fixedrange=True, range=[0, max_val * 1.18 if max_val > 0 else 10])
    fig.update_traces(cliponaxis=False)

    st.plotly_chart(fig, config=PLOTLY_CONFIG, key=key, width="stretch")

# ----------------------------------------------------------------------------------
# ЗАРЕЖДАНЕ НА PARQUET БАЗАТА ДАННИ И ФИЛТРИРАНЕ НА СТАРТОВАТА АНОМАЛИЯ (03.2022)
# ----------------------------------------------------------------------------------
@st.cache_data
def load_data():
    parquet_file = os.path.join("data", "kat_data_clean.parquet")
    if not os.path.exists(parquet_file):
        st.error("Файлът 'data/kat_data_clean.parquet' липсва! Моля, качете го в GitHub.")
        st.stop()
    df = pd.read_parquet(parquet_file)
    
    # ПРЕМАХВАНЕ НА СТАРТОВАТА АНОМАЛИЯ 03.2022 (КАТ натрупан стартов месец)
    df = df[df["Sort_Index"] != 202203].copy()
    return df

df_all_categories = load_data()
VEHICLE_CATEGORIES_KEYS = list(df_all_categories["Категория_Име"].unique())

# ----------------------------------------------------------------------------------
# ПРЕМАХНАТО ПРАЗНОТО ПРОСТРАНСТВО: БАЛАНСИРАН И КОМПАКТЕН БЛОК С ФИЛТРИ
# ----------------------------------------------------------------------------------
st.markdown("##### Изберете категория")
selected_cat = st.pills(
    "Категория", 
    options=VEHICLE_CATEGORIES_KEYS, 
    default=VEHICLE_CATEGORIES_KEYS[0], 
    label_visibility="collapsed",
    key="pill_category_main"
)

if not selected_cat: 
    st.stop()

# Вземаме данните за избраната категория
df_full = df_all_categories[df_all_categories["Категория_Име"] == selected_cat].copy()

# ПОДГОТВЯМЕ МЕТРИКИТЕ В ГЛОБАЛНИЯ DF
df_full["Нови"] = df_full["Нови_Месец"]
df_full["Употребявани"] = df_full["Употр_Месец"]
df_full["Пререгистрации"] = df_full["Други_Месец"]
df_full["Вторичен Пазар"] = df_full["Употребявани"] + df_full["Пререгистрации"]
df_full["Всички"] = df_full["Нови"] + df_full["Вторичен Пазар"]

available_years = sorted(df_full["Година"].unique().tolist(), reverse=True)
unique_periods = df_full[["Sort_Index", "Период"]].drop_duplicates().sort_values("Sort_Index")
p_opts = unique_periods["Sort_Index"].tolist()
p_lbls = unique_periods["Период"].tolist()
period_lookup = dict(zip(p_opts, p_lbls))

col_mode_sub, col_years_sub = st.columns([1, 1])

with col_mode_sub:
    st.markdown("##### Времеви режим")
    analysis_mode = st.radio(
        "Режим:",
        options=["Година спрямо Година (YoY)", "Избран диапазон (Период)"],
        horizontal=True,
        label_visibility="collapsed"
    )

with col_years_sub:
    st.markdown("##### Времеви прозорец (Години)")
    if analysis_mode == "Година спрямо Година (YoY)":
        # DEFAULT: 2026 и 2025
        default_yrs = [y for y in [2026, 2025] if y in available_years]
        if not default_yrs and available_years: default_yrs = [available_years[0]]

        selected_years = st.multiselect(
            "Избери години за сравнение:", 
            options=available_years, 
            default=default_yrs,
            label_visibility="collapsed"
        )
        if not selected_years:
            st.warning("Моля, изберете поне една година.")
            st.stop()

        df_working = df_full[df_full["Година"].isin(selected_years)].copy()

        latest_year = max(selected_years)
        prev_year = latest_year - 1
        latest_months = df_full[df_full["Година"] == latest_year]["Месец"].unique()

        df_kpi_curr = df_full[df_full["Година"] == latest_year].copy()

        if prev_year in available_years:
            df_prev = df_full[(df_full["Година"] == prev_year) & (df_full["Месец"].isin(latest_months))].copy()
            has_prev_period = True
            prev_period_label = f"{prev_year} (същите месеци)"
        else:
            df_prev = pd.DataFrame(columns=list(df_full.columns))
            has_prev_period = False
            prev_period_label = None

        period_label_full = f"{latest_year} YTD" if len(latest_months) < 12 else f"{latest_year}"

    else:
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

        df_working = df_full[(df_full["Sort_Index"] >= start_idx) & (df_full["Sort_Index"] <= end_idx)].copy()
        df_kpi_curr = df_working.copy()

        selected_sort_indices = sorted(df_working["Sort_Index"].unique().tolist())
        prev_sort_indices = sorted([s - 100 for s in selected_sort_indices if (s - 100) in period_lookup])
        has_prev_period = len(prev_sort_indices) > 0

        if has_prev_period:
            df_prev = df_full[df_full["Sort_Index"].isin(prev_sort_indices)].copy()
            prev_labels = [period_lookup[s] for s in prev_sort_indices]
            prev_period_label = f"{prev_labels[0]} - {prev_labels[-1]}" if len(prev_labels) > 1 else prev_labels[0]
        else:
            df_prev = pd.DataFrame(columns=list(df_working.columns))
            prev_period_label = None

        start_period_str = unique_periods[unique_periods["Sort_Index"] == start_idx]["Период"].values[0]
        end_period_str = unique_periods[unique_periods["Sort_Index"] == end_idx]["Период"].values[0]
        period_label_full = f"{start_period_str} - {end_period_str}" if start_period_str != end_period_str else start_period_str

st.markdown("---")

# ----------------------------------------------------------------------------------
# ТАБОВЕ ЗА АНАЛИЗ (ГОЛЕМИ И ИЗПЪКВАЩИ ЗАГЛАВИЯ)
# ----------------------------------------------------------------------------------
tab_overview, tab_brand, tab_model, tab_new, tab_used = st.tabs([
    "ОБЗОР", "МАРКИ", "МОДЕЛИ", "НОВИ", "ВТОРИЧЕН"
])

# ====================================================================================
# ТАБ 1: ОБЗОР (ЕКЗЕКУТИВ ПАНЕЛ)
# ====================================================================================
with tab_overview:
    st.markdown(f'<div class="section-title" style="--tab-accent:{TAB_ACCENT_OVERVIEW}">Стратегически анализ върху пазара ({period_label_full})</div>', unsafe_allow_html=True)
    
    col_ov_m, _ = st.columns([1, 1])
    # DEFAULT ПО ПОДРАЗБИРАНЕ -> "Нови"
    metric_overview = col_ov_m.pills(
        "Изследвана метрика за Обзор:", 
        options=["Нови", "Употребявани", "Пререгистрации", "Всички"], 
        default="Нови", 
        key="pill_overview"
    )

    if metric_overview:
        st.markdown("<br>", unsafe_allow_html=True)

        # --- EXECUTIVE SUMMARY ---
        if not df_kpi_curr.empty:
            tot_curr_summary = df_kpi_curr[metric_overview].sum()
            tot_prev_summary = df_prev[metric_overview].sum() if has_prev_period and not df_prev.empty else None
            growth_summary = get_growth_data(tot_curr_summary, tot_prev_summary)

            top_brand_row = df_kpi_curr.groupby("Brand")[metric_overview].sum().sort_values(ascending=False)
            leader_brand_summary = top_brand_row.index[0] if not top_brand_row.empty else "—"

            leader_model_summary, leader_model_growth = None, None
            if not df_prev.empty:
                curr_m = df_kpi_curr.groupby("Label")[metric_overview].sum()
                prev_m = df_prev.groupby("Label")[metric_overview].sum()
                cmp_m = pd.DataFrame({"Curr": curr_m, "Prev": prev_m}).fillna(0)
                cmp_m = cmp_m[(cmp_m["Curr"] >= 30) & (cmp_m["Prev"] >= 10)]
                if not cmp_m.empty:
                    cmp_m["Growth"] = (cmp_m["Curr"] - cmp_m["Prev"]) / cmp_m["Prev"] * 100
                    cmp_m = cmp_m.sort_values("Growth", ascending=False)
                    leader_model_summary = cmp_m.index[0]
                    leader_model_growth = cmp_m.iloc[0]["Growth"]

            growth_phrase = f"расте с {growth_summary:+.1f}%" if growth_summary is not None else "няма данни за сравнение"
            model_phrase = f" Водещ ръст показва <b>{leader_model_summary}</b> (+{leader_model_growth:.0f}%)." if leader_model_summary else ""

            st.markdown(
                f'<div style="background:linear-gradient(135deg, rgba(15,82,87,0.06), rgba(20,184,166,0.03)); '
                f'border-left:4px solid {TAB_ACCENT_OVERVIEW}; border-radius:10px; padding:14px 18px; '
                f'margin-bottom:1.1rem; font-size:0.95rem; color:#334155; line-height:1.5;">'
                f'📊 Пазарът в категорията <b>{selected_cat}</b> за {period_label_full} {growth_phrase} спрямо {prev_period_label or "предходния период"}, '
                f'воден от <b>{leader_brand_summary}</b> като лидер по обем.{model_phrase}'
                f'</div>', unsafe_allow_html=True
            )

        # 1. РАДАР ЗА РАСТЕЖ И ПЕЧЕЛИВШИ / ГУБЕЩИ (2 СИМЕТРИЧНИ КОЛОНИ)
        col_ov1, col_ov2 = st.columns(2)

        # 1.1. РАДАР ЗА РАСТЕЖ (ТОП 15 МОДЕЛА)
        with col_ov1:
            if not df_kpi_curr.empty and not df_prev.empty:
                curr_models = df_kpi_curr.groupby("Label")[metric_overview].sum()
                prev_models = df_prev.groupby("Label")[metric_overview].sum()

                comp_df = pd.DataFrame({"Curr": curr_models, "Prev": prev_models}).fillna(0)
                comp_df = comp_df[(comp_df["Curr"] >= 30) & (comp_df["Prev"] >= 10)].copy()

                if not comp_df.empty:
                    comp_df["Growth_Pct"] = ((comp_df["Curr"] - comp_df["Prev"]) / comp_df["Prev"]) * 100
                    top_momentum = comp_df.sort_values("Growth_Pct", ascending=False).head(15).sort_values("Growth_Pct", ascending=True)

                    fig_mom = go.Figure(go.Bar(
                        x=top_momentum["Growth_Pct"],
                        y=top_momentum.index,
                        orientation="h",
                        text=[f"+{g:.1f}% ({int(c)} бр.)" for g, c in zip(top_momentum["Growth_Pct"], top_momentum["Curr"])],
                        textposition="outside",
                        marker=dict(
                            color=top_momentum["Growth_Pct"],
                            colorscale=["#38bdf8", "#0f5257", "#14b8a6"],
                            line=dict(width=0),
                            cornerradius=6
                        ),
                        hovertemplate="<b>%{y}</b><br>Ръст: +%{x:.1f}%<br>Текущ обем: %{customdata[0]:,.0f} бр.<br>Предходен обем: %{customdata[1]:,.0f} бр.<extra></extra>".replace(",", " "),
                        customdata=top_momentum[["Curr", "Prev"]]
                    ))

                    max_g = top_momentum["Growth_Pct"].max()
                    fig_mom.update_layout(
                        title=dict(text="РАДАР ЗА РАСТЕЖ: ТОП 15 МОДЕЛИ (МИН. 30 БР.)", font=TITLE_FONT),
                        height=580,
                        margin=dict(t=50, l=10, r=80, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=CHART_FONT
                    )
                    fig_mom.update_xaxes(fixedrange=True, range=[0, max_g * 1.3 if max_g > 0 else 100], showgrid=True, gridcolor="#eef1f5")
                    fig_mom.update_yaxes(fixedrange=True)
                    fig_mom = apply_plotly_mobile_lock(fig_mom)
                    st.plotly_chart(fig_mom, config=PLOTLY_CONFIG, width="stretch")
                else:
                    st.info("Няма предостатъчно обем за изчисление на 'Радар за растеж'.")

        # 1.2. ПЕЧЕЛИВШИ И ГУБЕЩИ (ТОП 15)
        with col_ov2:
            if not df_kpi_curr.empty and not df_prev.empty:
                tot_curr = df_kpi_curr[metric_overview].sum()
                tot_prev = df_prev[metric_overview].sum()

                if tot_curr > 0 and tot_prev > 0:
                    curr_b_share = (df_kpi_curr.groupby("Brand")[metric_overview].sum() / tot_curr) * 100
                    prev_b_share = (df_prev.groupby("Brand")[metric_overview].sum() / tot_prev) * 100

                    delta_df = pd.DataFrame({"Share_Curr": curr_b_share, "Share_Prev": prev_b_share}).fillna(0)
                    delta_df["Delta_PP"] = delta_df["Share_Curr"] - delta_df["Share_Prev"]

                    sig_df = delta_df[(delta_df["Share_Curr"] >= 0.2) | (delta_df["Share_Prev"] >= 0.2)].sort_values("Delta_PP", ascending=True)

                    top_losers = sig_df.head(15)
                    top_gainers = sig_df.tail(15)
                    div_df = pd.concat([top_losers, top_gainers]).drop_duplicates().sort_values("Delta_PP", ascending=True)

                    colors_div = ["#059669" if d >= 0 else "#dc2626" for d in div_df["Delta_PP"]]
                    labels_div = [f"+{d:.2f}%" if d >= 0 else f"{d:.2f}%" for d in div_df["Delta_PP"]]

                    fig_div = go.Figure(go.Bar(
                        x=div_df["Delta_PP"],
                        y=div_df.index,
                        orientation="h",
                        text=labels_div,
                        textposition="outside",
                        marker=dict(color=colors_div, line=dict(width=0), cornerradius=5),
                        hovertemplate="<b>%{y}</b><br>Промяна дял: %{x:+.2f}%<br>Текущ дял: %{customdata[0]:.2f}%<br>Предходен дял: %{customdata[1]:.2f}%<extra></extra>",
                        customdata=div_df[["Share_Curr", "Share_Prev"]]
                    ))

                    max_val_abs = max(abs(div_df["Delta_PP"].min()), abs(div_df["Delta_PP"].max()))
                    x_bound = max(1.2, max_val_abs * 1.15)

                    fig_div.update_layout(
                        title=dict(text="ПЕЧЕЛИВШИ И ГУБЕЩИ ПАЗАРЕН ДЯЛ (ТОП 15)", font=TITLE_FONT),
                        height=580,
                        margin=dict(t=50, l=10, r=65, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=CHART_FONT
                    )
                    fig_div.update_xaxes(fixedrange=True, range=[-x_bound, x_bound], showgrid=True, gridcolor="#eef1f5", zeroline=True, zerolinecolor="#cbd5e1")
                    fig_div.update_yaxes(fixedrange=True)
                    fig_div = apply_plotly_mobile_lock(fig_div)
                    st.plotly_chart(fig_div, config=PLOTLY_CONFIG, width="stretch")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. СЕЗОННОСТ И МЕСЕЧНА ИНТЕНЗИВНОСТ (HEATMAPS)
        st.markdown(f'<div class="section-title" style="--tab-accent:#0284c7">Сезонност и месечна интензивност</div>', unsafe_allow_html=True)
        
        col_hm1, col_hm2 = st.columns(2)
        month_names_dict = {1:"Яну", 2:"Фев", 3:"Мар", 4:"Апр", 5:"Май", 6:"Юни", 7:"Юли", 8:"Авг", 9:"Сеп", 10:"Окт", 11:"Ное", 12:"Дек"}

        # 2.1. HEATMAP: ГОДИНИ x МЕСЕЦИ
        with col_hm1:
            if not df_full.empty:
                pivot_yr_m = df_full.groupby(["Година", "Месец"])[metric_overview].sum().unstack(level=1)
                pivot_yr_m.columns = [month_names_dict.get(m, m) for m in pivot_yr_m.columns]
                    text_matrix_hm1 = pivot_yr_m.map(lambda v: "н/д" if pd.isna(v) else fmt_num(v))

                fig_hm1 = px.imshow(
                    pivot_yr_m,
                    labels=dict(x="Месец", y="Година", color="Обем"),
                    x=pivot_yr_m.columns,
                    y=[str(y) for y in pivot_yr_m.index],
                    color_continuous_scale=BRAND_HEATMAP_SCALE,
                    aspect="auto",
                    title=f"СЕЗОННА ТОПЛИННА КАРТА ПО ГОДИНИ ({metric_overview.upper()})"
                )
                fig_hm1.update_traces(text=text_matrix_hm1.values, texttemplate="%{text}")
                fig_hm1.update_layout(
                    title=dict(font=TITLE_FONT),
                    height=380,
                    margin=dict(t=50, l=10, r=10, b=10),
                    font=CHART_FONT,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    coloraxis_showscale=False
                )
                fig_hm1.update_xaxes(fixedrange=True)
                fig_hm1.update_yaxes(fixedrange=True, type='category')
                st.plotly_chart(fig_hm1, config=PLOTLY_CONFIG, width="stretch")

        # 2.2. HEATMAP: ТОП 12 МАРКИ x МЕСЕЦИ (БЕЗ РАЗМЕСТВАЩА СКАЛА/СКРОЛБАР)
        with col_hm2:
            if not df_kpi_curr.empty:
                top_12_b = df_kpi_curr.groupby("Brand")[metric_overview].sum().nlargest(12).index.tolist()
                df_top12 = df_kpi_curr[df_kpi_curr["Brand"].isin(top_12_b)]
                
                pivot_b_m = df_top12.groupby(["Brand", "Месец"])[metric_overview].sum().unstack(level=1).fillna(0)
                pivot_b_m = pivot_b_m.reindex(top_12_b)
                pivot_b_m.columns = [month_names_dict.get(m, m) for m in pivot_b_m.columns]

                fig_hm2 = px.imshow(
                    pivot_b_m,
                    labels=dict(x="Месец", y="Марка", color="Обем"),
                    x=pivot_b_m.columns,
                    y=pivot_b_m.index,
                    color_continuous_scale = BRAND_HEATMAP_SCALE,
                    text_auto=".0f",
                    aspect="auto",
                    title=f"МЕСЕЧНА ИНТЕНЗИВНОСТ НА ТОП 12 МАРКИ ПРЕЗ {period_label_full}"
                )
                fig_hm2.update_layout(
                    title=dict(font=TITLE_FONT),
                    height=380,
                    margin=dict(t=50, l=110, r=10, b=10), # Фиксиран ляв марж за марките
                    font=CHART_FONT,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    coloraxis_showscale=False # Без излишни скали/слайдери отстрани
                )
                fig_hm2.update_xaxes(fixedrange=True)
                fig_hm2.update_yaxes(fixedrange=True, type='category')
                st.plotly_chart(fig_hm2, config=PLOTLY_CONFIG, width="stretch")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. КУМУЛАТИВНА YTD ТРАЕКТОРИЯ
        if not df_working.empty:
            agg_cum = df_working.groupby(["Година", "Месец"])[metric_overview].sum().reset_index()
            agg_cum["Cumulative"] = agg_cum.groupby("Година")[metric_overview].cumsum()

            agg_cum["Месец_Име"] = agg_cum["Месец"].map(month_names_dict)

            fig_cum = go.Figure()
            years_cum = sorted(agg_cum["Година"].unique())
            cum_colors = {2026: "#0f5257", 2025: "#2563a6", 2024: "#b45309", 2023: "#64748b", 2022: "#94a3b8"}

            for yr in years_cum:
                yr_data = agg_cum[agg_cum["Година"] == yr].sort_values("Месец")
                is_latest = (yr == max(years_cum))
                line_color = cum_colors.get(yr, "#64748b")

                fig_cum.add_trace(go.Scatter(
                    x=yr_data["Месец_Име"],
                    y=yr_data["Cumulative"],
                    name=str(yr),
                    mode="lines+markers",
                    line=dict(color=line_color, width=3.5 if is_latest else 2, shape="spline"),
                    marker=dict(size=7 if is_latest else 4),
                    fill="tozeroy" if is_latest else None,
                    fillcolor=hex_to_rgba(line_color, 0.12) if is_latest else None,
                    hovertemplate="%{y:,.0f} бр.<extra>%{fullData.name}</extra>".replace(",", " ")
                ))

            fig_cum.update_layout(
                title=dict(text=f"КУМУЛАТИВНА YTD ТРАЕКТОРИЯ ПО ГОДИНИ ({metric_overview.upper()})", font=TITLE_FONT),
                template="plotly_white", height=380, dragmode=False, font=CHART_FONT,
                hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e7eaf0", font=dict(family="Manrope, sans-serif", size=12, color="#10141c")),
                legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
                margin=dict(t=50, l=10, r=10, b=30)
            )
            fig_cum.update_xaxes(fixedrange=True, categoryorder='array', categoryarray=list(month_names_dict.values()))
            fig_cum.update_yaxes(fixedrange=True)
            st.plotly_chart(fig_cum, config=PLOTLY_CONFIG, width="stretch")


# ====================================================================================
# ТАБ 2: МАРКИ
# ====================================================================================
with tab_brand:
    st.markdown(f'<div class="section-title" style="--tab-accent:{TAB_ACCENT_BRAND}">Цялостен анализ на портфолиото на избрана марка</div>', unsafe_allow_html=True)

    brand_volumes = df_kpi_curr.groupby("Brand")["Всички"].sum()
    top_brands = brand_volumes.nlargest(50).index.tolist()
    other_brands = sorted([b for b in brand_volumes.index if b not in top_brands])
    ordered_brands = top_brands + other_brands

    def format_brand_option(brand):
        vol = brand_volumes.get(brand, 0)
        vol_str = f"{vol:,.0f}".replace(",", " ")
        if brand in top_brands: return f" {brand} ({vol_str})"
        return f"{brand} ({vol_str})"

    default_b = "SKODA" if "SKODA" in ordered_brands else (ordered_brands[0] if ordered_brands else "")

    col_b1, col_b2 = st.columns([1, 2])

    selected_brand = col_b1.selectbox("Избери марка за детайлен преглед:", options=ordered_brands, index=ordered_brands.index(default_b) if default_b in ordered_brands else 0, format_func=format_brand_option)
    metric_brand = st.pills("Изследвана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Нови", key="pill_brand")

    if selected_brand and metric_brand:
        brand_data_kpi = df_kpi_curr[df_kpi_curr["Brand"] == selected_brand]
        brand_data_multi = df_working[df_working["Brand"] == selected_brand]
        brand_data_prev = df_prev[df_prev["Brand"] == selected_brand] if has_prev_period else pd.DataFrame(columns=df_kpi_curr.columns)

        total_market_metric = df_kpi_curr[metric_brand].sum()
        brand_total = brand_data_kpi[metric_brand].sum()
        brand_prev_total = brand_data_prev[metric_brand].sum() if has_prev_period else None
        brand_share = (brand_total / total_market_metric) * 100 if total_market_metric > 0 else 0
        active_models_count = brand_data_kpi[brand_data_kpi[metric_brand] > 0]["Model"].nunique()

        accent_brand = TAB_ACCENT_BRAND
        kb1, kb2, kb3, kb4 = st.columns(4)
        kpi_card(kb1, "Общо продажби", fmt_num(brand_total), accent=accent_brand)
        render_kpi_growth(kb2, "Ръст (YoY)", brand_total, brand_prev_total, accent=accent_brand, prev_label=prev_period_label)
        kpi_card(kb3, "Пазарен дял", f"{brand_share:.1f}%", sub=f"от общо {fmt_num(total_market_metric)}", accent=accent_brand)
        kpi_card(kb4, "Активни модели", str(active_models_count), sub="с регистрации за периода", accent=accent_brand)

        st.markdown("<br>", unsafe_allow_html=True)

        render_multi_year_yoy_chart(df_input=brand_data_multi, metric=metric_brand, title=f"Динамика на продажбите: {metric_brand} за {selected_brand}", key="yoy_brand_chart", primary_color=accent_brand)

        st.markdown(f"**Топ модели на {selected_brand} за периода ({period_label_full})**")
        brand_models = brand_data_kpi.groupby("Model")[metric_brand].sum().reset_index()
        brand_models = brand_models[brand_models[metric_brand] > 0].sort_values(metric_brand, ascending=True).tail(20)
        brand_models["Model"] = brand_models["Model"].astype(str)

        n_models = len(brand_models)
        rank_desc = list(range(n_models, 0, -1))
        bar_colors = ["#14b8a6" if r == 1 else "#0f5257" if r <= 3 else "#bcdfe0" for r in rank_desc]

        fig_b_models = go.Figure(go.Bar(
            x=brand_models[metric_brand],
            y=brand_models["Model"],
            orientation="h",
            text=[fmt_num(v) for v in brand_models[metric_brand]],
            textposition="outside",
            marker=dict(color=bar_colors),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f} бр.<extra></extra>".replace(",", " ")
        ))
        fig_b_models.update_layout(
            title=dict(text=f"ТОП {n_models} МОДЕЛА ({metric_brand.upper()})", font=TITLE_FONT),
            height=max(420, n_models * 27),
            margin=dict(t=55, l=10, r=30, b=10),
            showlegend=False
        )
        fig_b_models = apply_plotly_mobile_lock(fig_b_models)
        fig_b_models.update_traces(textfont=dict(size=13, family="JetBrains Mono, monospace", color="#14181f"))
        fig_b_models.update_xaxes(showgrid=True, gridcolor="#eef1f5", zeroline=False)

        st.plotly_chart(fig_b_models, config=PLOTLY_CONFIG, width="stretch")

# ====================================================================================
# ТАБ 3: МОДЕЛИ
# ====================================================================================
with tab_model:
    st.markdown(f'<div class="section-title" style="--tab-accent:{TAB_ACCENT_MODEL}">Сравнителен анализ на конкретни модели</div>', unsafe_allow_html=True)
    model_volumes = df_working.groupby(["Brand", "Label"])["Всички"].sum().reset_index()
    liquid_models = model_volumes[model_volumes["Всички"] >= 5]

    available_brands_vols = liquid_models.groupby("Brand")["Всички"].sum()
    top_filter_brands = available_brands_vols.nlargest(50).index.tolist()
    other_filter_brands = sorted([b for b in available_brands_vols.index if b not in top_filter_brands])
    ordered_filter_options = ["Всички марки"] + top_filter_brands + other_filter_brands

    def format_filter_brand(b):
        if b == "Всички марки": return "🌐 Всички марки"
        vol = available_brands_vols.get(b, 0)
        vol_str = f"{vol:,.0f}".replace(",", " ")
        if b in top_filter_brands: return f" {b} ({vol_str})"
        return f"{b} ({vol_str})"

    col_f1, col_f2 = st.columns([1, 2])

    sel_brand = col_f1.selectbox("1. Филтър по марка (опционално):", options=ordered_filter_options, format_func=format_filter_brand)

    if sel_brand == "Всички марки": available_labels = sorted(liquid_models["Label"].unique())
    else: available_labels = sorted(liquid_models[liquid_models["Brand"] == sel_brand]["Label"].unique())

    target_models = ["SKODA Kodiaq", "VOLKSWAGEN Tayron", "HYUNDAI Santa Fe", "KIA Sorento"]
    def_models = [l for l in available_labels if any(t in l for t in target_models)]
    if not def_models and available_labels: def_models = [available_labels[0]]

    sel_models = col_f2.multiselect("2. Избери модели за сравнение:", options=available_labels, default=def_models)

    st.markdown("<br>", unsafe_allow_html=True)
    metric_tab1 = st.pills("3. Изследвана метрика:", options=["Нови", "Употребявани", "Пререгистрации", "Всички"], default="Нови", key="pill_model")

    MODEL_COLORS = ["#0f5257", "#b45309", "#2563a6", "#7c3aed", "#be185d", "#0d9488", "#64748b"]

    if sel_models and metric_tab1:
        m_data = df_working[df_working["Label"].isin(sel_models)].sort_values("Sort_Index")
        m_data_kpi = df_kpi_curr[df_kpi_curr["Label"].isin(sel_models)]
        m_data_prev = df_prev[df_prev["Label"].isin(sel_models)] if has_prev_period else pd.DataFrame(columns=df_kpi_curr.columns)

        selection_total = m_data_kpi[metric_tab1].sum()
        selection_prev_total = m_data_prev[metric_tab1].sum() if has_prev_period else None
        category_total = df_kpi_curr[metric_tab1].sum()
        selection_share = (selection_total / category_total * 100) if category_total > 0 else 0

        model_ranking = m_data_kpi.groupby("Label")[metric_tab1].sum().sort_values(ascending=False)
        leader_model = model_ranking.index[0] if not model_ranking.empty else "—"
        leader_units = model_ranking.iloc[0] if not model_ranking.empty else 0

        accent_model = TAB_ACCENT_MODEL
        km1, km2, km3, km4 = st.columns(4)
        kpi_card(km1, "Общо в селекцията", fmt_num(selection_total), accent=accent_model)
        render_kpi_growth(km2, "Ръст (YoY)", selection_total, selection_prev_total, accent=accent_model, prev_label=prev_period_label)
        kpi_card(km3, "Дял от категорията", f"{selection_share:.1f}%", sub=f"от общо {fmt_num(category_total)}", accent=accent_model)
        kpi_card(km4, "Лидер в селекцията", leader_model, sub=f"{fmt_num(leader_units)} бр.", accent=accent_model)

        st.markdown("<br>", unsafe_allow_html=True)

        fig = go.Figure()
        max_val = 0

        for i, model in enumerate(sel_models):
            model_df = m_data[m_data["Label"] == model]
            if model_df.empty:
                continue
            color = MODEL_COLORS[i % len(MODEL_COLORS)]
            max_val = max(max_val, model_df[metric_tab1].max())
            short_name = model.split(" ", 1)[-1]

            fig.add_trace(go.Scatter(
                x=model_df["Период"], y=model_df[metric_tab1], name=short_name, mode="lines+markers",
                line=dict(width=2.75, shape="spline", color=color),
                marker=dict(size=6, color=color),
                customdata=[model] * len(model_df),
                hovertemplate="<b>%{customdata}</b><br>%{y:,.0f} бр.<extra></extra>".replace(",", " ")
            ))

        y_max_range = max_val * 1.15 if max_val > 0 else 10
        legend_rows = 1 if len(sel_models) <= 4 else 2
        bottom_margin = 45 + (legend_rows * 24)

        fig.update_layout(
            template="plotly_white", height=360 + (legend_rows * 24), font=CHART_FONT, hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e7eaf0", font=dict(family="Manrope, sans-serif", size=12, color="#10141c")),
            legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", font=dict(size=11)),
            margin=dict(t=20, l=10, r=15, b=bottom_margin), dragmode=False
        )
        fig.update_xaxes(fixedrange=True, showgrid=False)
        fig.update_yaxes(fixedrange=True, range=[0, y_max_range], showgrid=True, gridcolor="#eef1f5", zeroline=False)
        fig.update_traces(cliponaxis=False)

        st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")

        st.markdown("<br><div class='section-title' style='--tab-accent:#64748b; font-size:0.95rem;'>СТРУКТУРА НА СЕЛЕКЦИЯТА ЗА ПЕРИОДА</div>", unsafe_allow_html=True)

        pc1, pc2 = st.columns(2)

        pie_data_models = m_data_kpi.groupby("Label")[metric_tab1].sum().reset_index()
        pie_data_models = pie_data_models[pie_data_models[metric_tab1] > 0].sort_values(metric_tab1, ascending=False)
        pie_colors_1 = [MODEL_COLORS[sel_models.index(lbl) % len(MODEL_COLORS)] if lbl in sel_models else "#94a3b8" for lbl in pie_data_models["Label"]]

        fig_pie_1 = go.Figure(go.Pie(
            labels=pie_data_models["Label"], values=pie_data_models[metric_tab1], hole=0.62,
            marker=dict(colors=pie_colors_1, line=dict(color="#ffffff", width=2)),
            textinfo="percent", textfont=dict(size=12, family="Manrope, sans-serif")
        ))
        fig_pie_1.update_layout(
            title=dict(text=f"Дял продажби ({metric_tab1})", font=TITLE_FONT, x=0.5),
            margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            font=CHART_FONT, paper_bgcolor='rgba(0,0,0,0)', height=340,
            annotations=[dict(text=f"<b>{fmt_num(selection_total)}</b><br><span style='font-size:11px;color:#64748b'>бр.</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=18, family="JetBrains Mono, monospace", color="#14181f"))]
        )
        pc1.plotly_chart(fig_pie_1, config=PLOTLY_CONFIG, width="stretch")

        total_new = m_data_kpi["Нови"].sum()
        total_used = m_data_kpi["Употребявани"].sum()
        total_rereg = m_data_kpi["Пререгистрации"].sum()
        total_status = total_new + total_used + total_rereg

        status_labels = ["Нови", "Употребявани", "Пререгистрации"]
        status_values = [total_new, total_used, total_rereg]
        status_colors = [TAB_ACCENT_NEW, TAB_ACCENT_USED, "#94b8d4"]

        fig_pie_2 = go.Figure(go.Pie(
            labels=status_labels, values=status_values, hole=0.62,
            marker=dict(colors=status_colors, line=dict(color="#ffffff", width=2)),
            textinfo="percent", textfont=dict(size=12, family="Manrope, sans-serif")
        ))
        fig_pie_2.update_layout(
            title=dict(text="Общо за селекцията", font=TITLE_FONT, x=0.5),
            margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            font=CHART_FONT, paper_bgcolor='rgba(0,0,0,0)', height=340,
            annotations=[dict(text=f"<b>{fmt_num(total_status)}</b><br><span style='font-size:11px;color:#64748b'>бр.</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=18, family="JetBrains Mono, monospace", color="#14181f"))]
        )
        pc2.plotly_chart(fig_pie_2, config=PLOTLY_CONFIG, width="stretch")

# ====================================================================================
# ТАБ 4: НОВИ
# ====================================================================================
with tab_new:
    st.markdown(f'<div class="section-title" style="--tab-accent:{TAB_ACCENT_NEW}">Пазарен дял и лидери (НОВИ МПС) <span style="font-size:0.85rem; color:#64748b; font-weight:normal; text-transform:none; letter-spacing:normal;">| Период: {period_label_full}</span></div>', unsafe_allow_html=True)

    df_new_agg = df_kpi_curr.groupby(["Brand", "Model"])["Нови"].sum().reset_index()
    total_new_market = df_new_agg["Нови"].sum()

    accent_new = TAB_ACCENT_NEW
    amber_gradient = ["#f7d9ae", "#d98a3d", "#b45309"]

    if total_new_market == 0:
        st.info(f"Няма регистрирани нови МПС от тази категория за периода {period_label_full}.")
    else:
        brand_totals_new = df_new_agg.groupby("Brand")["Нови"].sum().sort_values(ascending=False)
        leader_brand, leader_units = brand_totals_new.index[0], brand_totals_new.iloc[0]
        prev_total_new = df_prev["Нови"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо нови", fmt_num(total_new_market), accent=accent_new)
        render_kpi_growth(k2, "Ръст (YoY)", total_new_market, prev_total_new, accent=accent_new, prev_label=prev_period_label)
        kpi_card(k3, "Пазарен лидер", leader_brand, sub=f"Дял: {leader_units/total_new_market:.1%}", accent=accent_new)
        kpi_card(k4, "Активни марки", str(df_new_agg['Brand'].nunique()), accent=accent_new)

        st.markdown("<br>", unsafe_allow_html=True)
        render_multi_year_yoy_chart(df_working, "Нови", "Сравнение на тренда при Нови МПС по години", "yoy_new", primary_color=accent_new)

        col_m1, col_m2 = st.columns([1, 1])
        top_brands_new = brand_totals_new.reset_index().head(15)
        fig_b_new = px.bar(top_brands_new.sort_values("Нови"), x="Нови", y="Brand", orientation="h", title="ТОП 15 МАРКИ", text="Нови", color="Нови", color_continuous_scale=amber_gradient)
        fig_b_new.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False, font=CHART_FONT, title_font=TITLE_FONT)
        fig_b_new = apply_plotly_mobile_lock(fig_b_new)
        col_m1.plotly_chart(fig_b_new, config=PLOTLY_CONFIG, width="stretch")

        top_models_new = df_new_agg.sort_values("Нови", ascending=False).head(15).copy()
        top_models_new["Име"] = (top_models_new["Brand"] + " " + top_models_new["Model"]).astype(str)
        fig_m_new = px.bar(top_models_new.sort_values("Нови"), x="Нови", y="Име", orientation="h", title="ТОП 15 МОДЕЛИ", text="Нови", color="Нови", color_continuous_scale=amber_gradient)
        fig_m_new.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False, font=CHART_FONT, title_font=TITLE_FONT)
        fig_m_new = apply_plotly_mobile_lock(fig_m_new)
        col_m2.plotly_chart(fig_m_new, config=PLOTLY_CONFIG, width="stretch")

        st.markdown("##### Детайлна справка (Нови)")
        market_table_new = df_new_agg[df_new_agg["Нови"] > 0].sort_values("Нови", ascending=False).copy()
        market_table_new["Дял %"] = (market_table_new["Нови"] / total_new_market) * 100

        st.dataframe(market_table_new, hide_index=True, width="stretch", column_config={
            "Нови": st.column_config.NumberColumn("Брой", format="%d"),
            "Дял %": st.column_config.ProgressColumn("Пазарен Дял", format="%.2f%%", min_value=0, max_value=market_table_new["Дял %"].max())
        })

# ====================================================================================
# ТАБ 5: ВТОРИЧЕН ПАЗАР
# ====================================================================================
with tab_used:
    st.markdown(f'<div class="section-title" style="--tab-accent:{TAB_ACCENT_USED}">Вторичен пазар (Употребявани + Пререгистрации) <span style="font-size:0.85rem; color:#64748b; font-weight:normal; text-transform:none; letter-spacing:normal;">| Период: {period_label_full}</span></div>', unsafe_allow_html=True)

    df_used_agg = df_kpi_curr.groupby(["Brand", "Model"])[["Употребявани", "Пререгистрации", "Вторичен Пазар"]].sum().reset_index()
    total_used_market = df_used_agg["Вторичен Пазар"].sum()

    accent_used = TAB_ACCENT_USED
    steel_gradient = ["#c3d9ec", "#5089b8", "#2563a6"]

    if total_used_market == 0:
        st.info(f"Няма данни за вторичния пазар за периода {period_label_full}.")
    else:
        brand_totals_used = df_used_agg.groupby("Brand")["Вторичен Пазар"].sum().sort_values(ascending=False)
        leader_brand_u, leader_units_u = brand_totals_used.index[0], brand_totals_used.iloc[0]
        prev_total_used = df_prev["Вторичен Пазар"].sum() if has_prev_period else None

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "Общо вторичен пазар", fmt_num(total_used_market), accent=accent_used)
        render_kpi_growth(k2, "Ръст (YoY)", total_used_market, prev_total_used, accent=accent_used, prev_label=prev_period_label)
        kpi_card(k3, "Пазарен лидер", leader_brand_u, sub=f"Дял: {leader_units_u/total_used_market:.1%}", accent=accent_used)
        kpi_card(k4, "Активни марки", str(df_used_agg['Brand'].nunique()), accent=accent_used)

        st.markdown("<br>", unsafe_allow_html=True)
        render_multi_year_yoy_chart(df_working, "Вторичен Пазар", "Сравнение на тренда при Вторичен пазар по години", "yoy_used", primary_color=accent_used)

        col_u1, col_u2 = st.columns([1, 1])
        top_brands_used = brand_totals_used.reset_index().head(15)
        fig_b_used = px.bar(top_brands_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Brand", orientation="h", title="ТОП 15 МАРКИ", text="Вторичен Пазар", color="Вторичен Пазар", color_continuous_scale=steel_gradient)
        fig_b_used.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False, font=CHART_FONT, title_font=TITLE_FONT)
        fig_b_used = apply_plotly_mobile_lock(fig_b_used)
        col_u1.plotly_chart(fig_b_used, config=PLOTLY_CONFIG, width="stretch")

        top_models_used = df_used_agg.sort_values("Вторичен Пазар", ascending=False).head(15).copy()
        top_models_used["Име"] = (top_models_used["Brand"] + " " + top_models_used["Model"]).astype(str)
        fig_m_used = px.bar(top_models_used.sort_values("Вторичен Пазар"), x="Вторичен Пазар", y="Име", orientation="h", title="ТОП 15 МОДЕЛИ", text="Вторичен Пазар", color="Вторичен Пазар", color_continuous_scale=steel_gradient)
        fig_m_used.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10), coloraxis_showscale=False, font=CHART_FONT, title_font=TITLE_FONT)
        fig_m_used = apply_plotly_mobile_lock(fig_m_used)
        col_u2.plotly_chart(fig_m_used, config=PLOTLY_CONFIG, width="stretch")

        st.markdown("##### Детайлна справка (Вторичен Пазар)")
        market_table_used = df_used_agg[df_used_agg["Вторичен Пазар"] > 0].sort_values("Вторичен Пазар", ascending=False).copy()
        market_table_used["Дял %"] = (market_table_used["Вторичен Пазар"] / total_used_market) * 100

        st.dataframe(market_table_used, hide_index=True, width="stretch", column_config={
            "Употребявани": st.column_config.NumberColumn("Нов Внос", format="%d"),
            "Пререгистрации": st.column_config.NumberColumn("Смяна на собственост", format="%d"),
            "Вторичен Пазар": st.column_config.NumberColumn("Общо Вторичен Пазар", format="%d"),
            "Дял %": st.column_config.ProgressColumn("Пазарен Дял", format="%.2f%%", min_value=0, max_value=market_table_used["Дял %"].max())
        })
