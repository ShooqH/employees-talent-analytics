import pandas as pd
from src.performance_calculator import PerformanceCalculator

def test_composite_score_correct_value():
    # ARRANGE — build the smallest possible input
    df = pd.DataFrame({
        'employee_id':       [1],
        'technical_score':   [4.0],
        'leadership_score':  [3.0],
        'innovation_score':  [5.0]
    })
    config = {
        "analysis": {
            "performance_thresholds": {
                "high_performer_rating": 4.5,
                "decline_threshold": 0.3
            }
        }
    }
    # ACT -call the input 
    clc = PerformanceCalculator(config)
    score = clc.compute_composite_score(df)
    # ASSERT -check output
    assert score['composite_score'].iloc[0] == 4
    assert 'composite_score' in score.columns
    assert len(score) == 1

def test_high_performers_meet_threshold(): 
    # ARRANAGE -build the input 
    df = pd.DataFrame({
    'employee_id':     [1, 1, 2, 2],
    'review_quarter':  ['2024-Q1', '2024-Q2', '2024-Q1', '2024-Q2'],
    'composite_score': [4.6, 4.6, 3.0, 3.0]
})
    config = {
        "analysis": {
            "performance_thresholds": {
                "high_performer_rating": 4.5,
                "decline_threshold": 0.3
            }
        }
    }
    # ACT -call the function 
    cal = PerformanceCalculator(config)
    high = cal.identify_high_performers(df)
    # ASSERT -check output
    assert high['average_score'].iloc[0] >= 4.5
    assert high['employee_id'].iloc[0] == 1
    assert len(high) == 1


def test_declining_talent_detected(): 
    #ARRANGE
    df=pd.DataFrame({
        'employee_id':      [1, 1, 2, 2],
        'review_quarter':   ['2024-Q1', '2024-Q2', '2024-Q1', '2024-Q2'],
        'composite_score':  [4.0, 4.5, 3.0, 2.5]
    })
    config = {
        "analysis": {
            "performance_thresholds": {
                "high_performer_rating": 4.5,
                "decline_threshold": 0.3
            }
        }
    }
    # ACT 
    cal = PerformanceCalculator(config)
    decline_talent = cal.detect_declining_talent(df)
    # ASSERT 
    assert 2 in decline_talent['employee_id'].values
    assert 0.5 in decline_talent['score_drop'].values


