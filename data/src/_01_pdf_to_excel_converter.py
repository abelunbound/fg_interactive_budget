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

Author: Abel O. Akeni
Created: 2026-01-09
Python: 3.8+
"""

from typing import Tuple #List, 
import camelot # pylint: disable=no-member
import pandas as pd

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
            flavor='stream',
            row_tol=row_tol,
            column_tol=column_tol  # Critical for column detection
        )
        return tables
    
    def extract_with_adaptive_params(self, pages: str):
        """
        Try multiple parameter combinations to find best extraction.
        Useful when table structure varies across pages.
        """
        param_combinations = [
            {'row_tol': 3, 'column_tol': 2},  # Most sensitive
            {'row_tol': 3, 'column_tol': 3},  # Moderate
            {'row_tol': 3, 'column_tol': 5},  # Less sensitive
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