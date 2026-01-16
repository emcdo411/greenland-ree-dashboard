"""
Greenland Rare Earth Intelligence Dashboard
============================================
Advanced strategic mineral intelligence platform.

Author: Maurice McDonald | DFW Plotly Community Leader
Data Sources: GEUS, USGS MRDS, Mining Company Filings
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Greenland REE Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# COLOR PALETTE - FRED Style / Maurice McDonald Signature
# ============================================================================

COLORS = {
    'periwinkle': '#8E9FD5',
    'periwinkle_light': '#B8C4E8',
    'periwinkle_dark': '#6B7FC2',
    'periwinkle_pale': '#E8ECF5',
    'charcoal': '#2D3436',
    'charcoal_light': '#636E72',
    'white': '#FFFFFF',
    'grey_50': '#FAFBFC',
    'grey_100': '#F8F9FA',
    'grey_200': '#E9ECEF',
    'grey_300': '#DEE2E6',
    'danger': '#DC3545',
    'danger_light': '#F8D7DA',
    'success': '#28A745',
    'success_light': '#D4EDDA',
    'warning': '#FFC107',
    'warning_light': '#FFF3CD',
    'info': '#17A2B8',
}

# Custom CSS for professional styling - FIXED SIDEBAR
st.markdown(f"""
<style>
    /* ===== SIDEBAR STYLING - MATCH MAIN APP ===== */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['white']} !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {COLORS['white']} !important;
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['white']} !important;
        border-right: 1px solid {COLORS['grey_200']};
    }}
    
    section[data-testid="stSidebar"] > div {{
        background-color: {COLORS['white']} !important;
    }}
    
    /* Sidebar content area */
    .css-1d391kg, .css-1lcbmhc, .css-12oz5g7 {{
        background-color: {COLORS['white']} !important;
    }}
    
    /* ===== MAIN AREA ===== */
    .stApp {{
        background-color: {COLORS['grey_50']};
    }}
    
    .main .block-container {{
        background-color: {COLORS['grey_50']};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {COLORS['charcoal']};
    }}
    
    /* Metric cards */
    [data-testid="stMetricValue"] {{
        font-size: 28px;
        color: {COLORS['periwinkle_dark']};
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {COLORS['grey_100']};
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: {COLORS['charcoal']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['periwinkle']} !important;
        color: white !important;
    }}
    
    /* Slider styling */
    .stSlider > div > div {{
        background-color: {COLORS['periwinkle_light']};
    }}
    
    .stSlider > div > div > div {{
        background-color: {COLORS['periwinkle']};
    }}
    
    /* Multiselect */
    .stMultiSelect > div {{
        background-color: {COLORS['white']};
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        background-color: transparent;
    }}
    
    /* Info boxes */
    .highlight-box {{
        background: linear-gradient(135deg, {COLORS['periwinkle_pale']} 0%, {COLORS['white']} 100%);
        border-left: 4px solid {COLORS['periwinkle']};
        padding: 20px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }}
    
    /* Download button */
    .stDownloadButton > button {{
        background-color: {COLORS['periwinkle']};
        color: white;
        border: none;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {COLORS['periwinkle_dark']};
        color: white;
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        background-color: {COLORS['white']};
    }}
    
    /* Dataframe */
    .stDataFrame {{
        background-color: {COLORS['white']};
    }}
    
    /* Divider */
    hr {{
        border-color: {COLORS['grey_200']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load and prepare the comprehensive REE deposits dataset"""
    
    data = {
        'deposit_name': ['Tanbreez (Kringlerne)', 'Kvanefjeld', 'Sarfartoq', 'Motzfeldt', 
                       'Ilímaussaq Complex', 'Tikiusaaq', 'Qeqertaasaq', 'Milne Land',
                       'Niaqornaarsuk', 'Qaqarssuk', 'Kangerlussuaq', 'Gardar South',
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
                 'Tanbreez Mining', 'NunaMinerals', 'Government', 
                 'Multiple', 'ETM', 'Historical', 'Platina Resources'],
        'chinese_stake_pct': [0, 9.21, 0, 0, 5, 0, 0, 0, 0, 0, 0, 3, 9.21, 0, 0],
        'status': ['Advancing', 'Blocked', 'Permitted', 'Exploration', 'Multiple', 
                  'Prospect', 'Prospect', 'Exploration', 'Exploration', 'Abandoned',
                  'Reserved', 'Multiple', 'Uncertain', 'Closed', 'PGE Focus'],
        'uranium_ppm': [15, 285, 45, 60, 120, 30, 25, 40, 55, 20, 35, 150, 220, 15, 10],
        'strategic_score': [80.0, 52.0, 61.0, 48.0, 58.0, 42.0, 35.0, 40.0, 55.0, 38.0, 45.0, 62.0, 48.0, 25.0, 32.0],
        # Five-lens scores
        'geological_score': [85, 90, 70, 55, 75, 60, 50, 45, 65, 55, 50, 70, 60, 30, 40],
        'regulatory_score': [90, 20, 75, 60, 50, 70, 70, 65, 70, 50, 40, 45, 30, 80, 75],
        'ownership_score': [95, 50, 85, 80, 60, 90, 90, 85, 85, 80, 70, 65, 50, 85, 80],
        'infrastructure_score': [60, 65, 40, 55, 60, 30, 20, 25, 50, 35, 45, 70, 55, 60, 35],
        'geopolitical_score': [70, 55, 50, 40, 55, 35, 30, 40, 45, 30, 50, 60, 50, 20, 25],
        # Additional metadata
        'discovery_year': [2007, 1956, 1995, 1962, 1806, 2010, 2015, 2008, 2005, 1990, 2000, 1960, 1960, 1806, 1930],
        'ice_free_months': [4, 4, 3, 4, 4, 3, 2, 2, 4, 3, 3, 4, 4, 4, 2],
        'port_distance_km': [15, 12, 180, 25, 15, 200, 350, 400, 20, 150, 120, 18, 15, 30, 280],
    }
    
    df = pd.DataFrame(data)
    
    # Derived columns
    df['ownership_type'] = df['chinese_stake_pct'].apply(
        lambda x: 'Chinese Exposure' if x > 0 else 'Western Control'
    )
    df['uranium_status'] = df['uranium_ppm'].apply(
        lambda x: 'Blocked (>100 ppm)' if x > 100 else 'Clear (<100 ppm)'
    )
    df['score_category'] = pd.cut(
        df['strategic_score'], 
        bins=[0, 40, 60, 80, 100], 
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    df['contained_treo_kt'] = (df['resource_mt'] * df['treo_grade_pct'] / 100 * 1000).round(0)
    df['contained_hree_kt'] = (df['contained_treo_kt'] * df['heavy_ree_pct'] / 100).round(0)
    
    return df

# Load data
df = load_data()

# ============================================================================
# SIDEBAR - FILTERS & CONTROLS
# ============================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="font-size: 40px;">🌍</div>
        <div style="font-size: 14px; font-weight: bold; color: {COLORS['charcoal']};">REE Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size: 13px; font-weight: bold; color: {COLORS["charcoal"]}; margin-bottom: 5px;">📊 STRATEGIC SCORE</p>', unsafe_allow_html=True)
    score_range = st.slider(
        "Filter by score range",
        min_value=0,
        max_value=100,
        value=(0, 100),
        key="score_filter",
        label_visibility="collapsed"
    )
    
    st.markdown("")
    
    st.markdown(f'<p style="font-size: 13px; font-weight: bold; color: {COLORS["charcoal"]}; margin-bottom: 5px;">🏛️ OWNERSHIP</p>', unsafe_allow_html=True)
    ownership_filter = st.multiselect(
        "Filter by ownership",
        options=['Western Control', 'Chinese Exposure'],
        default=['Western Control', 'Chinese Exposure'],
        label_visibility="collapsed"
    )
    
    st.markdown("")
    
    st.markdown(f'<p style="font-size: 13px; font-weight: bold; color: {COLORS["charcoal"]}; margin-bottom: 5px;">☢️ URANIUM STATUS</p>', unsafe_allow_html=True)
    uranium_filter = st.multiselect(
        "Uranium ban impact",
        options=['Clear (<100 ppm)', 'Blocked (>100 ppm)'],
        default=['Clear (<100 ppm)', 'Blocked (>100 ppm)'],
        label_visibility="collapsed"
    )
    
    st.markdown("")
    
    st.markdown(f'<p style="font-size: 13px; font-weight: bold; color: {COLORS["charcoal"]}; margin-bottom: 5px;">⚙️ PROJECT STATUS</p>', unsafe_allow_html=True)
    status_options = df['status'].unique().tolist()
    status_filter = st.multiselect(
        "Project status",
        options=status_options,
        default=status_options,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Export
    st.markdown(f'<p style="font-size: 13px; font-weight: bold; color: {COLORS["charcoal"]}; margin-bottom: 10px;">📥 EXPORT DATA</p>', unsafe_allow_html=True)
    
    @st.cache_data
    def convert_df_to_csv(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')
    
    csv_data = convert_df_to_csv(df)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=f"greenland_ree_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 10px 0;">
        <p style="font-size: 10px; color: {COLORS['charcoal_light']}; margin: 0;">Data Sources</p>
        <p style="font-size: 11px; color: {COLORS['charcoal']}; margin: 5px 0 0 0;"><strong>GEUS • USGS • SEC</strong></p>
        <p style="font-size: 10px; color: {COLORS['charcoal_light']}; margin: 10px 0 0 0;">Updated: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
    """, unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df['strategic_score'] >= score_range[0]) &
    (df['strategic_score'] <= score_range[1]) &
    (df['ownership_type'].isin(ownership_filter)) &
    (df['uranium_status'].isin(uranium_filter)) &
    (df['status'].isin(status_filter))
]

# ============================================================================
# HEADER
# ============================================================================

col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 5px;">
        <span style="background-color: {COLORS['periwinkle']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 10px; font-weight: bold; letter-spacing: 1px;">OPEN SOURCE INTELLIGENCE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("# 🌍 Greenland Rare Earth Intelligence")
    st.caption("Strategic mineral assessment for the Arctic's most contested resource frontier")

with col_header2:
    st.markdown("")
    st.markdown("")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Deposits", f"{len(filtered_df)}/{len(df)}")
    with col_stat2:
        western_pct = len(filtered_df[filtered_df['chinese_stake_pct']==0])/max(len(filtered_df),1)*100
        st.metric("Western", f"{western_pct:.0f}%")

st.markdown("---")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "🔬 Deposit Analysis", 
    "🎯 Scenario Modeling",
    "📋 Data Explorer"
])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab1:
    # KPI Strip
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        st.metric(
            label="📍 Deposits",
            value=len(filtered_df),
            delta=f"of {len(df)} total"
        )
    
    with kpi2:
        total_resource = filtered_df['resource_mt'].sum()
        st.metric(
            label="⛏️ Total Resource",
            value=f"{total_resource/1000:.1f}B Mt",
        )
    
    with kpi3:
        total_treo = filtered_df['contained_treo_kt'].sum()
        st.metric(
            label="💎 Contained TREO",
            value=f"{total_treo/1000:.1f}M t",
        )
    
    with kpi4:
        avg_heavy = filtered_df['heavy_ree_pct'].mean()
        st.metric(
            label="🔋 Avg Heavy REE",
            value=f"{avg_heavy:.1f}%",
        )
    
    with kpi5:
        blocked_pct = len(filtered_df[filtered_df['uranium_ppm'] > 100]) / max(len(filtered_df),1) * 100
        st.metric(
            label="☢️ Uranium Blocked",
            value=f"{blocked_pct:.0f}%",
        )
    
    st.markdown("")
    
    # Main charts row
    map_col, chart_col = st.columns([3, 2])
    
    with map_col:
        st.markdown("#### 🗺️ Strategic Deposit Map")
        st.caption("Size = Resource | Color = Strategic Score | Click for details")
        
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat='latitude',
            lon='longitude',
            size='resource_mt',
            color='strategic_score',
            hover_name='deposit_name',
            hover_data={
                'latitude': False,
                'longitude': False,
                'resource_mt': ':.0f',
                'strategic_score': ':.0f',
                'heavy_ree_pct': ':.0f',
                'owner': True,
                'status': True,
            },
            color_continuous_scale=[
                [0, COLORS['grey_300']],
                [0.4, COLORS['periwinkle_light']],
                [0.7, COLORS['periwinkle']],
                [1, COLORS['periwinkle_dark']]
            ],
            size_max=50,
            zoom=2.3,
            center={'lat': 68, 'lon': -42},
            mapbox_style='carto-positron',
            height=500
        )
        
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_colorbar_title_text="Score"
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with chart_col:
        st.markdown("#### 📊 Strategic Ranking")
        st.caption("Deposits ordered by strategic value score")
        
        df_sorted = filtered_df.sort_values('strategic_score', ascending=True)
        
        # Color bars by score category
        colors = []
        for score in df_sorted['strategic_score']:
            if score >= 70:
                colors.append(COLORS['success'])
            elif score >= 50:
                colors.append(COLORS['periwinkle'])
            else:
                colors.append(COLORS['grey_300'])
        
        fig_ranking = go.Figure()
        
        fig_ranking.add_trace(go.Bar(
            y=df_sorted['deposit_name'],
            x=df_sorted['strategic_score'],
            orientation='h',
            marker_color=colors,
            text=[f"{s:.0f}" for s in df_sorted['strategic_score']],
            textposition='outside',
            textfont=dict(size=11),
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<br>Owner: %{customdata}<extra></extra>",
            customdata=df_sorted['owner']
        ))
        
        # Add threshold lines
        fig_ranking.add_vline(x=50, line_dash="dash", line_color=COLORS['warning'], line_width=1)
        fig_ranking.add_vline(x=70, line_dash="dash", line_color=COLORS['success'], line_width=1)
        
        fig_ranking.update_layout(
            xaxis_title='Strategic Score',
            xaxis_range=[0, 100],
            yaxis_title='',
            margin={"r":60,"t":10,"l":10,"b":40},
            height=500,
            plot_bgcolor='white',
            xaxis=dict(gridcolor=COLORS['grey_200']),
        )
        
        st.plotly_chart(fig_ranking, use_container_width=True)
    
    # Secondary charts
    st.markdown("---")
    
    sec1, sec2, sec3 = st.columns([2, 1, 1])
    
    with sec1:
        st.markdown("#### 💎 Resource Quality Matrix")
        st.caption("Positioning by size and grade | Bubble = Heavy REE content")
        
        fig_matrix = px.scatter(
            filtered_df,
            x='resource_mt',
            y='treo_grade_pct',
            size='heavy_ree_pct',
            color='ownership_type',
            hover_name='deposit_name',
            hover_data=['strategic_score', 'owner', 'status'],
            color_discrete_map={
                'Western Control': COLORS['periwinkle'],
                'Chinese Exposure': COLORS['danger']
            },
            log_x=True,
            size_max=45,
            height=350
        )
        
        # Add quadrant labels
        fig_matrix.add_annotation(x=3.5, y=1.8, text="HIGH VALUE", showarrow=False, 
                                  font=dict(size=10, color=COLORS['charcoal_light']))
        fig_matrix.add_annotation(x=1.2, y=0.4, text="LOW VALUE", showarrow=False,
                                  font=dict(size=10, color=COLORS['charcoal_light']))
        
        fig_matrix.update_layout(
            xaxis_title='Resource (Mt, log scale)',
            yaxis_title='Grade (% TREO)',
            margin={"r":10,"t":10,"l":10,"b":40},
            plot_bgcolor='white',
            xaxis=dict(gridcolor=COLORS['grey_200']),
            yaxis=dict(gridcolor=COLORS['grey_200']),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    with sec2:
        st.markdown("#### 🏛️ Ownership Split")
        st.caption("By total resource volume")
        
        western = filtered_df[filtered_df['chinese_stake_pct'] == 0]['resource_mt'].sum()
        chinese = filtered_df[filtered_df['chinese_stake_pct'] > 0]['resource_mt'].sum()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Western Control', 'Chinese Exposure'],
            values=[western, chinese],
            hole=0.65,
            marker_colors=[COLORS['periwinkle'], COLORS['danger']],
            textinfo='percent',
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} Mt<br>%{percent}<extra></extra>"
        )])
        
        fig_pie.add_annotation(
            text=f"{western/(western+chinese+0.001)*100:.0f}%<br><span style='font-size:10px'>Western</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=COLORS['charcoal'])
        )
        
        fig_pie.update_layout(
            margin={"r":10,"t":10,"l":10,"b":10},
            height=350,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with sec3:
        st.markdown("#### ☢️ Regulatory Risk")
        st.caption("2021 uranium ban impact")
        
        status_counts = filtered_df['uranium_status'].value_counts()
        
        fig_uranium = go.Figure(data=[go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker_color=[COLORS['success'] if 'Clear' in x else COLORS['danger'] for x in status_counts.index],
            text=status_counts.values,
            textposition='outside',
            textfont=dict(size=14),
        )])
        
        fig_uranium.update_layout(
            margin={"r":10,"t":10,"l":10,"b":40},
            height=350,
            yaxis_title='Deposits',
            xaxis_title='',
            plot_bgcolor='white',
            yaxis=dict(gridcolor=COLORS['grey_200']),
        )
        
        st.plotly_chart(fig_uranium, use_container_width=True)
    
    # Key Finding
    st.markdown("")
    st.markdown(f"""
    <div class="highlight-box">
        <div style="font-size: 11px; font-weight: bold; color: {COLORS['periwinkle_dark']}; letter-spacing: 1px; margin-bottom: 8px;">KEY FINDING</div>
        <p style="margin: 0; font-size: 15px; line-height: 1.6;">
            <strong>Tanbreez</strong> (80/100) emerges as the most strategically valuable deposit for Western supply chain diversification. 
            With 30% heavy REE content (highest globally), zero Chinese exposure, US corporate control via Critical Metals Corp (NASDAQ: CRML), 
            and clear regulatory status, it represents the optimal balance of geological quality and geopolitical security.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: DEPOSIT ANALYSIS
# ============================================================================

with tab2:
    st.markdown("### 🔬 Deep Dive Analysis")
    st.caption("Select a deposit for comprehensive five-lens assessment")
    
    # Deposit selector
    col_select, col_compare = st.columns([1, 1])
    
    with col_select:
        selected_deposit = st.selectbox(
            "Select Primary Deposit",
            options=filtered_df['deposit_name'].tolist(),
            index=0
        )
    
    with col_compare:
        compare_deposit = st.selectbox(
            "Compare With (Optional)",
            options=['None'] + [d for d in filtered_df['deposit_name'].tolist() if d != selected_deposit],
            index=0
        )
    
    # Get selected deposit data
    deposit_data = filtered_df[filtered_df['deposit_name'] == selected_deposit].iloc[0]
    
    st.markdown("---")
    
    # Deposit header
    score = deposit_data['strategic_score']
    score_color = COLORS['success'] if score >= 70 else COLORS['periwinkle'] if score >= 50 else COLORS['danger']
    
    header1, header2, header3 = st.columns([2, 1, 1])
    
    with header1:
        st.markdown(f"## {selected_deposit}")
        st.caption(f"Owner: {deposit_data['owner']} | Status: {deposit_data['status']}")
    
    with header2:
        st.metric("Strategic Score", f"{score:.0f}/100")
    
    with header3:
        st.metric("Ownership Risk", "Low" if deposit_data['chinese_stake_pct'] == 0 else f"{deposit_data['chinese_stake_pct']:.1f}% Chinese")
    
    # Five-lens radar chart
    radar_col, details_col = st.columns([1, 1])
    
    with radar_col:
        st.markdown("#### 🎯 Five-Lens Assessment")
        
        categories = ['Geological', 'Regulatory', 'Ownership', 'Infrastructure', 'Geopolitical']
        
        fig_radar = go.Figure()
        
        # Primary deposit
        values_primary = [
            deposit_data['geological_score'],
            deposit_data['regulatory_score'],
            deposit_data['ownership_score'],
            deposit_data['infrastructure_score'],
            deposit_data['geopolitical_score']
        ]
        values_primary.append(values_primary[0])  # Close the polygon
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values_primary,
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=f"rgba(142, 159, 213, 0.3)",
            line_color=COLORS['periwinkle'],
            name=selected_deposit
        ))
        
        # Comparison deposit
        if compare_deposit != 'None':
            compare_data = filtered_df[filtered_df['deposit_name'] == compare_deposit].iloc[0]
            values_compare = [
                compare_data['geological_score'],
                compare_data['regulatory_score'],
                compare_data['ownership_score'],
                compare_data['infrastructure_score'],
                compare_data['geopolitical_score']
            ]
            values_compare.append(values_compare[0])
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values_compare,
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=f"rgba(220, 53, 69, 0.2)",
                line_color=COLORS['danger'],
                name=compare_deposit
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9)),
                angularaxis=dict(tickfont=dict(size=11))
            ),
            showlegend=True if compare_deposit != 'None' else False,
            margin={"r":30,"t":30,"l":30,"b":30},
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with details_col:
        st.markdown("#### 📋 Deposit Specifications")
        
        specs_df = pd.DataFrame({
            'Metric': [
                'Resource Estimate',
                'TREO Grade',
                'Heavy REE Content',
                'Contained TREO',
                'Contained Heavy REE',
                'Uranium Content',
                'Ice-Free Season',
                'Port Distance',
                'Discovery Year'
            ],
            'Value': [
                f"{deposit_data['resource_mt']:,.0f} Mt",
                f"{deposit_data['treo_grade_pct']:.2f}%",
                f"{deposit_data['heavy_ree_pct']:.0f}%",
                f"{deposit_data['contained_treo_kt']:,.0f} kt",
                f"{deposit_data['contained_hree_kt']:,.0f} kt",
                f"{deposit_data['uranium_ppm']:.0f} ppm {'⚠️' if deposit_data['uranium_ppm'] > 100 else '✅'}",
                f"{deposit_data['ice_free_months']} months",
                f"{deposit_data['port_distance_km']} km",
                str(deposit_data['discovery_year'])
            ]
        })
        
        st.dataframe(specs_df, use_container_width=True, hide_index=True, height=380)
    
    # Score breakdown
    st.markdown("---")
    st.markdown("#### 📊 Score Breakdown")
    
    score_cols = st.columns(5)
    
    lens_data = [
        ('🏔️ Geological', deposit_data['geological_score'], 'Resource quality, grade, mineralogy'),
        ('⚖️ Regulatory', deposit_data['regulatory_score'], 'Permits, uranium ban, compliance'),
        ('🏛️ Ownership', deposit_data['ownership_score'], 'Western control, Chinese exposure'),
        ('🚢 Infrastructure', deposit_data['infrastructure_score'], 'Port access, power, logistics'),
        ('🌐 Geopolitical', deposit_data['geopolitical_score'], 'Strategic alignment, policy support'),
    ]
    
    for i, (label, score, desc) in enumerate(lens_data):
        with score_cols[i]:
            color = COLORS['success'] if score >= 70 else COLORS['warning'] if score >= 50 else COLORS['danger']
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: {COLORS['grey_100']}; border-radius: 8px; border-top: 4px solid {color};">
                <div style="font-size: 24px; font-weight: bold; color: {color};">{score}</div>
                <div style="font-size: 13px; font-weight: bold; margin: 5px 0;">{label}</div>
                <div style="font-size: 10px; color: {COLORS['charcoal_light']};">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: SCENARIO MODELING
# ============================================================================

with tab3:
    st.markdown("### 🎯 Scenario Modeling")
    st.caption("Explore how policy changes and market conditions affect strategic assessments")
    
    scenario_col1, scenario_col2 = st.columns([1, 1])
    
    with scenario_col1:
        st.markdown("#### ⚙️ Scenario Parameters")
        
        # Uranium ban scenario
        uranium_scenario = st.radio(
            "☢️ Greenland Uranium Ban (2021)",
            options=['Current (Ban Active)', 'Ban Lifted', 'Stricter Limits (50 ppm)'],
            index=0
        )
        
        # Chinese investment scenario
        chinese_scenario = st.radio(
            "🇨🇳 Chinese Investment Policy",
            options=['Current Restrictions', 'Complete Ban', 'Restrictions Relaxed'],
            index=0
        )
        
        # Infrastructure investment
        infra_boost = st.slider(
            "🚢 Infrastructure Investment ($B)",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.5
        )
        
        # REE price scenario
        price_scenario = st.select_slider(
            "💰 REE Price Environment",
            options=['Collapse (-50%)', 'Decline (-25%)', 'Stable', 'Rally (+25%)', 'Spike (+100%)'],
            value='Stable'
        )
    
    with scenario_col2:
        st.markdown("#### 📈 Scenario Impact")
        
        # Calculate scenario adjustments
        scenario_df = filtered_df.copy()
        
        # Uranium ban impact
        if uranium_scenario == 'Ban Lifted':
            scenario_df.loc[scenario_df['uranium_ppm'] > 100, 'regulatory_score'] += 40
            scenario_df.loc[scenario_df['uranium_ppm'] > 100, 'strategic_score'] += 15
        elif uranium_scenario == 'Stricter Limits (50 ppm)':
            scenario_df.loc[scenario_df['uranium_ppm'] > 50, 'regulatory_score'] -= 30
            scenario_df.loc[scenario_df['uranium_ppm'] > 50, 'strategic_score'] -= 10
        
        # Chinese investment impact
        if chinese_scenario == 'Complete Ban':
            scenario_df.loc[scenario_df['chinese_stake_pct'] > 0, 'ownership_score'] -= 20
            scenario_df.loc[scenario_df['chinese_stake_pct'] > 0, 'strategic_score'] -= 8
        elif chinese_scenario == 'Restrictions Relaxed':
            scenario_df['geopolitical_score'] -= 10
        
        # Infrastructure boost
        if infra_boost > 0:
            infra_impact = min(infra_boost * 3, 20)
            scenario_df['infrastructure_score'] += infra_impact
            scenario_df['strategic_score'] += infra_impact * 0.15
        
        # Cap scores at 100
        for col in ['regulatory_score', 'ownership_score', 'infrastructure_score', 'geopolitical_score', 'strategic_score']:
            scenario_df[col] = scenario_df[col].clip(0, 100)
        
        # Show top movers
        scenario_df['score_change'] = scenario_df['strategic_score'] - filtered_df['strategic_score']
        
        movers = scenario_df[['deposit_name', 'strategic_score', 'score_change']].sort_values('score_change', ascending=False)
        
        st.markdown("**Top Score Changes:**")
        
        for _, row in movers.head(5).iterrows():
            change = row['score_change']
            arrow = "🔺" if change > 0 else "🔻" if change < 0 else "➡️"
            color = COLORS['success'] if change > 0 else COLORS['danger'] if change < 0 else COLORS['charcoal_light']
            st.markdown(f"{arrow} **{row['deposit_name']}**: {row['strategic_score']:.0f} ({change:+.1f})")
    
    st.markdown("---")
    
    # Scenario comparison chart
    st.markdown("#### 📊 Baseline vs Scenario Comparison")
    
    comparison_df = pd.DataFrame({
        'Deposit': filtered_df['deposit_name'],
        'Baseline': filtered_df['strategic_score'],
        'Scenario': scenario_df['strategic_score']
    }).sort_values('Baseline', ascending=True)
    
    fig_scenario = go.Figure()
    
    fig_scenario.add_trace(go.Bar(
        y=comparison_df['Deposit'],
        x=comparison_df['Baseline'],
        orientation='h',
        name='Baseline',
        marker_color=COLORS['grey_300'],
    ))
    
    fig_scenario.add_trace(go.Bar(
        y=comparison_df['Deposit'],
        x=comparison_df['Scenario'],
        orientation='h',
        name='Scenario',
        marker_color=COLORS['periwinkle'],
    ))
    
    fig_scenario.update_layout(
        barmode='group',
        xaxis_title='Strategic Score',
        xaxis_range=[0, 100],
        yaxis_title='',
        margin={"r":20,"t":10,"l":10,"b":40},
        height=450,
        plot_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_scenario, use_container_width=True)
    
    # Scenario summary
    baseline_leader = filtered_df.loc[filtered_df['strategic_score'].idxmax(), 'deposit_name']
    scenario_leader = scenario_df.loc[scenario_df['strategic_score'].idxmax(), 'deposit_name']
    
    if baseline_leader != scenario_leader:
        st.warning(f"⚠️ **Leadership Change:** Under this scenario, **{scenario_leader}** overtakes **{baseline_leader}** as the top-ranked deposit.")
    else:
        st.success(f"✅ **{baseline_leader}** remains the top-ranked deposit under this scenario.")

# ============================================================================
# TAB 4: DATA EXPLORER
# ============================================================================

with tab4:
    st.markdown("### 📋 Data Explorer")
    st.caption("Full dataset with sorting and filtering capabilities")
    
    # Column selector
    all_columns = filtered_df.columns.tolist()
    display_columns = st.multiselect(
        "Select columns to display",
        options=all_columns,
        default=['deposit_name', 'strategic_score', 'resource_mt', 'treo_grade_pct', 
                'heavy_ree_pct', 'owner', 'chinese_stake_pct', 'status', 'uranium_ppm']
    )
    
    if display_columns:
        # Sortable dataframe
        sort_col = st.selectbox("Sort by", options=display_columns, index=1)
        sort_order = st.radio("Order", options=['Descending', 'Ascending'], horizontal=True)
        
        display_df = filtered_df[display_columns].sort_values(
            sort_col, 
            ascending=(sort_order == 'Ascending')
        ).reset_index(drop=True)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        # Summary statistics
        st.markdown("---")
        st.markdown("#### 📈 Summary Statistics")
        
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        summary_cols = [c for c in numeric_cols if c in display_columns]
        
        if summary_cols:
            summary_df = filtered_df[summary_cols].describe().round(2)
            st.dataframe(summary_df, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown("**Analysis by Maurice McDonald**")
    st.caption("DFW Plotly Community Leader")

with foot2:
    st.markdown("**Methodology**")
    st.caption("Five-Lens Strategic Assessment Framework")

with foot3:
    st.markdown("**[GitHub Repository](https://github.com/emcdo411/greenland-ree-dashboard)**")
    st.caption("MIT License | Data: GEUS • USGS • SEC")
