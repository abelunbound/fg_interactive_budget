# flake8: noqa
# pylint: skip-file

import dash
from dash import html, dcc, dash_table, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Register this page
dash.register_page(__name__, path='/misplaced_priorities', name='Misplaced Priorities')

# # Create dummy data
# dummy_data = [
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1929869.076, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2500000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1800000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 3200000.00, 'mda': '111002002', 'mda_name': 'Health Insurance Agency', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1500000.00, 'mda': '111003001', 'mda_name': 'Ministry of Education', 'mother_ministry': 'Ministry of Education'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 397603.960, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 450000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 320000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 580000.00, 'mda': '111002002', 'mda_name': 'Health Insurance Agency', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 96493.464, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 125000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020201', 'line_item_name': 'NHIS', 'amount': 95000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 192986.908, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 250000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020202', 'line_item_name': "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION", 'amount': 180000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 26169.534, 'mda': '111001001', 'mda_name': 'Ministry of Finance', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 35000.00, 'mda': '111001002', 'mda_name': 'Budget Office', 'mother_ministry': 'Ministry of Finance'},
#     {'line_item_code': '21020212', 'line_item_name': "EMPLOYEES' COMPENSATION SCHEME (ECS)", 'amount': 22000.00, 'mda': '111002001', 'mda_name': 'Ministry of Health', 'mother_ministry': 'Ministry of Health'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2100000.00, 'mda': '111004001', 'mda_name': 'Ministry of Works', 'mother_ministry': 'Ministry of Works'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 1750000.00, 'mda': '111004002', 'mda_name': 'Roads Agency', 'mother_ministry': 'Ministry of Works'},
#     {'line_item_code': '21010101', 'line_item_name': 'SALARY', 'amount': 2900000.00, 'mda': '111005001', 'mda_name': 'Ministry of Agriculture', 'mother_ministry': 'Ministry of Agriculture'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 380000.00, 'mda': '111004001', 'mda_name': 'Ministry of Works', 'mother_ministry': 'Ministry of Works'},
#     {'line_item_code': '21020111', 'line_item_name': 'REGULAR ALLOWANCES', 'amount': 290000.00, 'mda': '111004002', 'mda_name': 'Roads Agency', 'mother_ministry': 'Ministry of Works'},
# ]

# df = pd.DataFrame(dummy_data)


misplaced_priorities_data_input_path = "data/outputs/mandate_deviation/llm_alignment_results_1_to_200_combined.csv"
use_columns = [
    'code',
    'ergp_line_item',
    'mda_code',
    'agency',
    'amount',
    'alignment',
    'reason',
]
df = pd.read_csv(misplaced_priorities_data_input_path, usecols=use_columns)


# Get unique agencies for dropdown
agencies = df[['agency', 'mda_code']].drop_duplicates().sort_values('agency')
dropdown_options = [{'label': row['agency'], 'value': row['mda_code']} for _, row in agencies.iterrows()]

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
                id='view-type-mp',
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
                html.Label("Search or Select FG Agency or Department"),
                dcc.Dropdown(
                    id='mda-dropdown',
                    options=[{'label': '-- Select FG Agency --', 'value': 'ALL'}] + dropdown_options,
                    value='',
                    clearable=False,
                    style={'borderRadius': '8px'}
                )
            ], width=9),
            dbc.Col([
                html.Label('\u00A0'),  # Non-breaking space for alignment
                dbc.Button('Download', id='download-btn-mp', color='primary', className='w-100')
            ], width=3, style={'display': 'flex', 'flexDirection': 'column'})
        ])
    ], className='controls-section'),
    
    # Results Section
    html.Div([
        # Results header
        html.Div([
            html.H2(id='results-title-mp', children='Select an FG Agency to view results', className='results-title'),
            html.Div(id='total-badge-mp', children='Total: ₦0.00', className='total-badge')
        ], className='results-header'),
        
        # Table
        html.Div(id='table-container-mp')
    ], className='results-section'),
    
    # Store for filtered data
    dcc.Store(id='filtered-data-store-mp')
])

# Callback to filter data and update table
@callback(
    [Output('table-container-mp', 'children'),
     Output('results-title-mp', 'children'),
     Output('total-badge-mp', 'children'),
     Output('filtered-data-store-mp', 'data')],
    [Input('mda-dropdown', 'value'),
     Input('view-type-mp', 'value')]
)
def update_table(selected_agency, view_type):
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
    
    # Calculate total
    total = filtered_df['amount'].sum()
    total_formatted = f"Total: ₦{total:,.2f}"

    # A: Sum amount where alignment is NO
    flagged = filtered_df[filtered_df["alignment"] == "NO"]
    flagged_amount = flagged['amount'].sum()
    flagged_amount = flagged_amount/1000000000
    flagged_amount_naira = f"₦{flagged_amount:.2f}bn"
    # B: Sum amount for full filtered dataframe
    total_mda_project_value = total/1000000000
    total_mda_project_value_naira = f"₦{total_mda_project_value:.2f}bn"
    # C: A/B
    flagged_percentage = flagged_amount/total_mda_project_value
    flagged_percentage1 = flagged_amount/total_mda_project_value

    # Format the output as a percentage with 2 decimal places
    format_flagged_as_percent = f"{flagged_percentage:.2%}"
    
    # Count occurrences of misplaced priorities, check as a percentage of total
    
    # view_label = 'MDAs' if view_type == 'mda' else 'Mother Ministries'
    # results_title = f"{len(filtered_df)} {view_label}"

    if selected_agency == 'ALL':
        results_title = f"""The total value of 2026 budget padded with projects outside agencies' mandates 
        amounts to {flagged_amount_naira} or {format_flagged_as_percent} of the cumulative 
        {total_mda_project_value_naira} capital budget of all FG agencies' assessed"""
    else:
        results_title = f"""{format_flagged_as_percent} of this agencies capital budget 
        or {flagged_amount_naira} of its {total_mda_project_value_naira} is outside its mandate"""

    


   
    # Create table
    table = dash_table.DataTable(
        id='results-table',
        columns=[
            {'name': 'ERGPCode', 'id': 'code'},
            {'name': 'Capital Project', 'id': 'ergp_line_item'},
            {'name': 'Amount (₦)', 'id': 'amount_formatted'},
            {'name': 'Within Mandate?', 'id': 'alignment'},
            {'name': 'Assessment', 'id': 'reason'},
            
        ],
        data=filtered_df.to_dict('records'),
        page_size=10,
        page_action='native',
        filter_action ='native',
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
    
    return html.Div([table, pagination_info]), results_title, total_formatted, filtered_df.to_dict('records')

# Callback for download button (placeholder)
@callback(
    Output('download-btn-mp', 'n_clicks'),
    Input('download-btn-mp', 'n_clicks'),
    prevent_initial_call=True
)
def download_button_click(n_clicks):
    if n_clicks:
        # Placeholder for future download functionality
        print("Download button clicked - functionality coming soon!")
    return None
