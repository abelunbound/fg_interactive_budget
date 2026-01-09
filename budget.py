import dash
from dash import dcc, html, dash_table, Input, Output, callback
import pandas as pd

# Sample data - matching your provided data
data = {
    'code': [
        "0111001001", "0111001001", "0111001001", "0111001001", "0111001001",
        "0111001001", "0111001001", "0111001001", "0111001001", "0111001001",
        "0111001001", "0111001001", "0111001001", "0111001001", "0111001001",
        "0111001001", "0111002001", "0111003001", "0111004001", "0111005001",
        "0111006001", "0111007001", "0111008001", "0111009001", "0111010001"
    ],
    'line_item': [
        "EXPENDITURE", "PERSONNEL COST", "SALARY", "SALARIES AND WAGES",
        "SALARY", "ALLOWANCES AND SOCIAL CONTRIBUTION", "ALLOWANCES",
        "REGULAR ALLOWANCES", "SOCIAL CONTRIBUTIONS", "NHIS",
        "CONTRIBUTORY PENSION - EMPLOYER'S CONTRIBUTION",
        "EMPLOYEES' COMPENSATION SCHEME (ECS)", "OTHER RECURRENT COSTS",
        "OVERHEAD COST", "TRAVEL& TRANSPORT - GENERAL",
        "LOCAL TRAVEL & TRANSPORT: TRAINING", "SALARY", "SALARY", "SALARY",
        "ALLOWANCES", "ALLOWANCES", "NHIS", "NHIS", "OVERHEAD COST", "OVERHEAD COST"
    ],
    'amount': [
        43191309690, 2643122932, 1929869076, 1929869076, 1929869076,
        713253856, 397603960, 397603960, 315649896, 96493454,
        192986908, 26169534, 10060608332, 10060608332, 3433795667,
        275735543, 1500000000, 2100000000, 1800000000, 450000000,
        380000000, 85000000, 92000000, 8500000000, 9200000000
    ]
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Budget Line Item Analyzer"

# Get unique line items for dropdown
line_items = sorted(df['line_item'].unique().tolist())

# Format currency
def format_currency(amount):
    return f"₦ {amount:,.2f}"

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Budget Line Item Analyzer", 
                style={
                    'fontFamily': '"Courier New", monospace',
                    'fontSize': '2.5rem',
                    'fontWeight': '700',
                    'color': '#0d6b4f',
                    'marginBottom': '0.5rem',
                    'marginTop': '0'
                }),
        html.P("Explore and analyze government budget allocations across ministries, departments, and agencies",
               style={
                   'fontSize': '1rem',
                   'color': '#666',
                   'marginBottom': '2rem'
               })
    ], style={'padding': '2rem 3rem 1rem 3rem'}),
    
    # Controls section
    html.Div([
        # Radio buttons
        dcc.RadioItems(
            id='view-type',
            options=[
                {'label': ' MDA (Ministries, Departments & Agencies)', 'value': 'mda'},
                {'label': ' Mother Ministry', 'value': 'mother'}
            ],
            value='mda',
            inline=True,
            style={
                'marginBottom': '1.5rem',
                'paddingBottom': '1.5rem',
                'borderBottom': '1px solid #ddd',
                'display': 'flex',
                'gap': '2rem'
            },
            labelStyle={
                'display': 'flex',
                'alignItems': 'center',
                'marginRight': '2rem',
                'fontSize': '0.95rem',
                'cursor': 'pointer'
            }
        ),
        
        # Search controls row
        html.Div([
            # Dropdown
            html.Div([
                dcc.Dropdown(
                    id='line-item-dropdown',
                    options=[{'label': 'Select a line item...', 'value': ''}] + 
                            [{'label': item, 'value': item} for item in line_items],
                    value='',
                    placeholder='Select a line item...',
                    style={
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '0.95rem'
                    }
                )
            ], style={
                'flex': '0 0 350px',
                'marginRight': '1rem'
            }),
            
            # Search input and button
            html.Div([
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder='Search MDAs (coming soon)...',
                    disabled=True,
                    style={
                        'width': '100%',
                        'padding': '0.65rem 1rem',
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'fontSize': '0.95rem',
                        'backgroundColor': '#fafafa',
                        'marginRight': '0.5rem'
                    }
                ),
            ], style={
                'flex': '1',
                'marginRight': '0.5rem'
            }),
            
            html.Button(
                'Search',
                id='search-button',
                disabled=True,
                style={
                    'padding': '0.65rem 2rem',
                    'backgroundColor': '#0d6b4f',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'fontSize': '0.95rem',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'whiteSpace': 'nowrap',
                    'opacity': '0.5'
                }
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'gap': '0.5rem'
        })
    ], style={
        'backgroundColor': 'white',
        'padding': '2rem',
        'borderRadius': '8px',
        'margin': '0 3rem 2rem 3rem',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
    }),
    
    # Results section
    html.Div([
        # Results header
        html.Div([
            html.Div(id='results-title', children='Select a line item to view results',
                    style={
                        'fontFamily': '"Courier New", monospace',
                        'fontSize': '1.25rem',
                        'fontWeight': '600',
                        'color': '#0d6b4f'
                    }),
            html.Div(id='total-amount', children='₦ 0.00',
                    style={
                        'backgroundColor': '#fff8e1',
                        'border': '2px solid #ffc107',
                        'borderRadius': '8px',
                        'padding': '0.5rem 1.5rem',
                        'fontFamily': '"Courier New", monospace',
                        'fontSize': '1.25rem',
                        'fontWeight': '700',
                        'color': '#f57c00'
                    })
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '1.5rem 2rem',
            'backgroundColor': '#f8f8f8',
            'borderBottom': '1px solid #ddd'
        }),
        
        # Table container
        html.Div(id='table-container', children=[
            html.Div([
                html.Div([
                    html.Div("🔍", style={
                        'fontSize': '4rem',
                        'color': '#ccc',
                        'marginBottom': '1rem'
                    }),
                    html.P("No data to display. Please select a line item from the dropdown above.",
                          style={'color': '#999', 'fontSize': '0.95rem'})
                ], style={
                    'textAlign': 'center',
                    'padding': '4rem 2rem'
                })
            ])
        ])
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '8px',
        'margin': '0 3rem 2rem 3rem',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
        'overflow': 'hidden'
    })
], style={
    'backgroundColor': '#f5f5f5',
    'minHeight': '100vh',
    'fontFamily': 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
})

