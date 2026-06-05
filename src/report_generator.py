import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HRReportGenerator:
    """
    Compiles HR analytics results into structured reports
    for executive consumption.
    """

    def __init__(self, config: dict):
        # load config
        self.config =config
        # set output format from config
        self.output_format = config['reporting']['output_format']
    

    def generate_summary_stats(self, datasets: dict, df_performance: pd.DataFrame) -> dict:
        """
        Generate high-level summary statistics across all datasets.
        Returns dict with key metrics.
        """
        # get datasets from dict
        df_employees = datasets.get("employees")
        df_projects = datasets.get("projects")
        df_training = datasets.get("training")
        # return dict
        summary = {
            'total_employees':df_employees['employee_id'].nunique(),
            'total_assignments': df_projects['assignment_id'].nunique(),
            "avg_performance_score": round(df_performance['composite_score'].mean(), 2),
            'total_training_records': df_training['training_id'].nunique()
        }


        return summary

    def generate_talent_report(self,
                                high_performers: pd.DataFrame,
                                declining: pd.DataFrame,
                                promotion_ranking: pd.DataFrame) -> dict:
        """
        Compile talent analytics into a structured report dict.
        """
        df_pro =promotion_ranking.sort_values(by='promotion_score', ascending=False).head(5)
        df_pro =df_pro[['employee_id', 'promotion_score']]
        summary = {
            'num_high_performers': high_performers['employee_id'].nunique(), 
            'num_declining': declining['employee_id'].nunique(),
            'top_5_candidates': df_pro.to_dict(orient='records'), 
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
  
        return summary

    def print_executive_report(self, report: dict) -> None:
        """
        Print a clean, formatted executive summary to console.
        """
        print("=" * 60)
        print("HR TALENT ANALYTICS EXECUTIVE REPORT")
        print(f"Generated: {report['generated_at']}")
        print("=" * 60)

        print("\n WORKFORCE OVERVIEW")
        print(f"Total Employees        : {report['total_employees']}")
        print(f"Project Assignments    : {report['total_assignments']}")
        print(f"Training Records       : {report['total_training_records']}")
        print(f"Avg Performance Score  : {report['avg_performance_score']}")

        print("\n TALENT HIGHLIGHTS")
        print(f"  High Performers        : {report['num_high_performers']} employees")
        print(f"  Declining Talent       : {report['num_declining']} employees")

        print("\n TOP 5 PROMOTION CANDIDATES") # there is no rank  column
        for i, row in enumerate(report['top_5_candidates'], 1):
            print(f"  Rank {i}  |  Employee {row['employee_id']}  |  Score: {row['promotion_score']:.3f}")

        print("\n" + "=" * 60)
        logger.info("Executive report printed successfully")
    
