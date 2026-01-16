"""
Greenland Rare Earth Intelligence Dashboard
============================================
Strategic mineral intelligence for the Arctic's most contested resource frontier.

Author: Maurice McDonald | DFW Plotly Community Leader
Data Sources: GEUS, USGS MRDS, Mining Company Filings

Streamlit App Version
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Greenland REE Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

# Color Palette (FRED-Style / Maurice McDonald Signature)
COLORS = {
    'periwinkle': '#8E9FD5',
    'periwinkle_light': '#B8C4E8',
    'periwinkle_dark': '#6B7FC2',
    'periwinkle_pale': 'rgba(142, 159, 213, 0.15)',
    'charcoal': '#2D3436',
    'charcoal_light': '#636E72',
    'white': '#FFFFFF',
    'grey_100': '#F8F9FA',
    'grey_200': '#E9ECEF',
    'grey_300': '#DEE2E6',
    'danger': '#DC3545',
    'success': '#28A745',
    'warning': '#FFC107',
}

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        font-size: 32px;
        font-weight: bold;
        color: {COLORS['charcoal']};
        margin-bottom: 0;
    }}
    .sub-header {{
        font-size: 16px;
        color: {COLORS['charcoal_light']};
        margin-top: 0;
    }}
    .kpi-card {{
        background-color: {COLORS['grey_100']};
        border-left: 4px solid {COLORS['periwinkle']};
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: bold;
        color: {COLORS['periwinkle']};
        margin: 0;
    }}
    .kpi-label {{
        font-size: 11px;
        color: {COLORS['charcoal_light']};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }}
    .finding-box {{
        background-color: {COLORS['periwinkle_pale']};
        border-left: 4px solid {COLORS['periwinkle']};
        padding: 20px;
        border-radius: 4px;
        margin: 20px 0;
    }}
    .osint-badge {{
        background-color: {COLORS['periwinkle']};
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
    }}
    .stMetric > div {{
        background-color: {COLORS['grey_100']};
        padding: 10px;
        border-radius: 4px;
        border-left: 4px solid {COLORS['periwinkle']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load and prepare the REE deposits dataset"""
    
    data = {
        'deposit_name': ['Tanbreez (Kringlerne)', 'Kvanefjeld', 'Sarfartoq', 'Motzfeldt', 
                       'Ilímaussaq Complex (Other)', 'Tikiusaaq', 'Qeqertaasaq', 'Milne Land',
                       'Niaqornaarsuk', 'Qaqarssuk', 'Kangerlussuaq REE Zone', 'Gardar Province South',
                       'Narsaq Area', 'Ivigtut Area', 'Skaergaard'],
        'latitude': [60.87, 60.98, 66.48, 61.17, 60.95, 64.22, 69.25, 70.75, 
                    60.45, 66.12, 67.02, 60.75, 60.92, 61.20, 68.18],
        'longitude': [-45.88, -45.92, -51.17, -45.08, -45.85, -51.95, -53.50, -26.50,
                     -45.25, -52.75, -50.70, -46.00, -46.08, -48.17, -31.75],
        'resource_mt': [4000, 1010, 8.6, 340, 500, 25, 15, 45, 120, 35, 75, 2000, 180, 50, 65],
        'treo_grade_pct': [0.60, 1.10, 2.00, 0.25, 0.80, 1.50, 0.90, 0.65, 0.45, 1.80, 0.55, 0.70, 0.95, 0.30, 0.25],
        'heavy_ree_pct': [30, 12, 15, 8, 18, 10, 12, 8, 14, 6, 9, 20, 11, 5, 7],
        'owner': ['Critical Metals Corp', 'Energy Transition Minerals', 'Hudson Resources', 
                 'Regency Mines', 'Various', 'Unlicensed', 'Unlicensed', 'GreenRock Resources',
                 'Tanbreez subsidiary', 'NunaMinerals legacy', 'Government reserved', 
                 'Multiple operators', 'ETM subsidiary', 'Historical', 'Platina Resources'],
        'chinese_stake_pct': [0, 9.21, 0, 0, 5, 0, 0, 0, 0, 0, 0, 3, 9.21, 0, 0],
        'status': ['Advancing - US ownership', 'Blocked - Uranium ban', 'Permitted', 
                  'Early exploration', 'Multiple licenses', 'Prospect only', 'Prospect only',
                  'Exploration license', 'Exploration license', 'Abandoned license',
                  'Reserved area', 'Multiple status', 'License uncertainty', 'Depleted/closed', 'PGE focus'],
        'uranium_ppm': [15, 285, 45, 60, 120, 30, 25, 40, 55, 20, 35, 150, 220, 15, 10],
        'strategic_score': [80.0, 52.0, 61.0, 48.0, 58.0, 42.0, 35.0, 40.0, 55.0, 38.0, 45.0, 62.0, 48.0, 25.0, 32.0],
    }
    
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['score_category'] = pd.cut(df['strategic_score'], 
                                   bins=[0, 40, 60, 80, 100], 
                                   labels=['Low', 'Medium', 'High', 'Very High'])
    df['uranium_status'] = df['uranium_ppm'].apply(lambda x: 'Blocked (>100 ppm)' if x > 100 else 'Clear (<100 ppm)')
    df['ownership_type'] = df['chinese_stake_pct'].apply(lambda x: 'Chinese Exposure' if x > 0 else 'Western Control')
    
    return df

