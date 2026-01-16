"""
Greenland Rare Earth Intelligence Dashboard
============================================
Strategic mineral intelligence for the Arctic's most contested resource frontier.

Author: Maurice McDonald | DFW Plotly Community Leader
Data Sources: GEUS, USGS MRDS, Mining Company Filings
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ============================================================================
# CONFIGURATION
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

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load and prepare the REE deposits dataset"""
    
    # Try to load from CSV, fall back to embedded data
    try:
        df = pd.read_csv('greenland_ree_deposits.csv')
    except FileNotFoundError:
        # Embedded data for standalone operation
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
# DASH APP INITIALIZATION
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
    title='Greenland REE Intelligence'
)

server = app.server  # For deployment

# ============================================================================
# COMPONENT BUILDERS
# ============================================================================

def create_kpi_card(title, value, subtitle, icon="📊", accent=False):
    """Create a KPI card component"""
    return dbc.Card([
        dbc.CardBody([
            html.Div(icon, style={'fontSize': '24px', 'marginBottom': '8px'}),
            html.P(title, className='text-muted mb-1', style={'fontSize': '12px', 'textTransform': 'uppercase'}),
            html.H3(value, style={
                'color': COLORS['periwinkle'] if accent else COLORS['charcoal'],
                'fontWeight': 'bold',
                'marginBottom': '4px'
            }),
            html.P(subtitle, className='text-muted mb-0', style={'fontSize': '11px'})
        ])
    ], style={
        'borderLeft': f"4px solid {COLORS['periwinkle'] if accent else COLORS['grey_300']}",
        'height': '100%'
    })


def create_map_figure(df):
    """Create the main map visualization"""
    
    fig = px.scatter_mapbox(
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
        zoom=3,
        center={'lat': 68, 'lon': -42},
        mapbox_style='carto-positron'
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title='Strategic<br>Score',
            tickfont=dict(size=10),
            titlefont=dict(size=11)
        ),
        paper_bgcolor='white'
    )
    
    return fig


def create_score_comparison(df):
    """Create horizontal bar chart of strategic scores"""
    
    df_sorted = df.sort_values('strategic_score', ascending=True).tail(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_sorted['deposit_name'],
        x=df_sorted['strategic_score'],
        orientation='h',
        marker=dict(
            color=df_sorted['strategic_score'],
            colorscale=[
                [0, COLORS['grey_300']],
                [0.5, COLORS['periwinkle_light']],
                [1, COLORS['periwinkle']]
            ],
            line=dict(width=0)
        ),
        text=df_sorted['strategic_score'].round(0).astype(int),
        textposition='outside',
        textfont=dict(size=11, color=COLORS['charcoal']),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis=dict(
            title='Strategic Score',
            range=[0, 100],
            gridcolor=COLORS['grey_200'],
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=10)
        ),
        margin=dict(l=10, r=40, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=350
    )
    
    return fig


def create_resource_vs_grade(df):
    """Create scatter plot of resource size vs grade"""
    
    fig = px.scatter(
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
        }
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(gridcolor=COLORS['grey_200']),
        yaxis=dict(gridcolor=COLORS['grey_200']),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        height=300
    )
    
    return fig


def create_ownership_pie(df):
    """Create ownership breakdown pie chart"""
    
    western = df[df['chinese_stake_pct'] == 0]['resource_mt'].sum()
    chinese_exposed = df[df['chinese_stake_pct'] > 0]['resource_mt'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Western Control', 'Chinese Exposure'],
        values=[western, chinese_exposed],
        hole=0.6,
        marker=dict(colors=[COLORS['periwinkle'], COLORS['danger']]),
        textinfo='percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} Mt<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=10)
        ),
        height=250,
        annotations=[dict(
            text=f'{western/(western+chinese_exposed)*100:.0f}%<br>Western',
            x=0.5, y=0.5,
            font=dict(size=14, color=COLORS['charcoal']),
            showarrow=False
        )]
    )
    
    return fig


