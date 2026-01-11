# flake8: noqa
# pylint: skip-file

# import dash
# from dash import html, dcc, page_container
# import dash_bootstrap_components as dbc

# # Initialize the Dash app with Bootstrap theme
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

# # Custom CSS
# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <style>
#             :root {
#                 --primary: #1a472a;
#                 --primary-light: #2d5a3d;
#                 --accent: #d4af37;
#                 --bg: #faf8f3;
#                 --bg-elevated: #ffffff;
#                 --text: #2c2c2c;
#                 --text-muted: #6b6b6b;
#                 --border: #e0ddd5;
#             }
            
#             body {
#                 background-color: var(--bg);
#                 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
#                 margin: 0;
#                 padding: 0;
#             }
            
#             .navbar-custom {
#                 background: var(--primary);
#                 padding: 1rem 0;
#                 box-shadow: 0 2px 10px rgba(26, 71, 42, 0.15);
#             }
            
#             .navbar-brand {
#                 font-family: Georgia, 'Times New Roman', serif;
#                 font-size: 1.5rem;
#                 color: white !important;
#                 font-weight: bold;
#             }
            
#             .nav-link {
#                 color: rgba(255, 255, 255, 0.85) !important;
#                 font-weight: 500;
#                 padding: 0.5rem 1rem !important;
#                 transition: all 0.2s;
#             }
            
#             .nav-link:hover {
#                 color: var(--accent) !important;
#                 transform: translateY(-2px);
#             }
            
#             .nav-link.active {
#                 color: var(--accent) !important;
#                 font-weight: 600;
#             }
            
#             .header {
#                 border-bottom: 2px solid var(--accent);
#                 padding-bottom: 1.5rem;
#                 margin-bottom: 3rem;
#             }
            
#             .header h1 {
#                 font-family: 'DM Serif Display', Georgia, serif !important;
#                 font-size: 2.5rem;
#                 color: var(--primary);
#                 margin-bottom: 0.5rem;
#             }
            
#             .subtitle {
#                 color: var(--text-muted);
#                 font-size: 0.95rem;
#                 font-weight: 300;
#             }
            
#             .controls-section {
#                 background: var(--bg-elevated);
#                 padding: 2rem;
#                 border-radius: 12px;
#                 box-shadow: 0 4px 20px rgba(26, 71, 42, 0.08);
#                 margin-bottom: 2rem;
#             }
            
#             .results-section {
#                 background: var(--bg-elevated);
#                 padding: 2rem;
#                 border-radius: 12px;
#                 box-shadow: 0 4px 20px rgba(26, 71, 42, 0.08);
#             }
            
#             .results-header {
#                 display: flex;
#                 justify-content: space-between;
#                 align-items: center;
#                 margin-bottom: 1.5rem;
#                 padding-bottom: 1rem;
#                 border-bottom: 2px solid var(--accent);
#             }
            
#             .results-title {
#                 font-family: Georgia, 'Times New Roman', serif;
#                 font-size: 1.5rem;
#                 color: var(--primary);
#                 margin: 0;
#             }
            
#             .total-badge {
#                 background: var(--accent);
#                 color: var(--primary);
#                 padding: 0.5rem 1.5rem;
#                 border-radius: 50px;
#                 font-weight: 600;
#                 font-size: 1.1rem;
#             }
            
#             .Select-control {
#                 border: 2px solid var(--border) !important;
#                 border-radius: 8px !important;
#             }
            
#             .Select-control:hover {
#                 border-color: var(--primary) !important;
#             }
            
#             label {
#                 font-size: 0.875rem;
#                 font-weight: 600;
#                 color: var(--primary);
#                 text-transform: uppercase;
#                 letter-spacing: 0.5px;
#                 margin-bottom: 0.5rem;
#                 display: block;
#             }
            
#             .dash-table-container {
#                 overflow-x: auto;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {
#                 border-collapse: separate;
#                 border-spacing: 0;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
#                 background-color: var(--primary) !important;
#                 color: white !important;
#                 padding: 1rem !important;
#                 text-align: left !important;
#                 font-weight: 600 !important;
#                 text-transform: uppercase;
#                 font-size: 0.875rem;
#                 letter-spacing: 0.5px;
#                 border: none !important;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td {
#                 padding: 1rem !important;
#                 background-color: var(--bg) !important;
#                 border-bottom: 1px solid var(--border) !important;
#                 border-left: none !important;
#                 border-right: none !important;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:hover td {
#                 background-color: #f0ede4 !important;
#                 transition: all 0.2s;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-child th:first-child {
#                 border-top-left-radius: 8px;
#             }
            
