# flake8: noqa
# pylint: skip-file

import dash
from dash import html, dcc, dash_table, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Register this page
dash.register_page(__name__, path='/', name='Home')

# Create dummy data
dummy_data = [
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1929869.076, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2500000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1800000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 3200000.00, 'mda': '111002002', 'mda_name': 'Health Insurance Agency', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1500000.00, 'mda': '111003001', 'mda_name': 'Ministry of Education', 'mother_ministry': 'Ministry of Education'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 397603.960, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 450000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 320000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 580000.00, 'mda': '111002002', 'mda_name': 'Health Insurance Agency', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 96493.464, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 125000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 95000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 192986.908, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 250000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 180000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 26169.534, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 35000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
    {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 22000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2100000.00, 'mda': '111004001', 'mda_name': 'Ministry of Works', 'mother_ministry': 'Ministry of Works'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1750000.00, 'mda': '111004002', 'mda_name': 'Roads Agency', 'mother_ministry': 'Ministry of Works'},
    {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2900000.00, 'mda': '111005001', 'mda_name': 'Ministry of Agriculture', 'mother_ministry': 'Ministry of Agriculture'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 380000.00, 'mda': '111004001', 'mda_name': 'Ministry of Works', 'mother_ministry': 'Ministry of Works'},
    {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 290000.00, 'mda': '111004002', 'mda_name': 'Roads Agency', 'mother_ministry': 'Ministry of Works'},
]

df = pd.DataFrame(dummy_data)

# Get unique line items for dropdown
line_items = df[['line_item_code', 'line_item_name']].drop_duplicates().sort_values('line_item_code')
dropdown_options = [{'label': f"{row['line_item_code']} - {row['line_item_name']}", 'value': row['line_item_code']} 
                   for _, row in line_items.iterrows()]

# Page layout
layout = html.Div([
    # Header
    html.Div([
        html.H1("Budget Line Item Analyzer", className="header"),
        html.P("Ministry & MDA Budget Analysis Tool", className="subtitle")
    ], className="header", style={'marginTop': '2rem'}),
    
    # Controls Section
    html.Div([
        # Radio buttons
        html.Div([
            dbc.RadioItems(
                id='view-type',
                options=[
                    {'label': ' MDA View', 'value': 'mda'},
                    {'label': ' Mother Ministry View', 'value': 'ministry'}
                ],
                value='mda',
                inline=True,
                className='mb-3'
            )
        ], className='radio-group', style={'display': 'none'}),
        
        # Dropdown and Download button row
        dbc.Row([
            dbc.Col([
                html.Label("Select Line Item"),
                dcc.Dropdown(
                    id='line-item-dropdown',
                    options=[{'label': '-- Select a line item --', 'value': ''}] + dropdown_options,
                    value='',
                    clearable=False,
                    style={'borderRadius': '8px'}
                )
            ], width=9),
            dbc.Col([
                html.Label('\u00A0'),  # Non-breaking space for alignment
                dbc.Button('Download', id='download-btn', color='primary', className='w-100')
            ], width=3, style={'display': 'flex', 'flexDirection': 'column'})
        ])
    ], className='controls-section'),
    
    # Results Section
    html.Div([
        # Results header
        html.Div([
            html.H2(id='results-title', children='Select a line item to view results', className='results-title'),
            html.Div(id='total-badge', children='Total: ₦0.00', className='total-badge')
        ], className='results-header'),
        
        # Table
        html.Div(id='table-container')
    ], className='results-section'),
    
    # Store for filtered data
    dcc.Store(id='filtered-data-store')
])

# Callback to filter data and update table
@callback(
    [Output('table-container', 'children'),
     Output('results-title', 'children'),
     Output('total-badge', 'children'),
     Output('filtered-data-store', 'data')],
    [Input('line-item-dropdown', 'value'),
     Input('view-type', 'value')]
)
def update_table(selected_line_item, view_type):
    if not selected_line_item:
        empty_msg = html.Div([
            html.Div('📊', style={'fontSize': '3rem', 'opacity': '0.5', 'marginBottom': '1rem'}),
            html.P('Select a line item from the dropdown above to view budget data')
        ], style={'textAlign': 'center', 'padding': '3rem', 'color': 'var(--text-muted)'})
        
        return empty_msg, 'Select a line item to view results', 'Total: ₦0.00', None
    
    # Filter data
    filtered_df = df[df['line_item_code'] == selected_line_item].copy()
    
    if filtered_df.empty:
        empty_msg = html.Div([
            html.Div('🔍', style={'fontSize': '3rem', 'opacity': '0.5', 'marginBottom': '1rem'}),
            html.P('No results found for the selected line item')
        ], style={'textAlign': 'center', 'padding': '3rem', 'color': 'var(--text-muted)'})
        
        return empty_msg, 'No results found', 'Total: ₦0.00', None
    
    # Format amount as currency
    filtered_df['amount_formatted'] = filtered_df['amount'].apply(
        lambda x: f"₦{x:,.2f}"
    )
    
    # Calculate total
    total = filtered_df['amount'].sum()
    total_formatted = f"Total: ₦{total:,.2f}"
    
    # Get line item name
    line_item_name = filtered_df['line_item_name'].iloc[0]
    view_label = 'MDAs' if view_type == 'mda' else 'Mother Ministries'
    results_title = f"{line_item_name} ({selected_line_item}) - {len(filtered_df)} {view_label}"
    
    # Create table
    table = dash_table.DataTable(
        id='results-table',
        columns=[
            {'name': 'Line Item Code', 'id': 'line_item_code'},
            {'name': 'Line Item Name', 'id': 'line_item_name'},
            {'name': 'MDA Code', 'id': 'mda'},
            {'name': 'MDA Name', 'id': 'mda_name'},
            {'name': 'Amount (₦)', 'id': 'amount_formatted'}
        ],
        data=filtered_df.to_dict('records'),
        page_size=10,
        page_action='native',
        style_cell={
            'textAlign': 'left',
            'padding': '1rem',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif'
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
    
    return html.Div([table, pagination_info]), results_title, total_formatted, filtered_df.to_dict('records')

# Callback for download button (placeholder)
@callback(
    Output('download-btn', 'n_clicks'),
    Input('download-btn', 'n_clicks'),
    prevent_initial_call=True
)
def download_button_click(n_clicks):
    if n_clicks:
        # Placeholder for future download functionality
        print("Download button clicked - functionality coming soon!")
    return None
