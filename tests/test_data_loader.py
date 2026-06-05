import pytest
from pathlib import Path
from src.data_loader import HRDataLoader

def test_load_all_returns_five_keys(tmp_path):
    # 1. ARRANGE
    # Create the 5 expected CSV files inside a temp directory
    required_files = [
        "employees.csv", 
        "project_assignments.csv", 
        "salary_history.csv", 
        "performance_reviews.csv", 
        "training_history.csv"
    ]
    for file_name in required_files:
        (tmp_path / file_name).write_text("col1,col2\nval1,val2")
    
    # Instantiate loader (it will default to an empty config if config.yaml doesn't exist)
    loader = HRDataLoader(config_path="non_existent_config.yaml")
    # Redirect its raw path to our temporary folder
    loader.raw_path = tmp_path

    # 2. ACT
    result = loader.load_all()
    
    # 3. ASSERT
    expected_keys = {"employees", "projects", "salary", "performance", "training"}
    
    assert isinstance(result, dict)
    assert set(result.keys()) == expected_keys

def test_missing_file_returns_none(tmp_path):
    # 1. ARRANGE
    # tmp_path is completely empty, so any file requested will be missing
    loader = HRDataLoader(config_path="non_existent_config.yaml")
    # Override raw_path because config is empty (invalid config path used)
    loader.raw_path = tmp_path 

    # 2. ACT
    # Attempting to load employees when employees.csv doesn't exist
    result = loader.load_employees()

    # 3. ASSERT
    assert result is None



def test_invalid_config_uses_fallback_path():
    # 1. ARRANGE
    # Pass a path that does not exist
    invalid_config_path = "this_file_does_not_exist_anywhere.yaml"

    # 2. ACT
    loader = HRDataLoader(config_path=invalid_config_path)

    # 3. ASSERT
    # Verify that it didn't crash, config is empty, and raw_path fell back gracefully
    assert loader.config == {}
    assert loader.raw_path == Path('data/raw')