#             .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-child th:last-child {
#                 border-top-right-radius: 8px;
#             }
            
#             .btn-primary {
#                 background-color: var(--primary) !important;
#                 border-color: var(--primary) !important;
#                 font-weight: 600;
#                 text-transform: uppercase;
#                 letter-spacing: 0.5px;
#                 padding: 0.75rem 2rem;
#             }
            
#             .btn-primary:hover {
#                 background-color: var(--primary-light) !important;
#                 border-color: var(--primary-light) !important;
#             }
            
#             .form-check-input:checked {
#                 background-color: var(--primary) !important;
#                 border-color: var(--primary) !important;
#             }
            
#             .radio-group {
#                 padding-bottom: 1.5rem;
#                 border-bottom: 1px solid var(--border);
#                 margin-bottom: 1.5rem;
#             }
            
#             input[type="text"].form-control {
#                 border: 2px solid var(--border);
#                 border-radius: 8px;
#             }
            
#             input[type="text"].form-control:focus {
#                 border-color: var(--primary);
#                 box-shadow: 0 0 0 0.2rem rgba(26, 71, 42, 0.1);
#             }
            
#             .pagination-info {
#                 color: var(--text-muted);
#                 font-size: 0.9rem;
#                 margin-top: 1rem;
#             }
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

# # Navigation bar
# navbar = dbc.Navbar(
#     dbc.Container([
#         dbc.Row([
#             dbc.Col([
#                 dbc.NavbarBrand("Budget Analyzer", className="navbar-brand")
#             ], width="auto"),
#             dbc.Col([
#                 dbc.Nav([
#                     dbc.NavLink("Home", href="/", active="exact", className="nav-link"),
#                     dbc.NavLink("Analysis", href="/analysis", active="exact", className="nav-link"),
#                     dbc.NavLink("Reports", href="/reports", active="exact", className="nav-link"),
#                 ], navbar=True)
#             ])
#         ], align="center", className="w-100")
#     ], fluid=True),
#     className="navbar-custom mb-4",
#     dark=True
# )

# # App layout
# app.layout = html.Div([
#     navbar,
#     dbc.Container([
#         page_container
#     ], fluid=True, style={'maxWidth': '1400px', 'padding': '2rem'})
# ])

# if __name__ == '__main__':
#     app.run(debug=True, port=8050)


import dash
from dash import html, dcc, page_container
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

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
                margin: 0;
                padding: 0;
            }
            
            .navbar-custom {
                background: var(--primary) !important; 
                padding: 0.5rem 0;
                box-shadow: 0 2px 10px rgba(26, 71, 42, 0.15);
            }
            
            .navbar-brand {
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 1.5rem;
                color: white !important;
                font-weight: bold;
            }
            
            .nav-link {
                color: rgba(255, 255, 255, 0.85) !important;
                font-weight: 500;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s;
            }
            
            .nav-link:hover {
                color: var(--accent) !important;
                transform: translateY(-2px);
            }
            
            .nav-link.active {
                color: var(--accent) !important;
                font-weight: 600;
            }
            
            .header {
                # border-bottom: 2px solid var(--accent);
                padding-bottom: 1rem;
                # margin-bottom: 3rem;
            }
            
            .header h1 {
                font-family: 'DM Serif Display', Georgia, serif;
                font-size: 2.5rem;
                color: var(--primary);
                margin-bottom: 0.5rem;
                font-weight: bold; 
            }
            
            .subtitle {
                border-bottom: 2px solid var(--accent);
                color: var(--text-muted);
                padding-bottom: 1rem;
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

# Navigation bar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            # dbc.Col([
            #     dbc.NavbarBrand("FG Interactive Budget", className="navbar-brand")
            # ], width="auto"),

            dbc.Col([
                dbc.Nav([
                    dbc.NavLink("Home", href="/", active="exact", className="nav-link"),
                    dbc.NavLink("Analysis", href="/analysis", active="exact", className="nav-link"),
                    dbc.NavLink("Reports", href="/reports", active="exact", className="nav-link"),
                ], navbar=True)

            ])
        ], align="center", className="w-100")
    ], 
    # style={'maxWidth': '1400px'}
    ),
    className="navbar-custom mb-4",
    dark=True
)

# App layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        page_container
    ], fluid=True, style={'maxWidth': '1400px', 'padding': '2rem'})
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)