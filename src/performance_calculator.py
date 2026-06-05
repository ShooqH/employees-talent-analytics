import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class PerformanceCalculator:
    """
    Computes composite performance scores and trends
    for HR decision making.
    """

    def __init__(self, config: dict):
        # Load thresholds from config
        self.config = config
        # high_performer_rating
        self.high_performer_rating = config["analysis"]["performance_thresholds"]["high_performer_rating"]
        # decline_threshold
        self.decline_threshold = config["analysis"]["performance_thresholds"]["decline_threshold"]
        logger.info(f"PerformanceCalculator initialized — high performer threshold: {self.high_performer_rating}")
    def compute_composite_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute composite score per employee per quarter.
        Formula: average of technical_score, leadership_score, innovation_score
        Returns dataframe with new column: composite_score
        """
        df =df.copy()
        df['composite_score'] = df[['technical_score', 'leadership_score', 'innovation_score']].mean(axis=1)
        logger.info(f"Composite scores computed for {len(df)} records")
        return df

    def identify_high_performers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter employees whose average composite_score
        meets or exceeds high_performer_rating threshold from config.
        Returns dataframe of high performers only.
        """
        
         
        df['average_score'] =df.groupby('employee_id')['composite_score'].transform('mean')
        mask = df['average_score'] >= self.high_performer_rating
        high_performers= df[mask].drop_duplicates(subset='employee_id')
        high_performers = high_performers[['employee_id', 'average_score']]
        logger.info(f"Identified {len(high_performers)} high performers")
        return high_performers
        
    def detect_declining_talent(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify employees whose composite_score dropped
        by more than decline_threshold between their
        first and latest quarter.
        Returns dataframe of declining employees only.
        """
        df_cleaned = df.drop_duplicates(subset=['employee_id', 'review_quarter'], keep='last')       
        df_sorted = df_cleaned.sort_values(['employee_id', 'review_quarter'])
               
        first = df_sorted.groupby('employee_id')['composite_score'].first()
        last = df_sorted.groupby('employee_id')['composite_score'].last()
        score_drop_series = first - last
        
        final_drops = score_drop_series[score_drop_series >= self.decline_threshold]        
        results_df = final_drops.reset_index(name='score_drop')        
        logger.info(f"Identified {len(results_df)} talents_drop")
        return results_df
        
