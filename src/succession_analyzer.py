import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)

class SuccessionAnalyzer:
    """
    Identifies succession candidates for critical roles
    based on performance and development.
    """

    
      
        

    def identify_ready_now(self,
                        df_employees: pd.DataFrame,
                        df_high_performers: pd.DataFrame,
                        df_training: pd.DataFrame) -> pd.DataFrame:
        """
        df_performance already has composite_score and average_score
        computed by PerformanceCalculator.
        We just filter on top of that.
        """
        #high_performers = calculator.identify_high_performers(df_performance)

        df_ready= df_training[(df_training['certification_earned'] == True) &
        (df_training['employee_id'].isin(df_high_performers['employee_id']))]
        df_ready =df_ready[['employee_id']]
        df_ready =df_ready.drop_duplicates()
        return df_ready 
    

    def map_succession_pipeline(self,
                                  df_ready: pd.DataFrame,
                                  df_employees: pd.DataFrame) -> pd.DataFrame:
        """
        Group succession candidates by department and office.
        Shows coverage: which departments have succession depth
        and which are at risk.
        Returns summary dataframe.
        """
        
        # merge df_ready and df_employees
        df_combined = pd.merge(df_ready, df_employees, on='employee_id', how ='left')
        # the output would show df_ready employee_id and the all emplyees data like department and office
        succession = (
            df_combined
            .groupby(['department', 'office_location'])['employee_id']
            .count()
            .reset_index(name='succession_candidates_count')
        )
        succession = (
            df_employees[['department', 'office_location']]
            .drop_duplicates() # to show zero 
            .merge(succession, on=['department', 'office_location'], how='left')
            .fillna({'succession_candidates_count': 0})
        )
        succession['status'] =np.where(
            succession['succession_candidates_count'] == 0, 
            'at risk', 
            'covered'
        )
        return succession
        
        
        