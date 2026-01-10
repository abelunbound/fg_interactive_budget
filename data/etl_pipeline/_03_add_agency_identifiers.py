# flake8: noqa
# pylint: skip-file

import pandas as pd


def add_mda_column(
    input_excel: str,
    output_excel: str,
    sheet_name: str = 0
):
    """
    If length of entry in column 0 is 10 characters,
    copy it to column 4 (5th column) and name that column 'mda'.
    """

    print(f"Reading: {input_excel}")

    df = pd.read_excel(
        input_excel,
        sheet_name=sheet_name,
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    print(f"Original shape: {df.shape}")

    # Ensure at least 5 columns exist
    if df.shape[1] < 5:
        for _ in range(5 - df.shape[1]):
            df[df.shape[1]] = ""

    # Set header for column 5
    df.iloc[0, 4] = "mda"

    moved_count = 0

    # Start from row 1 to avoid header row
    for i in range(1, len(df)):
        val = str(df.iloc[i, 0]).strip()

        if val and val.lower() != "nan" and len(val) == 10:
            df.iloc[i, 4] = val
            moved_count += 1

    print(f"Filled MDA column for {moved_count} rows")
    
    # ⭐ ADD THIS: Call propagate function BEFORE saving
    propagate_mda_down(df, mda_col=4, source_col=0)

    print(f"Saving: {output_excel}")

    df.to_excel(
        output_excel,
        index=False,
        header=False,
        engine="openpyxl"
    )

    print("Done.")
    print(f"Final shape: {df.shape}")


def propagate_mda_down(df, mda_col=4, source_col=0):
    print("Propagating MDA values downward...")
    
    # 🆕 STEP 1: Find first 10-digit value in column 0
    current_mda = None
    for i in range(1, len(df)):
        val = str(df.iloc[i, source_col]).strip()
        if val and val.lower() != "nan" and len(val) == 10:
            current_mda = val  # Found first anchor!
            break
    
    if not current_mda:
        print("⚠️  No 10-digit anchor found in source column")
        return
    
    # STEP 2: Normal propagation with initial anchor set
    filled_count = 0
    for i in range(1, len(df)):
        src_val = str(df.iloc[i, source_col]).strip()
        mda_val = str(df.iloc[i, mda_col]).strip()
        
        # Update anchor if new 10-digit value found
        if src_val and src_val.lower() != "nan" and len(src_val) == 10:
            current_mda = src_val
            df.iloc[i, mda_col] = current_mda
            continue
        
        # Fill empty cells with current anchor
        if (not mda_val or mda_val.lower() == "nan") and current_mda:
            df.iloc[i, mda_col] = current_mda
            filled_count += 1
    
    print(f"Propagated MDA to {filled_count} rows")


if __name__ == "__main__":
    # ===== CONFIG =====
    input_excel = "data/outputs/output_merged.xlsx"
    output_excel = "data/outputs/output_merged_with_mda.xlsx"

    add_mda_column(
        input_excel=input_excel,
        output_excel=output_excel
    )