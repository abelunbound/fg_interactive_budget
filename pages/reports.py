# flake8: noqa
# pylint: skip-file

import dash
from dash import html
import dash_bootstrap_components as dbc

# Register this page
dash.register_page(__name__, path='/reports', name='Reports')

# Page layout
layout = html.Div([
    html.Div([
        html.H1("Reports", className="header"),
        html.P("Budget Reports and Exports", className="subtitle")
    ], className="header", style={'marginTop': '2rem'}),
    
    html.Div([
        html.Div([
            html.Div('📄', style={'fontSize': '4rem', 'marginBottom': '1rem'}),
            html.H3('Reports Page', style={'color': '#1a472a', 'marginBottom': '1rem'}),
            html.P('This page will contain budget reports and export functionality.', 
                   style={'color': '#6b6b6b', 'fontSize': '1.1rem'}),
            html.P('Coming soon...', style={'color': '#6b6b6b', 'fontStyle': 'italic'})
        ], style={
            'textAlign': 'center',
            'padding': '4rem 2rem',
            'background': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 4px 20px rgba(26, 71, 42, 0.08)'
        })
    ])
])
