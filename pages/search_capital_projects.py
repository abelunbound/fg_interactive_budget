# flake8: noqa
# pylint: skip-file

import dash
from dash import html, dcc, dash_table, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Register this page
dash.register_page(__name__, path='/search-capital-projects', name='Analysis')


ergp_capital_projects_df = "data/outputs/ergp_budget_with_mda_no_duplicates.csv"
df = pd.read_csv(ergp_capital_projects_df)

# Get unique agencies for dropdown
agencies = df[['agency', 'mda_code']].drop_duplicates().sort_values('agency')
dropdown_options = [{'label': row['agency'], 'value': row['mda_code']} for _, row in agencies.iterrows()]

# Page layout
layout = html.Div([
    # Header
    html.Div([
        # html.H1("Budget Line Item Analyzer", className="header"),
        html.P("""Search any item of interest - Ambulance, Street lights, 
               vehicles to see allocations across agencies""", 
               className="subtitle")
    ], className="header", style={'marginTop': '2rem'}),
    
    # Controls Section
    html.Div([
        # Radio buttons
        html.Div([
            dbc.RadioItems(
                id='view-type-search-capital',
                options=[
                    {'label': ' MDA View', 'value': 'mda'},
                    {'label': ' Mother Ministry View', 'value': 'ministry'}
                ],
                value='mda',
                inline=True,
                className='mb-3'
            )
        ], className='radio-group', style={'display': 'none'}), #Temporarily disabled from view
        
        # Dropdown and Download button row
        dbc.Row([
            dbc.Col([
                # html.Label("Search or Select FG Agency or Department"),
                dcc.Dropdown(
                    id='mda-dropdown-search-capital',
                    options=[{'label': '-- All FG Agencies --', 'value': 'ALL'}] + dropdown_options,
                    value='ALL',
                    clearable=False,
                    placeholder="Select an agency...",
                    style={'borderRadius': '8px'}
                )
            ], 
            md=5, xs=12),
            
            dbc.Col([
                # html.Label("Search or Select FG Agency or Department"),
                dbc.Input(
                    id='search-capital-input',
                    type='text',
                    placeholder='Enter search term (e.g., street light)...',
                    debounce=True
                )
            ], 
            md=7, xs=12),

            # dbc.Col([
            #     html.Label('\u00A0'),  # Non-breaking space for alignment
            #     dbc.Button('Download', id='download-btn-search-capital', color='primary')
            # ], 
            # md=1, xs=12, 
            # style={'display': 'flex', 'flexDirection': 'column'})
        ])
    ], className='controls-section'),
    
    # Results Section
    html.Div([
        # Results header
        html.Div([
            # html.H2(id='results-title-search-capital', children='Select an FG Agency to view results', className='results-title'),
            html.Div(id='total-badge-search-capital', children='Total: ₦0.00', className='total-badge')
        ], className='results-header'),
        
        # Table
        html.Div(id='table-container-search-capital')
    ], className='results-section'),
    
    # Store for filtered data
    dcc.Store(id='filtered-data-store-search-capital')
])

# Callback to filter data and update table
@callback(
    [Output('table-container-search-capital', 'children'),
    #  Output('results-title-search-capital', 'children'),
     Output('total-badge-search-capital', 'children'),
     Output('filtered-data-store-search-capital', 'data')
     ],
    [Input('mda-dropdown-search-capital', 'value'),
     Input('view-type-search-capital', 'value'),
     Input('search-capital-input', 'value')
     ]
)
def update_table(selected_agency, view_type, search_capital_project_term):
    if not selected_agency:
        empty_msg = html.Div([
            html.Div('📊', style={'fontSize': '3rem', 'opacity': '0.5', 'marginBottom': '1rem'}),
            html.P('Select an FG Agency from the dropdown above to view misplaced priorities')
        ], style={'textAlign': 'center', 'padding': '3rem', 'color': 'var(--text-muted)'})
        
        return empty_msg, 'Select an Agency to view results', 'Total: ₦0.00', None
    
    # Filter data
    if selected_agency == 'ALL':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['mda_code'] == selected_agency].copy()
    
    if filtered_df.empty:
        empty_msg = html.Div([
            html.Div('🔍', style={'fontSize': '3rem', 'opacity': '0.5', 'marginBottom': '1rem'}),
            html.P('No results found for the selected Agency')
        ], style={'textAlign': 'center', 'padding': '3rem', 'color': 'var(--text-muted)'})
        
        return empty_msg, 'No results found', 'Total: ₦0.00', None
    
    # Format amount as currency
    filtered_df['amount_formatted'] = filtered_df['amount'].apply(
        lambda x: f"₦{x:,.2f}"
    )

    # Search
    if search_capital_project_term:
        # Case-insensitive search across all columns
        mask = filtered_df['ergp_line_item'].astype(str).str.contains(
            search_capital_project_term, case=False, na=False
        )
        filtered_df = filtered_df[mask]
    
    # Calculate total
    total = filtered_df['amount'].sum()
    total_formatted = f"Total: ₦{total:,.2f}"

   
    # Create table
    table = dash_table.DataTable(
        id='results-table',
        columns=[
            {'name': 'ERGPCode', 'id': 'code'},
            {'name': 'Capital Project', 'id': 'ergp_line_item'},
            {'name': 'Status', 'id': 'status'},
            {'name': 'Agency', 'id': 'agency'},
            {'name': 'Amount (₦)', 'id': 'amount_formatted'},
            
            
        ],
        data=filtered_df.to_dict('records'),
        page_size=10,
        page_action='native',
        filter_action ='native',
        # sort_action="native",
        style_cell={
            'textAlign': 'left',
            'padding': '1rem',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif',
            'whiteSpace': 'normal',  # Allow text wrapping
            'height': 'auto',  # Auto height for wrapped text
        },
        style_header={
            'backgroundColor': '#1a472a',
            'color': 'white',
            'fontWeight': '600',
            'textTransform': 'uppercase',
            'fontSize': '0.875rem',
            'letterSpacing': '0.5px',
            'border': 'none'
        },
        style_data={
            'backgroundColor': '#faf8f3',
            'border': 'none',
            'borderBottom': '1px solid #e0ddd5'
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'amount_formatted'},
                'fontWeight': '600',
                'color': '#1a472a',
                'fontVariantNumeric': 'tabular-nums'
            }
        ],
        style_table={
            'borderRadius': '8px',
            'overflow': 'hidden'
        }
    )
    
    # Pagination info
    pagination_info = html.Div(
        f"Showing entries from filtered data",
        className='pagination-info'
    )


    
    
    return html.Div([table, pagination_info]), total_formatted, filtered_df.to_dict('records')

# # Callback for download button (placeholder)
# @callback(
#     Output('download-btn-search-capital', 'n_clicks'),
#     Input('download-btn-search-capital', 'n_clicks'),
#     prevent_initial_call=True
# )
# def download_button_click(n_clicks):
#     if n_clicks:
#         # Placeholder for future download functionality
#         print("Download button clicked - functionality coming soon!")
#     return None

