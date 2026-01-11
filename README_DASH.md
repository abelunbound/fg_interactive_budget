# Budget Line Item Analyzer - Multi-Page Dash App

## Project Structure

```
budget_analyzer/
├── app.py                  # Main application file with navigation
├── pages/                  # Pages folder
│   ├── home.py            # Home page (Budget analyzer)
│   ├── analysis.py        # Analysis page (placeholder)
│   └── reports.py         # Reports page (placeholder)
├── requirements_dash.txt  # Dependencies
└── README_DASH.md         # This file
```

## Installation

1. Install required packages:
```bash
pip install -r requirements_dash.txt
```

Or install individually:
```bash
pip install dash==2.14.2
pip install dash-bootstrap-components==1.5.0
pip install pandas==2.1.3
```

## Running the App

Run the main application:
```bash
python app.py
```

The app will start on `http://127.0.0.1:8050/`

Open your browser and navigate to that URL.

## Features

### Multi-Page Navigation
✅ **Modern Navigation Menu** - Top navigation bar with links to different pages
✅ **Home Page** - Budget line item analyzer with full functionality
✅ **Analysis Page** - Placeholder for advanced analysis tools
✅ **Reports Page** - Placeholder for reports and exports

### Home Page Features
✅ **Dropdown** - Select line items from the dropdown menu (80% width)
✅ **Download Button** - Positioned beside dropdown (20% width)
✅ **Radio Buttons** - Toggle between MDA View and Mother Ministry View (top position)
✅ **Interactive Table** - Hover over rows to see highlight effects
✅ **Pagination** - Navigate through data with 10 items per page
✅ **Total Sum** - Automatically calculates and displays the total amount
✅ **Responsive Design** - Professional green and gold color scheme

### Modern Features
✅ **page_container** - Modern Dash multi-page routing
✅ **@callback** - Using modern callback decorator instead of @app.callback
✅ **dash.register_page()** - Automatic page registration

## Data Structure

The app uses a pandas DataFrame with the following columns:
- `line_item_code`: Line item code (e.g., '21010101')
- `line_item_name`: Name of the line item (e.g., 'SALARY')
- `amount`: Budget amount (numeric)
- `mda`: MDA code (e.g., '111001001')
- `mda_name`: Name of the MDA (e.g., 'Ministry of Finance')
- `mother_ministry`: Parent ministry name

## Adding New Pages

To add a new page:

1. Create a new file in the `pages/` folder (e.g., `pages/newpage.py`)
2. Add this structure:

```python
import dash
from dash import html

# Register the page
dash.register_page(__name__, path='/newpage', name='New Page')

# Define the layout
layout = html.Div([
    html.H1("New Page"),
    # Your page content here
])
```

3. The page will automatically appear in the navigation and be accessible at `/newpage`

## Customization

To use your own data, edit the `dummy_data` list in `pages/home.py`:

```python
# Load your data
df = pd.read_csv('your_data.csv')  # or however you load your data
```

Make sure your dataframe has the required columns listed above.

## Navigation

- **Home** (`/`) - Main budget analyzer interface
- **Analysis** (`/analysis`) - Advanced analysis tools (coming soon)
- **Reports** (`/reports`) - Reports and exports (coming soon)