# Load data
df = load_data()

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<span class="osint-badge">● OPEN SOURCE INTELLIGENCE</span>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Greenland Rare Earth Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Strategic mineral assessment for the Arctic\'s most contested resource frontier</p>', unsafe_allow_html=True)

with col2:
    st.markdown("**Data Sources**")
    st.caption("GEUS • USGS • SEC Filings")

st.markdown("---")

# ============================================================================
# KPI STRIP
# ============================================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="🗺️ TOTAL DEPOSITS",
        value=str(len(df)),
        delta="Documented REE occurrences"
    )

with kpi2:
    st.metric(
        label="⛏️ TOTAL RESOURCE",
        value=f"{df['resource_mt'].sum()/1000:.1f}B Mt",
        delta="Combined estimate"
    )

with kpi3:
    western_pct = len(df[df['chinese_stake_pct']==0])/len(df)*100
    st.metric(
        label="🇺🇸 WESTERN CONTROL",
        value=f"{western_pct:.0f}%",
        delta=f"{len(df[df['chinese_stake_pct']==0])} of {len(df)} deposits"
    )

with kpi4:
    blocked = len(df[df['uranium_ppm'] > 100])
    st.metric(
        label="⚠️ URANIUM BLOCKED",
        value=str(blocked),
        delta="Deposits >100 ppm U"
    )

st.markdown("")

# ============================================================================
# MAIN CONTENT - MAP AND SCORES
# ============================================================================

map_col, score_col = st.columns([3, 2])

with map_col:
    st.markdown("#### 🗺️ Deposit Locations")
    st.caption("Size = Resource | Color = Strategic Score")
    
    fig_map = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        size='resource_mt',
        color='strategic_score',
        hover_name='deposit_name',
        hover_data={
            'latitude': False,
            'longitude': False,
            'resource_mt': ':.0f',
            'strategic_score': ':.1f',
            'heavy_ree_pct': ':.0f',
            'owner': True,
            'status': True,
            'chinese_stake_pct': ':.1f'
        },
        color_continuous_scale=[
            [0, COLORS['grey_300']],
            [0.5, COLORS['periwinkle_light']],
            [1, COLORS['periwinkle_dark']]
        ],
        size_max=40,
        zoom=2.5,
        center={'lat': 68, 'lon': -42},
        mapbox_style='carto-positron',
        height=450
    )
    
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title='Strategic<br>Score',
            tickfont=dict(size=10),
            titlefont=dict(size=11)
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

