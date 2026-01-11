# flake8: noqa
# pylint: skip-file


import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# Configuration
input_path = "data/outputs/budget_split_into_capital_and_all_envelopes.xlsx"
sheet_name = "LineItem_Tables"

def ingest_excel(input_path, sheet_name):
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    
    # Convert CODE to string and filter by length
    df['CODE'] = df['CODE'].astype(str)
    df = df[df['CODE'].str.len() == 8].reset_index(drop=True)
    
    # Rename column 4 (5th column, 0-indexed) to 'mda'
    df = df.rename(columns={df.columns[4]: "mda"})
    
    # Drop column 3 (4th column, 0-indexed)
    df = df.drop(df.columns[3], axis=1)
    
    # Rename columns
    df = df.rename(columns={
        "CODE": "line_item_code",
        "LINE ITEM": "line_item_name",
        "AMOUNT": "amount"
    })
    
    # Convert amount to numeric (handles commas, spaces, etc.)
    df['amount'] = df['amount'].astype(str).str.replace(',', '', regex=False)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Drop rows with NaN amounts
    df = df.dropna(subset=['amount']).reset_index(drop=True)
    
    return df

# Load data
df = ingest_excel(input_path, sheet_name)

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary: #1a472a;
                --primary-light: #2d5a3d;
                --accent: #d4af37;
                --bg: #faf8f3;
                --bg-elevated: #ffffff;
                --text: #2c2c2c;
                --text-muted: #6b6b6b;
                --border: #e0ddd5;
            }
            
            body {
                background-color: var(--bg);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            }
            
            .header {
                border-bottom: 2px solid var(--accent);
                padding-bottom: 1.5rem;
                margin-bottom: 3rem;
            }
            
            .header h1 {
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 2.5rem;
                color: var(--primary);
                margin-bottom: 0.5rem;
            }
            
            .subtitle {
                color: var(--text-muted);
                font-size: 0.95rem;
                font-weight: 300;
            }
            
            .controls-section {
                background: var(--bg-elevated);
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(26, 71, 42, 0.08);
                margin-bottom: 2rem;
            }
            
            .results-section {
                background: var(--bg-elevated);
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(26, 71, 42, 0.08);
            }
            
            .results-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid var(--accent);
            }
            
            .results-title {
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 1.5rem;
                color: var(--primary);
                margin: 0;
            }
            
            .total-badge {
                background: var(--accent);
                color: var(--primary);
                padding: 0.5rem 1.5rem;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1.1rem;
            }
            
            .Select-control {
                border: 2px solid var(--border) !important;
                border-radius: 8px !important;
            }
            
            .Select-control:hover {
                border-color: var(--primary) !important;
            }
            
            label {
                font-size: 0.875rem;
                font-weight: 600;
                color: var(--primary);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 0.5rem;
                display: block;
            }
            
            .dash-table-container {
                overflow-x: auto;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {
                border-collapse: separate;
                border-spacing: 0;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
                background-color: var(--primary) !important;
                color: white !important;
                padding: 1rem !important;
                text-align: left !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                font-size: 0.875rem;
                letter-spacing: 0.5px;
                border: none !important;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td {
                padding: 1rem !important;
                background-color: var(--bg) !important;
                border-bottom: 1px solid var(--border) !important;
                border-left: none !important;
                border-right: none !important;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:hover td {
                background-color: #f0ede4 !important;
                transition: all 0.2s;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-child th:first-child {
                border-top-left-radius: 8px;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-child th:last-child {
                border-top-right-radius: 8px;
            }
            
            .btn-primary {
                background-color: var(--primary) !important;
                border-color: var(--primary) !important;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 0.75rem 2rem;
            }
            
            .btn-primary:hover {
                background-color: var(--primary-light) !important;
                border-color: var(--primary-light) !important;
            }
            
            .form-check-input:checked {
                background-color: var(--primary) !important;
                border-color: var(--primary) !important;
            }
            
            .radio-group {
                padding-bottom: 1.5rem;
                border-bottom: 1px solid var(--border);
                margin-bottom: 1.5rem;
            }
            
            input[type="text"].form-control {
                border: 2px solid var(--border);
                border-radius: 8px;
            }
            
            input[type="text"].form-control:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 0.2rem rgba(26, 71, 42, 0.1);
            }
            
            .pagination-info {
                color: var(--text-muted);
                font-size: 0.9rem;
                margin-top: 1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Get unique line items for dropdown
line_items = df[['line_item_code', 'line_item_name']].drop_duplicates().sort_values('line_item_code')
dropdown_options = [{'label': f"{row['line_item_code']} - {row['line_item_name']}", 'value': row['line_item_code']} 
                   for _, row in line_items.iterrows()]

# App layout
app.layout = dbc.Container([
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
        ], className='radio-group'),
        
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
    
], fluid=True, style={'maxWidth': '1400px', 'padding': '2rem'})

# Callback to filter data and update table
@app.callback(
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
@app.callback(
    Output('download-btn', 'n_clicks'),
    Input('download-btn', 'n_clicks'),
    prevent_initial_call=True
)
def download_button_click(n_clicks):
    if n_clicks:
        # Placeholder for future download functionality
        print("Download button clicked - functionality coming soon!")
    return None

if __name__ == '__main__':
    app.run(debug=True, port=8050)