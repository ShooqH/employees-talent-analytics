import pandas as pd
import logging
import yaml
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HRDataLoader:
    """
    Production-grade data loader for HR Talent Analytics.
    Handles ingestion of all 5 raw CSV files with error handling.
    """

    def __init__(self, config_path: str = 'config.yaml'):
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            logger.info("Config file loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load config file: {e}")
            self.config = {}

        try:
            raw_path_str = self.config.get('data', {}).get('raw_path', 'data/raw')
            self.raw_path = Path(raw_path_str)
            logger.info(f"Raw data path set to: {self.raw_path}")
        except Exception as e:
            logger.error(f"Error setting raw data path: {e}")
            self.raw_path = Path('data/raw')

        self.employees = None
        self.projects = None
        self.performance = None
        self.training = None
        self.salary = None

    def load_all(self) -> dict:
        """Load all datasets and return as dictionary."""
        logger.info("Starting to load all datasets...")
        self.employees = self.load_employees()
        self.projects = self.load_projects()
        self.salary = self.load_salary()
        self.performance = self.load_performance()
        self.training = self.load_training()

        data = {
            "employees": self.employees,
            "projects": self.projects,
            "salary": self.salary,
            "performance": self.performance,
            "training": self.training
        }
        logger.info("All datasets loaded successfully")
        return data

    def load_employees(self) -> pd.DataFrame:
        """Load and return employees dataset."""
        return self._load_csv("employees.csv")

    def load_projects(self) -> pd.DataFrame:
        """Load and return project assignments dataset."""
        return self._load_csv("project_assignments.csv")

    def load_performance(self) -> pd.DataFrame:
        """Load and return performance reviews dataset."""
        return self._load_csv("performance_reviews.csv")

    def load_training(self) -> pd.DataFrame:
        """Load and return training history dataset."""
        return self._load_csv("training_history.csv")

    def load_salary(self) -> pd.DataFrame:
        """Load and return salary history dataset."""
        return self._load_csv("salary_history.csv")

    def _load_csv(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Private method: load a single CSV with error handling.
        Log success or failure. Never crash silently.
        """
        try:
            filepath = self.raw_path / filename
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            return None
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            return None