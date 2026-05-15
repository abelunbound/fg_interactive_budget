# flake8: noqa
"""
Nigerian Budget PDF to Excel Converter
=======================================

Extracts tables from Nigerian government appropriation bill PDFs into Excel
spreadsheets.

Key Challenge Solved:
---------------------
Nigerian budget PDFs have TYPE column (ONGOING/NEW/COMPLETED) merged 
with PROJECT NAME.
Example: "BUILD ROAD.ONGOING" instead of separate columns.

This tool:
1. Detects ERGP project tables (checks for ERGP codes)
2. Splits merged TYPE values from PROJECT NAME
3. Merges multi-line project descriptions
4. Preserves non-ERGP tables (LINE ITEM, Budget summaries)

Architecture:
-------------
PDFToExcelConverter (Orchestrator)
├── PDFTableExtractor (Camelot interface)
├── TableCleaner (Post-processing logic)
└── ExcelExporter (Excel output handler)

Design Decisions:
-----------------
1. Why column_tol=1?
   - ERGP tables have narrow TYPE column with minimal spacing
   - Tested values 1-10, found 1 works for 95% of cases
   - Trade-off: May over-split some tables with wide word spacing

2. Why post-process TYPE column instead of better extraction parameters?
   - PDF source has TYPE physically concatenated to PROJECT NAME text
   - Camelot can't split text that's merged at PDF level
   - Regex splitting is deterministic and testable

3. Why process order: TYPE fix → then merge continuation rows?
   - TYPE fix creates correct 4-column structure
   - Continuation row merging expects correct columns
   - Reversing this order would require re-detecting column indices

4. Why class constant for TYPE_VALUES?
   - Nigerian budgets use consistent TYPE values
   - Single source of truth, easy to update
   - Memory efficient (created once, not per-table)

Usage:
------
    from pdf_to_excel_converter import PDFToExcelConverter

    converter = PDFToExcelConverter('budget.pdf', 'output.xlsx')
    converter.convert(pages='1-10', column_tol=1, row_tol=3)

Parameters:
-----------
column_tol (int): Horizontal spacing threshold for column detection
    - Lower = more sensitive = more columns detected
    - Range: 1-10, Default: 1
    - Use 1 for ERGP tables (TYPE column separation)

row_tol (int): Vertical spacing threshold for row grouping
    - Lower = more rows, Higher = more merging
    - Range: 1-15, Default: 3
    - Increase if multi-line descriptions not combining

Author: Abel O. Akeni
Created: 2026-01-09
Python: 3.8+
"""

from typing import Tuple  # List,
import camelot  # pylint: disable=no-member
import pandas as pd


import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"[TIMER] {func.__name__} took {elapsed:.2f} seconds")
    return wrapper


