"""
Greenland Rare Earth Intelligence Dashboard
============================================
Strategic mineral intelligence for the Arctic's most contested resource frontier.

Author: Maurice McDonald | DFW Plotly Community Leader
Data Sources: GEUS, USGS MRDS, Mining Company Filings
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
# COLOR PALETTE
# ============================================================================

COLORS = {
    'periwinkle': '#8E9FD5',
    'periwinkle_light': '#B8C4E8',
    'periwinkle_dark': '#6B7FC2',
    'charcoal': '#2D3436',
    'charcoal_light': '#636E72',
    'grey_200': '#E9ECEF',
    'grey_300': '#DEE2E6',
    'danger': '#DC3545',
    'success': '#28A745',
}

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
    df['ownership_type'] = df['chinese_stake_pct'].apply(lambda x: 'Chinese Exposure' if x > 0 else 'Western Control')
    
    return df

# Load data
df = load_data()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("### 🌍 Greenland Rare Earth Intelligence")
st.caption("Strategic mineral assessment for the Arctic's most contested resource frontier | Data: GEUS • USGS • SEC")

st.divider()

# ============================================================================
# KPI STRIP
# ============================================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="🗺️ Total Deposits",
        value=str(len(df)),
    )

with kpi2:
    st.metric(
        label="⛏️ Total Resource",
        value=f"{df['resource_mt'].sum()/1000:.1f}B Mt",
    )

with kpi3:
    western_pct = len(df[df['chinese_stake_pct']==0])/len(df)*100
    st.metric(
        label="🇺🇸 Western Control",
        value=f"{western_pct:.0f}%",
    )

with kpi4:
    blocked = len(df[df['uranium_ppm'] > 100])
    st.metric(
        label="⚠️ Uranium Blocked",
        value=str(blocked),
    )

st.markdown("")

# ============================================================================
# MAP AND SCORES
# ============================================================================

map_col, score_col = st.columns([3, 2])

with map_col:
    st.markdown("**📍 Deposit Locations**")
    st.caption("Size = Resource | Color = Strategic Score")
    
    fig_map = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        size='resource_mt',
        color='strategic_score',
        hover_name='deposit_name',
        hover_data=['resource_mt', 'strategic_score', 'owner', 'status'],
        color_continuous_scale='Blues',
        size_max=40,
        zoom=2.5,
        center={'lat': 68, 'lon': -42},
        mapbox_style='carto-positron',
        height=450
    )
    
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig_map, use_container_width=True)

with score_col:
    st.markdown("**📊 Strategic Score Ranking**")
    st.caption("Top deposits by strategic value")
    
    df_sorted = df.sort_values('strategic_score', ascending=True).tail(10)
    
    fig_scores = go.Figure()
    
    fig_scores.add_trace(go.Bar(
        y=df_sorted['deposit_name'],
        x=df_sorted['strategic_score'],
        orientation='h',
        marker_color=COLORS['periwinkle'],
        text=df_sorted['strategic_score'].round(0).astype(int),
        textposition='outside',
    ))
    
    fig_scores.update_layout(
        xaxis_title='Strategic Score',
        xaxis_range=[0, 100],
        yaxis_title='',
        margin={"r":50,"t":10,"l":10,"b":40},
        height=400,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_scores, use_container_width=True)

# ============================================================================
# SECONDARY CHARTS
# ============================================================================

chart1, chart2, chart3 = st.columns([2, 1, 1])

with chart1:
    st.markdown("**💎 Resource vs Grade**")
    st.caption("Bubble size = Heavy REE %")
    
    fig_scatter = px.scatter(
        df,
        x='resource_mt',
        y='treo_grade_pct',
        size='heavy_ree_pct',
        color='ownership_type',
        hover_name='deposit_name',
        color_discrete_map={
            'Western Control': COLORS['periwinkle'],
            'Chinese Exposure': COLORS['danger']
        },
        log_x=True,
        height=300
    )
    
    fig_scatter.update_layout(
        xaxis_title='Resource (Mt, log scale)',
        yaxis_title='Grade (% TREO)',
        margin={"r":10,"t":10,"l":10,"b":40},
        plot_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart2:
    st.markdown("**🏛️ Ownership**")
    st.caption("By resource volume")
    
    western = df[df['chinese_stake_pct'] == 0]['resource_mt'].sum()
    chinese_exposed = df[df['chinese_stake_pct'] > 0]['resource_mt'].sum()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Western', 'Chinese Exp.'],
        values=[western, chinese_exposed],
        hole=0.6,
        marker_colors=[COLORS['periwinkle'], COLORS['danger']],
        textinfo='percent',
    )])
    
    fig_pie.update_layout(
        margin={"r":10,"t":10,"l":10,"b":10},
        height=280,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with chart3:
    st.markdown("**☢️ Uranium Status**")
    st.caption("2021 ban impact")
    
    clear = len(df[df['uranium_ppm'] <= 100])
    blocked = len(df[df['uranium_ppm'] > 100])
    
    fig_uranium = go.Figure(data=[go.Bar(
        x=['Clear', 'Blocked'],
        y=[clear, blocked],
        marker_color=[COLORS['success'], COLORS['danger']],
        text=[clear, blocked],
        textposition='outside',
    )])
    
    fig_uranium.update_layout(
        margin={"r":10,"t":10,"l":10,"b":40},
        height=280,
        yaxis_title='Deposits',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_uranium, use_container_width=True)

# ============================================================================
# KEY FINDING
# ============================================================================

st.info("""
**🎯 KEY FINDING:** **Tanbreez** (80/100) is the most strategically valuable deposit for Western interests. 
With 30% heavy REE content (highest globally), zero Chinese exposure, and US corporate control, 
it represents the best opportunity for supply chain diversification.
""")

# ============================================================================
# DATA TABLE
# ============================================================================

st.markdown("**📋 Deposit Details**")

st.dataframe(
    df[['deposit_name', 'strategic_score', 'resource_mt', 'treo_grade_pct', 
        'heavy_ree_pct', 'owner', 'chinese_stake_pct', 'status']].sort_values(
        'strategic_score', ascending=False
    ).reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.caption("Analysis by **Maurice McDonald** | DFW Plotly Community Leader | [GitHub](https://github.com/emcdo411/greenland-ree-dashboard)")
