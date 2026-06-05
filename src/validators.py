import pandas as pd
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class HRDataValidator:
    """
    Validates loaded HR datasets for quality and completeness.
    Generates a validation report for each dataset.
    """

    def validate_employees(self, df: pd.DataFrame) -> Tuple[bool, list]:
        """
        Validate employees dataset.
        Returns: (is_valid: bool, issues: list of strings)
        """
        issues = []

        if df['employee_id'].isnull().any():
            issues.append(" Null values in employee_id")

        if df['employee_id'].duplicated().any():
            issues.append(" Duplicate employee_id found")

        valid_offices = ['Dhahran', 'Jeddah', 'Riyadh']
        invalid_loc = ~df['office_location'].isin(valid_offices)
        if invalid_loc.any():
            issues.append(" Invalid office_location values found")

        is_valid = len(issues) == 0
        return is_valid, issues

    def validate_performance(self, df: pd.DataFrame) -> Tuple[bool, list]:
        """
        Validate performance reviews dataset.
        Returns: (is_valid: bool, issues: list of strings)
        """
        issues = []

        if df['employee_id'].isnull().any():
            issues.append(" Null values in employee_id")

        cols = ['technical_score', 'leadership_score', 'innovation_score']
        mask = ((df[cols] < 1) | (df[cols] > 5.05)).any().any()
        if mask:
            issues.append("Score out of range (must be 1.0 - 5.0)")


        is_valid = len(issues) == 0
        return is_valid, issues

    def generate_report(self, datasets: dict) -> None:
        """
        Run all validations and print a clean summary report.
        """
        print("\n" + "="*45)
        print("   HR DATA VALIDATION REPORT")
        print("="*45)

        for k, v in datasets.items():
            if v is None:
                print(f"\n {k.upper()}:   Dataset not loaded")
                continue

            if k == 'employees':
                is_valid, issues = self.validate_employees(v)
            elif k == 'performance':
                is_valid, issues = self.validate_performance(v)
            else:
                continue

            print(f"\n {k.upper()}")
            print(f"   Status: {' Valid' if is_valid else ' Issues found'}")
            for issue in issues:
                print(f"   - {issue}")

        print("\n" + "="*45)