class PDFTableExtractor:
    """Handles PDF table extraction using Camelot."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_tables(self, pages: str, row_tol: int = 3, column_tol: int = 3):
        """
        Extract tables from specified PDF pages.

        Args:
            pages: Page range (e.g., '1-10', '1,3,5')
            row_tol: Row tolerance for text grouping (vertical)
            column_tol: Column tolerance for detecting column separators (horizontal)
                       Lower values = more sensitive to spacing = more columns detected

        Returns:
            TableList object containing extracted tables
        """
        tables = camelot.read_pdf(
            self.pdf_path,
            pages=pages,
            flavor="stream",
            # flavor="lattice",
            row_tol=row_tol,
            column_tol=column_tol,  # Critical for column detection
        )

        return tables

    def extract_with_adaptive_params(self, pages: str):
        """
        Try multiple parameter combinations to find best extraction.
        Useful when table structure varies across pages.
        """
        param_combinations = [
            {"row_tol": 8, "column_tol": 2},  # Most sensitive
            {"row_tol": 3, "column_tol": 3},  # Moderate
            {"row_tol": 3, "column_tol": 5},  # Less sensitive
        ]

        best_tables = None
        best_score = 0

        for params in param_combinations:
            tables = self.extract_tables(pages, **params)

            # Simple scoring: prefer extractions with correct column count
            # For ERGP tables, we expect 4 columns: CODE, NAME, TYPE, AMOUNT
            score = sum(1 for t in tables if t.df.shape[1] == 4)

            if score > best_score:
                best_score = score
                best_tables = tables

        return best_tables


class TableCleaner:
    """Handles post-processing and cleaning of extracted tables."""

    TYPE_VALUES = ["ONGOING", "NEW", "COMPLETED", "SUSPENDED"]

    @staticmethod
    def merge_continuation_rows(
        df: pd.DataFrame, code_col: int = 0, name_col: int = 1
    ) -> Tuple[pd.DataFrame, int]:
        """
        Merge rows where CODE column is empty (continuation rows).

        Args:
            df: DataFrame to process
            code_col: Index of CODE column
            name_col: Index of PROJECT NAME column

        Returns:
            Tuple of (cleaned DataFrame with merged rows, number of rows merged)
        """
        df = df.copy()
        rows_to_drop = []

        for i in range(1, len(df)):  # Skip header row
            code_value = str(df.iloc[i, code_col]).strip()

            # Check if this is a continuation row (empty CODE)
            if TableCleaner._is_empty_code(code_value):
                # Merge with previous row
                prev_row_idx = i - 1
                current_name = str(df.iloc[i, name_col]).strip()

                if current_name and current_name != "nan":
                    prev_name = str(df.iloc[prev_row_idx, name_col]).strip()
                    df.iloc[prev_row_idx, name_col] = f"{prev_name} {current_name}"

                rows_to_drop.append(i)

        # Drop continuation rows and reset index
        df = df.drop(rows_to_drop).reset_index(drop=True)

        return df, len(rows_to_drop)

    # ### Fix  
    # @staticmethod
    # def merge_continuation_rows(
    #     df: pd.DataFrame, code_col: int = 0, name_col: int = 1
    # ) -> Tuple[pd.DataFrame, int]:
    #     """
    #     Merge rows where CODE column is empty (continuation rows).

    #     Uses midpoint split on gaps between ERGP rows:
    #     - First floor(N/2) empty rows → post-code orphans, appended to ERGP_A
    #     - Last  ceil(N/2) empty rows → pre-code orphans, prepended to ERGP_B

    #     Args:
    #         df: DataFrame to process
    #         code_col: Index of CODE column
    #         name_col: Index of PROJECT NAME column

    #     Returns:
    #         Tuple of (cleaned DataFrame with merged rows, number of rows merged)
    #     """
    #     df = df.copy()
    #     rows_to_drop = []

    #     # Only look at ERGP rows — ignore non-ERGP non-empty rows (headers, totals, etc.)
    #     ergp_indices = [
    #         i for i in range(len(df))
    #         if str(df.iloc[i, code_col]).strip().upper().startswith("ERGP")
    #     ]

    #     def _name(idx):
    #         v = str(df.iloc[idx, name_col]).strip()
    #         return v if v and v != "nan" else ""

    #     def _append(idx, text):
    #         base = _name(idx)
    #         df.iloc[idx, name_col] = f"{base} {text}".strip() if base else text

    #     def _prepend(idx, text):
    #         base = _name(idx)
    #         df.iloc[idx, name_col] = f"{text} {base}".strip() if base else text

    #     # --- Process gaps between consecutive ERGP rows ---
    #     for k in range(len(ergp_indices) - 1):
    #         a = ergp_indices[k]      # ERGP_A index
    #         b = ergp_indices[k + 1]  # ERGP_B index

    #         # Empty-code rows strictly between a and b
    #         gap = [
    #             i for i in range(a + 1, b)
    #             if TableCleaner._is_empty_code(str(df.iloc[i, code_col]).strip())
    #         ]
    #         N = len(gap)
    #         if N == 0:
    #             continue
    #         # ----- Fix for wrong cells being merged to project names
    #         if N == 1:
    #             b_name = _name(b)
    #             if b_name:  # B already has content → orphan is tail of A
    #                 text = _name(gap[0])
    #                 if text:
    #                     _append(a, text)
    #             else:       # B is empty → orphan is head of B
    #                 text = _name(gap[0])
    #                 if text:
    #                     _prepend(b, text)
    #             rows_to_drop.extend(gap)
    #             continue
    #         # ---- Fix for wrong cells being merged to project names

    #         n_post = N // 2       # goes to ERGP_A (post-code)
    #         n_pre  = N - n_post   # goes to ERGP_B (pre-code)

    #         # Post-code: append in order to ERGP_A
    #         for idx in gap[:n_post]:
    #             text = _name(idx)
    #             if text:
    #                 _append(a, text)

    #         # Pre-code: prepend in order to ERGP_B
    #         pre_texts = [_name(idx) for idx in gap[n_post:] if _name(idx)]
    #         if pre_texts:
    #             _prepend(b, " ".join(pre_texts))

    #         rows_to_drop.extend(gap)

    #     # --- Empty rows after last ERGP: append to last ERGP ---
    #     if ergp_indices:
    #         last = ergp_indices[-1]
    #         for i in range(last + 1, len(df)):
    #             if TableCleaner._is_empty_code(str(df.iloc[i, code_col]).strip()):
    #                 text = _name(i)
    #                 if text:
    #                     _append(last, text)
    #                 rows_to_drop.append(i)

    #     ## --- Empty rows before first ERGP: drop silently ---
    #     # if ergp_indices:
    #     #     first = ergp_indices[0]
    #     #     for i in range(1, first):
    #     #         if TableCleaner._is_empty_code(str(df.iloc[i, code_col]).strip()):
    #     #             rows_to_drop.append(i)

    #     # # --- Empty rows before first ERGP: prepend to first ERGP ---
    #     # if ergp_indices:
    #     #     first = ergp_indices[0]
    #     #     pre_texts = []
    #     #     for i in range(1, first):
    #     #         if TableCleaner._is_empty_code(str(df.iloc[i, code_col]).strip()):
    #     #             text = _name(i)
    #     #             if text:
    #     #                 pre_texts.append(text)
    #     #             rows_to_drop.append(i)
    #     #     if pre_texts:
    #     #         _prepend(first, " ".join(pre_texts))

    #     # --- Empty rows before first ERGP: prepend only adjacent orphans ---
    #     if ergp_indices:
    #         first = ergp_indices[0]
    #         # Walk backwards from first ERGP, collect only consecutive empty rows
    #         adjacent = []
    #         for i in range(first - 1, 0, -1):
    #             if TableCleaner._is_empty_code(str(df.iloc[i, code_col]).strip()):
    #                 text = _name(i)
    #                 adjacent.append((i, text))
    #             else:
    #                 break  # stop at first non-empty-code row
    #         # Reverse to restore original order, prepend to first ERGP
    #         adjacent.reverse()
    #         pre_texts = [text for _, text in adjacent if text]
    #         rows_to_drop.extend([i for i, _ in adjacent])
    #         if pre_texts:
    #             _prepend(first, " ".join(pre_texts))


    #     df = df.drop(list(set(rows_to_drop))).reset_index(drop=True)
    #     return df, len(set(rows_to_drop))
        

    @staticmethod
    def _is_empty_code(code_value: str) -> bool:
        """Check if a code value is empty or invalid."""
        return not code_value or code_value in ("", "nan", "None")

    @staticmethod
    def is_ergp_table(df: pd.DataFrame) -> bool:
        """
        Check if table contains ERGP project codes.
        ERGP codes start with 'ERGP' followed by numbers.

        Args:
            df: DataFrame to check

        Returns:
            True if table contains ERGP codes, False otherwise
        """
        # Check first few rows of column 0 (CODE column)
        for i in range(min(20, len(df))):
            code = str(df.iloc[i, 0]).strip().upper()
            if code.startswith("ERGP"):
                return True
        return False

    @staticmethod
    def fix_merged_type_column(df: pd.DataFrame) -> pd.DataFrame:
        """
        Fix ERGP tables where TYPE column is merged with PROJECT NAME.
        Only applies to 3-column ERGP tables.

        Background:
            Some ERGP tables have TYPE (ONGOING/NEW/COMPLETED) concatenated
            to PROJECT NAME like "BUILD ROAD.ONGOING" instead of separate columns.
            This happens at PDF source level - not a Camelot extraction issue.

        Args:
            df: DataFrame with 3 columns (CODE, PROJECT_NAME+TYPE, AMOUNT)

        Returns:
            DataFrame with 4 columns (CODE, PROJECT_NAME, TYPE, AMOUNT)

        Side Effects:
            - Inserts new column at position 2 (between PROJECT NAME and AMOUNT)
            - Modifies PROJECT NAME column (removes TYPE suffix)
            - Logs number of rows where TYPE was extracted

        Example:
            Before (3 columns):
                0: ERGP123 | 1: BUILD ROAD.ONGOING | 2: 1,000,000

            After (4 columns):
                0: ERGP123 | 1: BUILD ROAD | 2: ONGOING | 3: 1,000,000

        Note:
            Only recognizes TYPE_VALUES: ONGOING, NEW, COMPLETED, SUSPENDED.
            If PDF has different TYPE values, add them to TYPE_VALUES constant.

            Handles separators: period (.), comma (,), space ( )
            Example: "...ONGOING", "...,ONGOING", "... ONGOING" all work
        """
        df = df.copy()

        # WHY: Insert at position 2 specifically?
        # ERGP tables have structure: CODE (0) | PROJECT_NAME (1) | AMOUNT (2)
        # We want: CODE (0) | PROJECT_NAME (1) | TYPE (2) | AMOUNT (3)
        # So TYPE goes between PROJECT_NAME and AMOUNT
        new_col_name = len(df.columns)
        df.insert(2, new_col_name, "")

        rows_fixed = 0

        # WHY: Loop through all rows instead of vectorized operation?
        # Because we need to check multiple TYPE values per row with early break
        # Pandas doesn't have clean vectorized "endswith any of these" + extract
        for i in range(len(df)):
            project_name = str(df.iloc[i, 1])

            # WHY: Check each TYPE value in order?
            # Try most common first (ONGOING), fail fast if not found
            # Break after first match to avoid double-processing
            for type_val in TableCleaner.TYPE_VALUES:
                if project_name.upper().endswith(type_val):
                    # WHY: Remove and strip in one operation?
                    # project_name[:-len(type_val)] removes TYPE
                    # .rstrip('., ') removes trailing separators (., comma, space)
                    # Example: "BUILD ROAD.ONGOING" → "BUILD ROAD." → "BUILD ROAD"
                    cleaned_name = project_name[: -len(type_val)].rstrip("., ")
                    df.iloc[i, 1] = cleaned_name
                    df.iloc[i, 2] = type_val
                    rows_fixed += 1
                    break  # WHY break? Only one TYPE per project

        # WHY: Log only if rows_fixed > 0?
        # Avoid cluttering output for tables that don't need fixing
        if rows_fixed > 0:
            print(
                f"    → Fixed merged TYPE column: {rows_fixed} rows had TYPE extracted"
            )

        return df


