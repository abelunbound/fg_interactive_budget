# flake8: noqa
# pylint: skip-file

import pandas as pd

def is_valid_lineitem_code(cell_value: str):
    """Check if code qualifies as LINE ITEM."""
    if not cell_value or cell_value == 'NAN':
        return False
    if cell_value == 'CODE':  # Header
        return False
    if len(cell_value) > 8:   # Too long (likely MDA codes)
        return False
    if cell_value.isdigit() or any(c.isdigit() for c in cell_value):
        return True
    return False


def split_tables_by_type(
    input_excel: str,
    output_excel: str,
    sheet_name: str = 0
):
    """
    Split merged tables into two types:
    - ERGP tables (CODE starts with ERGP)
    - LINE ITEM tables (CODE is numeric)
    
    Output: One Excel file with two sheets.
    """
    
    print(f"Reading: {input_excel}")
    
    df = pd.read_excel(
        input_excel,
        sheet_name=sheet_name,
        header=None,
        dtype=str,
        engine="openpyxl"
    )
    
    print(f"Total rows: {len(df)}")
    
    # Lists to collect rows for each table type
    ergp_rows = []
    lineitem_rows = []
    
    # Track if we've added headers
    header_added_ergp = False
    header_added_lineitem = False
    
    for i in range(len(df)):
        code_value = str(df.iloc[i, 0]).strip().upper()
        
        # Check if this is a header row (contains "CODE" or "LINE ITEM" keywords)
        is_header = any(keyword in str(df.iloc[i]).upper() 
                       for keyword in ['CODE', 'LINE ITEM', 'PROJECT NAME'])
        
        if is_header:
            # Add header to both types if not already added
            if not header_added_ergp:
                ergp_rows.append(df.iloc[i].tolist())
                header_added_ergp = True
            if not header_added_lineitem:
                lineitem_rows.append(df.iloc[i].tolist())
                header_added_lineitem = True
            continue
        
        # Skip completely empty rows
        if not code_value or code_value == 'NAN':
            continue
        
        # Classify by CODE column
        if code_value.startswith('ERGP'):
            # ERGP project table
            ergp_rows.append(df.iloc[i].tolist())
        elif is_valid_lineitem_code(code_value):
            # LINE ITEM table (numeric codes)
            lineitem_rows.append(df.iloc[i].tolist())
    
    # Create DataFrames
    ergp_df = pd.DataFrame(ergp_rows)
    lineitem_df = pd.DataFrame(lineitem_rows)
    
    print(f"\nERGP tables: {len(ergp_df)} rows")
    print(f"LINE ITEM tables: {len(lineitem_df)} rows")
    
    # Save to Excel with two sheets
    print(f"\nSaving to: {output_excel}")
    
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        if len(ergp_df) > 0:
            ergp_df.to_excel(writer, sheet_name='ERGP_Tables', index=False, header=False)
        if len(lineitem_df) > 0:
            lineitem_df.to_excel(writer, sheet_name='LineItem_Tables', index=False, header=False)
    
    print("Done!")
    print(f"  - Sheet 'ERGP_Tables': {len(ergp_df)} rows")
    print(f"  - Sheet 'LineItem_Tables': {len(lineitem_df)} rows")


if __name__ == "__main__":
    # ===== CONFIG =====
    # input_excel = "data_approved/outputs/output_merged_with_mda.xlsx"  # Your merged file with MDA column
    input_excel = "data_approved/outputs/output_merged_with_mda.xlsx"  # Your merged file with MDA column
    output_excel = "data_approved/outputs/budget_split_into_capital_and_all_envelopes.xlsx"
    
    #1. to_500_output_merged_with_mda
    #2. 501_to_1000_output_merged_with_mda
    #3. 1001_to_2000_output_merged_with_mda
    #4. output_merged_with_mda
    
    split_tables_by_type(
        input_excel=input_excel,
        output_excel=output_excel
    )