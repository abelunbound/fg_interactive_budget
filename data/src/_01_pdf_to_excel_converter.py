"""
Nigerian Budget PDF to Excel Converter
=======================================

Extracts tables from Nigerian government appropriation bill PDFs into Excel spreadsheets.

Key Challenge Solved:
---------------------
Nigerian budget PDFs have TYPE column (ONGOING/NEW/COMPLETED) merged with PROJECT NAME.
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

Author: [Your Name]
Created: 2026-01-09
Python: 3.8+
"""