class ExcelExporter:
    """Handles exporting tables to Excel."""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.writer = None

    def __enter__(self):
        self.writer = pd.ExcelWriter(self.output_path, engine="openpyxl")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.writer:
            self.writer.close()

    def export_table(self, df: pd.DataFrame, sheet_name: str):
        """
        Export a DataFrame to a sheet in the Excel file.

        Args:
            df: DataFrame to export
            sheet_name: Name for the Excel sheet (max 31 chars)
        """
        # Truncate sheet name to Excel's limit
        sheet_name = sheet_name[:31]
        df.to_excel(self.writer, sheet_name=sheet_name, index=False, header=False)


class PDFToExcelConverter:
    """Main orchestrator for PDF to Excel conversion."""

    def __init__(self, pdf_path: str, output_path: str):
        self.extractor = PDFTableExtractor(pdf_path)
        self.cleaner = TableCleaner()
        self.output_path = output_path

    def convert(
        self,
        pages: str = "1-10",
        merge_rows: bool = True,
        row_tol: int = 3,
        column_tol: int = 1,
    ) -> dict:
        """
        Convert PDF tables to Excel.

        Args:
            pages: Page range to extract
            merge_rows: Whether to merge continuation rows
            row_tol: Row tolerance for text grouping
            column_tol: Column tolerance (use 1-3 for ERGP tables to separate TYPE column)

        Returns:
            Dictionary with conversion statistics
        """
        # Extract tables with optimal parameters
        tables = self.extractor.extract_tables(
            pages, row_tol=row_tol, column_tol=column_tol
        )
        print(f"Found {tables.n} tables\n")

        stats = {
            "total_tables": tables.n,
            "tables_processed": [],
            "total_rows_merged": 0,
        }

        # # Process and export
        # with ExcelExporter(self.output_path) as exporter:
        #     for idx, table in enumerate(tables):
        #         df = table.df.copy()

        # ---Fix for duplicate tables Process and export
        seen_tables = {}  # key: page number, value: set of df hashes
        with ExcelExporter(self.output_path) as exporter:
            for idx, table in enumerate(tables):
                df = table.df.copy()

                # Deduplicate: skip if identical table already seen on this page
                df_hash = pd.util.hash_pandas_object(df).sum()
                if table.page in seen_tables and df_hash in seen_tables[table.page]:
                    print(f"Table {idx+1} (Page {table.page}): duplicate, skipping")
                    continue
                seen_tables.setdefault(table.page, set()).add(df_hash)
                # ---Fix for duplicate tables ---


                ##### Added 27 Apr 2026 - troubleshooting
                # ##### Added 27 Apr 2026 - troubleshooting
                print(f"\n=== RAW TABLE {idx+1} (Page {table.page}) shape={df.shape} ===")
                for row_i, row in df.iterrows():
                    print(f"  [{row_i}] CODE='{row.iloc[0]}' | NAME='{row.iloc[1]}'")
                print("---")

                ##### Added 27 Apr 2026 - troubleshooting

                rows_merged = 0

                print(f"Found {tables.n} tables\n", flush=True)  # ← Add flush=True
                # PROCESSING ORDER IS CRITICAL:
                #
                # Step 1: Fix TYPE column FIRST (if needed)
                # WHY FIRST? Creates correct 4-column structure before row merging
                # If we merge rows first on 3-column structure, then add TYPE column,
                # we'd need to re-detect which column indices to use for merging
                if df.shape[1] == 3 and self.cleaner.is_ergp_table(df):
                    df = self.cleaner.fix_merged_type_column(df)

                # Step 2: Merge continuation rows AFTER TYPE fix
                # WHY AFTER? Continuation row merging expects correct column structure
                # Works on column 0 (CODE) and column 1 (PROJECT_NAME)
                # If TYPE column doesn't exist yet, indices would be wrong
                if merge_rows and df.shape[0] > 1:  # Skip if only header
                    df, rows_merged = self.cleaner.merge_continuation_rows(df)

                # Generate sheet name
                sheet_name = f"Page_{table.page}_T{idx + 1}"

                # Export to Excel
                exporter.export_table(df, sheet_name)

                # Track statistics
                table_stat = {
                    "table_num": idx + 1,
                    "page": table.page,
                    "rows_merged": rows_merged,
                    "final_shape": df.shape,
                    "accuracy": table.accuracy,
                }
                stats["tables_processed"].append(table_stat)
                stats["total_rows_merged"] += rows_merged

                print(
                    f"Table {idx + 1} (Page {table.page}): "
                    f"{rows_merged} rows merged, "
                    f"final shape: {df.shape}, "
                    f"accuracy: {table.accuracy:.2f}%",
                    flush=True,
                )

        print(f"\nSaved to {self.output_path}")
        return stats





@timed
def main():
    """Main execution function."""
    # Configuration
    pdf_path = "data_approved/inputs/approved_2026_budget.pdf"
    output_path = "data_approved/outputs/output.xlsx"
    pages = "288-291"
    # pages = "497-503"
    # pages = "1524-1527" #Ministry of Works and Housing to test project names greater than 6 lines

    # Convert
    converter = PDFToExcelConverter(pdf_path, output_path)
    stats = converter.convert(pages=pages, merge_rows=True, row_tol=4, column_tol=1)
    # stats = converter.convert(pages=pages, merge_rows=True)


    # Summary
    print(f"{'=' * 60}")
    print("CONVERSION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total tables extracted: {stats['total_tables']}")
    print(f"Total rows merged: {stats['total_rows_merged']}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()

# script _01 needss file in "data_approved/inputs/2026 Appropriation Bill Details.pdf"
# script _02 needss file in "data_approved/outputs/output.xlsx"
# script _03 needss file in "data_approved/outputs/output_merged.xlsx" 
# script _04 needss file in "data_approved/outputs/output_merged_with_mda.xlsx"
