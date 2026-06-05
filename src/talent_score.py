import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TalentScorer:
    """
    Ranks employees for promotion readiness using
    weighted scoring across performance, growth, and development.
    """

    def __init__(self, config: dict):
        # Load promotion_weights from config
        self.config = config
        self.promotion_weights = config["analysis"]["compensation"]["promotion_weights"]
        # performance, growth, development
        self.performance = config["analysis"]["compensation"]["promotion_weights"]["performance"]
        self.growth = config["analysis"]["compensation"]["promotion_weights"]["growth"]
        self.development = config["analysis"]["compensation"]["promotion_weights"]["development"]



    def compute_growth_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute growth score per employee.
        Formula: composite_score in latest quarter minus
        composite_score in earliest quarter.
        Returns dataframe with new column: growth_score
        """
        df_sorted = df.sort_values(['employee_id', 'review_quarter'])
        first = df_sorted.groupby('employee_id')['composite_score'].first()
        last = df_sorted.groupby('employee_id')['composite_score'].last()
        growth  = last - first 
        df_sorted['growth_score'] = df_sorted['employee_id'].map(growth)
        logger.info(f"'growth scores computed for {len(df_sorted)} records")
        return df_sorted


    def compute_development_score(self, df_training: pd.DataFrame) -> pd.DataFrame:
        """
        Compute development score per employee.
        Returns dataframe with employee_id and development_score.
        """
        df_training = df_training.copy()
        df_certified = df_training[df_training['certification_earned'] == True]
        df_certified['development_score'] = df_certified.groupby('employee_id')['training_id'].transform('count')
        df_ds = df_certified[['employee_id', 'development_score']].drop_duplicates(subset='employee_id')
        return df_ds

        
        

    def compute_promotion_score(self,
                                 df_performance: pd.DataFrame,
                                 df_training: pd.DataFrame) -> pd.DataFrame:
        """
        Combine performance, growth, and development scores
        using weights from config.
        Returns final ranked dataframe with promotion_score.
        """ 
        
        def normalize(series):
            return (series - series.min()) / (series.max() - series.min())
        # extracts growth and development scores
        development_score = self.compute_development_score(df_training)
        growth_score = self.compute_growth_score(df_performance)
        growth_score =growth_score[['employee_id', 'growth_score']].drop_duplicates(subset='employee_id')
        # group the performance score from performance_calculator.py
        performance_score =df_performance.groupby('employee_id')['composite_score'].mean().reset_index(name='performance_score')
        # merge them
        df_combined = growth_score.merge(development_score, on='employee_id',how='left')
        df_combined=df_combined.merge(performance_score, on='employee_id', how='left')
        df_combined['development_score'] = df_combined['development_score'].fillna(0)
        # normlaize them
        df_combined['perf_norm'] = normalize(df_combined['performance_score'])
        df_combined['growth_norm'] = normalize(df_combined['growth_score'])
        df_combined['dev_norm'] = normalize(df_combined['development_score'])
        # compute promotion weights
        df_combined['promotion_score'] = ((df_combined['perf_norm']* self.performance) +
        (df_combined['growth_norm'] * self.growth) + (df_combined['dev_norm']* self.development)
        )
        # rank 
        return df_combined.sort_values(by='promotion_score', ascending=False)        