# Callback to update results
@callback(
    [Output('results-title', 'children'),
     Output('total-amount', 'children'),
     Output('table-container', 'children')],
    Input('line-item-dropdown', 'value')
)
def update_results(selected_line_item):
    # If no line item selected, show empty state
    if not selected_line_item or selected_line_item == '':
        empty_state = html.Div([
            html.Div("🔍", style={
                'fontSize': '4rem',
                'color': '#ccc',
                'marginBottom': '1rem'
            }),
            html.P("No data to display. Please select a line item from the dropdown above.",
                  style={'color': '#999', 'fontSize': '0.95rem'})
        ], style={
            'textAlign': 'center',
            'padding': '4rem 2rem'
        })
        
        return (
            'Select a line item to view results',
            '₦ 0.00',
            empty_state
        )
    
    # Filter data
    filtered_df = df[df['line_item'] == selected_line_item].copy()
    total_amount = filtered_df['amount'].sum()
    
    # Create table with built-in pagination
    table = dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[
            {'name': 'CODE', 'id': 'code'},
            {'name': 'LINE ITEM', 'id': 'line_item'},
            {'name': 'AMOUNT (₦)', 'id': 'amount', 'type': 'numeric',
             'format': {'specifier': ',.2f', 'locale': {'symbol': ['₦ ', '']}}}
        ],
        # Built-in pagination
        page_action='native',
        page_current=0,
        page_size=10,
        
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#0d6b4f',
            'color': 'white',
            'fontWeight': '700',
            'textTransform': 'uppercase',
            'fontSize': '0.75rem',
            'letterSpacing': '0.05em',
            'padding': '1rem',
            'fontFamily': 'Arial, sans-serif'
        },
        style_data={
            'fontFamily': '"Courier New", monospace',
            'fontSize': '0.9rem',
            'padding': '1rem'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '1rem'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'amount'},
                'textAlign': 'right',
                'fontWeight': '600'
            },
            {
                'if': {'column_id': 'code'},
                'color': '#0066cc',
                'fontWeight': '500'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#fafafa'
            }
        ],
        # Pagination styling
        style_as_list_view=True,
        css=[{
            'selector': '.previous-next-container',
            'rule': 'display: flex; justify-content: center; padding: 1rem; background-color: #f8f8f8;'
        }]
    )
    
    return (
        f'Results for: {selected_line_item}',
        format_currency(total_amount),
        table
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)