with score_col:
    st.markdown("#### 📊 Strategic Score Ranking")
    st.caption("Top deposits by strategic value")
    
    df_sorted = df.sort_values('strategic_score', ascending=True).tail(10)
    
    fig_scores = go.Figure()
    
    fig_scores.add_trace(go.Bar(
        y=df_sorted['deposit_name'],
        x=df_sorted['strategic_score'],
        orientation='h',
        marker=dict(
            color=df_sorted['strategic_score'],
            colorscale=[
                [0, COLORS['grey_300']],
                [0.5, COLORS['periwinkle_light']],
                [1, COLORS['periwinkle']]
            ]
        ),
        text=df_sorted['strategic_score'].round(0).astype(int),
        textposition='outside',
        textfont=dict(size=11, color=COLORS['charcoal']),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    ))
    
    fig_scores.update_layout(
        xaxis=dict(title='Strategic Score', range=[0, 100], gridcolor=COLORS['grey_200']),
        yaxis=dict(title=''),
        margin=dict(l=10, r=50, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400
    )
    
    st.plotly_chart(fig_scores, use_container_width=True)

# ============================================================================
# SECONDARY CHARTS
# ============================================================================

chart1, chart2, chart3 = st.columns([2, 1, 1])

with chart1:
    st.markdown("#### 💎 Resource vs Grade")
    st.caption("Bubble size = Heavy REE %")
    
    fig_scatter = px.scatter(
        df,
        x='resource_mt',
        y='treo_grade_pct',
        size='heavy_ree_pct',
        color='ownership_type',
        hover_name='deposit_name',
        hover_data=['strategic_score', 'owner'],
        color_discrete_map={
            'Western Control': COLORS['periwinkle'],
            'Chinese Exposure': COLORS['danger']
        },
        log_x=True,
        labels={
            'resource_mt': 'Resource (Million Tonnes, log scale)',
            'treo_grade_pct': 'Grade (% TREO)',
            'heavy_ree_pct': 'Heavy REE %'
        },
        height=300
    )
    
    fig_scatter.update_layout(
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(gridcolor=COLORS['grey_200']),
        yaxis=dict(gridcolor=COLORS['grey_200']),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart2:
    st.markdown("#### 🏛️ Ownership")
    st.caption("By resource volume")
    
    western = df[df['chinese_stake_pct'] == 0]['resource_mt'].sum()
    chinese_exposed = df[df['chinese_stake_pct'] > 0]['resource_mt'].sum()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Western Control', 'Chinese Exposure'],
        values=[western, chinese_exposed],
        hole=0.6,
        marker=dict(colors=[COLORS['periwinkle'], COLORS['danger']]),
        textinfo='percent',
        textfont=dict(size=12)
    )])
    
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=9)),
        height=280,
        annotations=[dict(
            text=f'{western/(western+chinese_exposed)*100:.0f}%<br>Western',
            x=0.5, y=0.5,
            font=dict(size=12, color=COLORS['charcoal']),
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with chart3:
    st.markdown("#### ☢️ Uranium Status")
    st.caption("2021 ban impact")
    
    clear = len(df[df['uranium_ppm'] <= 100])
    blocked = len(df[df['uranium_ppm'] > 100])
    
    fig_uranium = go.Figure(data=[go.Bar(
        x=['Clear', 'Blocked'],
        y=[clear, blocked],
        marker=dict(color=[COLORS['success'], COLORS['danger']]),
        text=[clear, blocked],
        textposition='outside',
        textfont=dict(size=14, color=COLORS['charcoal'])
    )])
    
    fig_uranium.update_layout(
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(title=''),
        yaxis=dict(title='Deposits', gridcolor=COLORS['grey_200']),
        height=280
    )
    
    st.plotly_chart(fig_uranium, use_container_width=True)

# ============================================================================
# KEY FINDING
# ============================================================================

st.markdown("""
<div class="finding-box">
    <p style="font-size: 10px; font-weight: bold; color: #6B7FC2; letter-spacing: 1px; margin-bottom: 8px;">KEY FINDING</p>
    <p style="margin: 0; font-size: 14px;">
        <strong>Tanbreez</strong> (80/100) is the most strategically valuable deposit for Western interests. 
        With 30% heavy REE content (highest globally), zero Chinese exposure, 
        and US corporate control, it represents the best opportunity for supply chain diversification.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# DATA TABLE
# ============================================================================

st.markdown("#### 📋 Deposit Details")

st.dataframe(
    df[['deposit_name', 'strategic_score', 'resource_mt', 'treo_grade_pct', 
        'heavy_ree_pct', 'owner', 'chinese_stake_pct', 'status']].sort_values(
        'strategic_score', ascending=False
    ).reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
    column_config={
        'deposit_name': st.column_config.TextColumn('Deposit', width='medium'),
        'strategic_score': st.column_config.NumberColumn('Score', format='%.1f'),
        'resource_mt': st.column_config.NumberColumn('Resource (Mt)', format='%.0f'),
        'treo_grade_pct': st.column_config.NumberColumn('Grade %', format='%.2f'),
        'heavy_ree_pct': st.column_config.NumberColumn('Heavy REE %', format='%.0f'),
        'owner': st.column_config.TextColumn('Owner', width='medium'),
        'chinese_stake_pct': st.column_config.NumberColumn('Chinese %', format='%.1f'),
        'status': st.column_config.TextColumn('Status', width='medium'),
    }
)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown("**Analysis by Maurice McDonald**")
    st.caption("DFW Plotly Community Leader")

with foot2:
    st.markdown("**Data Sources**")
    st.caption("GEUS • USGS MRDS • Mining Filings")

with foot3:
    st.markdown("**[GitHub Repository](https://github.com/emcdo41/greenland-ree-dashboard)**")
    st.caption("MIT License")
