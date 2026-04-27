# flake8: noqa
# pylint: skip-file

import pandas as pd


def merge_excel_sheets_to_one(
    input_excel: str,
    output_excel: str,
    output_sheet_name: str = "ALL_TABLES",
    empty_rows_between: int = 1
):
    """
    Merge all sheets from an Excel file into a single sheet by stacking vertically.

    - Preserves each table as-is
    - Adds empty rows between tables
    - Supports different column counts
    - Keeps original cell contents untouched

    Args:
        input_excel: Path to source Excel (multi-sheet)
        output_excel: Path to output Excel (single-sheet)
        output_sheet_name: Name of the merged sheet
        empty_rows_between: Number of empty rows between tables
    """

    print(f"Reading: {input_excel}")
    xls = pd.ExcelFile(input_excel, engine="openpyxl") # pylint: disable=no-member

    all_blocks = []

    for idx, sheet_name in enumerate(xls.sheet_names):
        print(f"  → Loading sheet: {sheet_name}")

        df = pd.read_excel(
            xls,
            sheet_name=sheet_name,
            header=None,     # IMPORTANT: preserve raw layout
            dtype=str        # Prevent pandas from messing with numbers
        )

        # Append table
        all_blocks.append(df)

        # Append empty spacer rows (except after last sheet)
        if idx < len(xls.sheet_names) - 1 and empty_rows_between > 0:
            spacer = pd.DataFrame(
                [[""] * df.shape[1]] * empty_rows_between
            )
            all_blocks.append(spacer)

    print("Stacking all tables vertically...")

    final_df = pd.concat(all_blocks, ignore_index=True)

    print(f"Writing output: {output_excel}")

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        final_df.to_excel(
            writer,
            sheet_name=output_sheet_name,
            index=False,
            header=False
        )

    print("Done.")
    print(f"Final shape: {final_df.shape}")


if __name__ == "__main__":
    # ===== CONFIG =====
    input_excel = "data_approved/outputs/output.xlsx"           # Your multi-sheet file
    output_excel = "data_approved/outputs/output_merged.xlsx"   # New single-sheet file

    merge_excel_sheets_to_one(
        input_excel=input_excel,
        output_excel=output_excel,
        output_sheet_name="ALL_TABLES",
        empty_rows_between=1
    )