def create_uranium_status_chart(df):
    """Create uranium status breakdown"""
    
    clear = len(df[df['uranium_ppm'] <= 100])
    blocked = len(df[df['uranium_ppm'] > 100])
    
    fig = go.Figure(data=[go.Bar(
        x=['Clear (<100 ppm)', 'Blocked (>100 ppm)'],
        y=[clear, blocked],
        marker=dict(color=[COLORS['success'], COLORS['danger']]),
        text=[clear, blocked],
        textposition='outside',
        textfont=dict(size=14, color=COLORS['charcoal'])
    )])
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(title='', tickfont=dict(size=10)),
        yaxis=dict(title='Number of Deposits', gridcolor=COLORS['grey_200'], tickfont=dict(size=10)),
        height=250
    )
    
    return fig


# ============================================================================
# APP LAYOUT
# ============================================================================

app.layout = dbc.Container([
    
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Span('● ', style={'color': COLORS['periwinkle'], 'fontSize': '14px'}),
                html.Span('OPEN SOURCE INTELLIGENCE', style={
                    'fontSize': '11px',
                    'letterSpacing': '2px',
                    'color': COLORS['periwinkle_dark'],
                    'fontWeight': 'bold'
                })
            ], style={'marginBottom': '8px'}),
            html.H1('Greenland Rare Earth Intelligence', style={
                'color': COLORS['charcoal'],
                'fontWeight': 'bold',
                'marginBottom': '4px',
                'fontSize': '28px'
            }),
            html.P('Strategic mineral assessment for the Arctic\'s most contested resource frontier', 
                   style={'color': COLORS['charcoal_light'], 'marginBottom': '0'})
        ], width=8),
        dbc.Col([
            html.Div([
                html.P('Data Sources', style={'fontSize': '10px', 'color': COLORS['charcoal_light'], 'marginBottom': '4px'}),
                html.Span('GEUS', className='badge', style={'backgroundColor': COLORS['periwinkle'], 'marginRight': '4px'}),
                html.Span('USGS', className='badge', style={'backgroundColor': COLORS['periwinkle_dark'], 'marginRight': '4px'}),
                html.Span('SEC', className='badge', style={'backgroundColor': COLORS['charcoal_light']}),
            ], style={'textAlign': 'right'})
        ], width=4)
    ], className='mb-4 mt-3'),
    
    # KPI Strip
    dbc.Row([
        dbc.Col(create_kpi_card(
            'Total Deposits', 
            str(len(df)), 
            'Documented REE occurrences',
            '🗺️',
            accent=True
        ), width=3),
        dbc.Col(create_kpi_card(
            'Total Resource', 
            f'{df["resource_mt"].sum()/1000:.1f}B Mt', 
            'Combined resource estimate',
            '⛏️'
        ), width=3),
        dbc.Col(create_kpi_card(
            'Western Control', 
            f'{len(df[df["chinese_stake_pct"]==0])/len(df)*100:.0f}%', 
            f'{len(df[df["chinese_stake_pct"]==0])} of {len(df)} deposits',
            '🇺🇸',
            accent=True
        ), width=3),
        dbc.Col(create_kpi_card(
            'Uranium Blocked', 
            str(len(df[df['uranium_ppm'] > 100])), 
            'Deposits >100 ppm U',
            '⚠️'
        ), width=3),
    ], className='mb-4'),
    
    # Main Content Row
    dbc.Row([
        # Map Column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Deposit Locations', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('Size = Resource | Color = Strategic Score', className='text-muted')
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='main-map',
                        figure=create_map_figure(df),
                        style={'height': '450px'},
                        config={'displayModeBar': False}
                    )
                ], style={'padding': '0'})
            ])
        ], width=7),
        
        # Score Column
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Strategic Score Ranking', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('Top 10 deposits by strategic value', className='text-muted')
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='score-chart',
                        figure=create_score_comparison(df),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=5),
    ], className='mb-4'),
    
    # Secondary Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Resource vs Grade', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('Bubble size = Heavy REE %', className='text-muted')
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='scatter-chart',
                        figure=create_resource_vs_grade(df),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Ownership Breakdown', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('By total resource volume', className='text-muted')
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='ownership-pie',
                        figure=create_ownership_pie(df),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Uranium Status', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('2021 ban impact', className='text-muted')
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='uranium-chart',
                        figure=create_uranium_status_chart(df),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=3),
    ], className='mb-4'),
    
    # Key Finding Banner
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Span('KEY FINDING', style={
                            'fontSize': '10px',
                            'fontWeight': 'bold',
                            'color': COLORS['periwinkle_dark'],
                            'letterSpacing': '1px'
                        }),
                    ], style={'marginBottom': '8px'}),
                    html.P([
                        html.Strong('Tanbreez'), 
                        ' (80/100) is the most strategically valuable deposit for Western interests. ',
                        'With 30% heavy REE content (highest globally), zero Chinese exposure, ',
                        'and US corporate control, it represents the best opportunity for supply chain diversification.'
                    ], style={'marginBottom': '0', 'fontSize': '14px'})
                ])
            ], style={'borderLeft': f'4px solid {COLORS["periwinkle"]}', 'backgroundColor': COLORS['periwinkle_pale']})
        ])
    ], className='mb-4'),
    
    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Deposit Details', className='mb-0', style={'fontWeight': 'bold'}),
                    html.Small('Click column headers to sort', className='text-muted')
                ]),
                dbc.CardBody([
                    dbc.Table.from_dataframe(
                        df[['deposit_name', 'strategic_score', 'resource_mt', 'treo_grade_pct', 
                            'heavy_ree_pct', 'owner', 'chinese_stake_pct', 'status']].sort_values(
                            'strategic_score', ascending=False
                        ).round(2),
                        striped=True,
                        bordered=True,
                        hover=True,
                        size='sm',
                        style={'fontSize': '11px'}
                    )
                ])
            ])
        ])
    ], className='mb-4'),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.Div([
                html.Span('Analysis by ', style={'color': COLORS['charcoal_light']}),
                html.Strong('Maurice McDonald'),
                html.Span(' | DFW Plotly Community Leader | ', style={'color': COLORS['charcoal_light']}),
                html.A('GitHub', href='https://github.com/emcdo41/greenland-ree-dashboard', target='_blank'),
                html.Span(' | ', style={'color': COLORS['charcoal_light']}),
                html.Span('Data: GEUS, USGS, Mining Filings', style={'color': COLORS['charcoal_light'], 'fontSize': '11px'})
            ], style={'textAlign': 'center', 'paddingBottom': '20px'})
        ])
    ])
    
], fluid=True, style={'maxWidth': '1400px', 'backgroundColor': COLORS['white']})

# ============================================================================
# CALLBACKS (for future interactivity)
# ============================================================================

# Example callback - update charts based on map click
@callback(
    Output('score-chart', 'figure'),
    Input('main-map', 'clickData'),
    prevent_initial_call=True
)
def highlight_selected(click_data):
    """Highlight selected deposit in bar chart"""
    fig = create_score_comparison(df)
    
    if click_data:
        selected = click_data['points'][0]['hovertext']
        # Add highlight logic here if needed
    
    return fig

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌍 GREENLAND RARE EARTH INTELLIGENCE DASHBOARD")
    print("="*60)
    print(f"\n📊 Loaded {len(df)} deposits")
    print(f"💎 Total resource: {df['resource_mt'].sum()/1000:.1f}B Mt")
    print(f"🇺🇸 Western control: {len(df[df['chinese_stake_pct']==0])}/{len(df)} deposits")
    print(f"\n🚀 Starting server at http://127.0.0.1:8050")
    print("   Press Ctrl+C to quit\n")
    
    app.run_server(debug=True, port=8050)
