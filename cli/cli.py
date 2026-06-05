import argparse
import yaml
import logging
from src.data_loader import HRDataLoader
from src.validators import HRDataValidator
from src.performance_calculator import PerformanceCalculator
from src.talent_score import TalentScorer
from src.report_generator import HRReportGenerator
from src.APIclient import HRApiClient
from src.succession_analyzer import SuccessionAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.yaml") -> dict:
    """Load config from yaml file."""
    try: 
        with open (config_path, 'r') as file: 
            config = yaml.safe_load(file)
        logger.info('config file loaded sccessfully:')
        return config
    except FileNotFoundError:
        logger.error('file not found')
        return {}

def load_and_validate_data(config: dict) -> dict:
    """Load all datasets and run validation."""
    loader = HRDataLoader(config_path="config.yaml")
    datasets = loader.load_all()
    validator = HRDataValidator()
    validator.generate_report(datasets)
    return datasets

def cmd_report(args, config: dict) -> None:
    """Handler for: python cli/hr_analytics.py report"""
    datasets = load_and_validate_data(config)
    df_performance = datasets['performance']
    calc = PerformanceCalculator(config)
    df_performance = calc.compute_composite_score(df_performance)
    # object generate 
    gen = HRReportGenerator(config)
    first =gen.generate_summary_stats(datasets, df_performance)
    # prepare for talent report
    declining_df = calc.detect_declining_talent(df_performance)
    df_training = datasets['training']
    talent_scorer = TalentScorer(config) 
    top_5 = talent_scorer.compute_promotion_score(df_performance, df_training)
    high_performers =calc.identify_high_performers(df_performance)
    second = gen.generate_talent_report(high_performers, declining_df, top_5)
    # combine dicts
    full_report = {**first, **second}
    gen.print_executive_report(full_report)
    

def cmd_top_talent(args, config: dict) -> None:
    """Handler for: python cli/hr_analytics.py top-talent"""
    datasets = load_and_validate_data(config)
    df_performance  = datasets['performance']
    df_training = datasets['training']
    calc = PerformanceCalculator(config)
    df_performance = calc.compute_composite_score(df_performance)
    talent_scorer = TalentScorer(config) 
    top_5 = talent_scorer.compute_promotion_score(df_performance, df_training)
    print(top_5)

def cmd_declining(args, config: dict) -> None:
    """Handler for: python cli/hr_analytics.py declining"""
    datasets = load_and_validate_data(config)
    df_performance = datasets['performance']
    calc = PerformanceCalculator(config)
    df_performance = calc.compute_composite_score(df_performance)
    declining = calc.detect_declining_talent(df_performance)
    print(declining)

def cmd_market(args, config: dict) -> None:
    """Handler for: python cli/hr_analytics.py market"""
    API =HRApiClient(base_url='https://api.exchangerate-api.com/v4')
    rate =API.get_exchange_rate()
    market =API.get_labor_market_index()
    print(rate)
    print(market)

def cmd_succession(args, config: dict) -> None:
    """Handler for: python -m cli.cli succession"""
    try:
        datasets = load_and_validate_data(config)
        df_employees = datasets['employees']
        df_training = datasets['training']
        df_performance = datasets['performance']

        calc = PerformanceCalculator(config)
        df_performance = calc.compute_composite_score(df_performance)
        high_performers = calc.identify_high_performers(df_performance)

        analyzer = SuccessionAnalyzer()
        ready_now = analyzer.identify_ready_now(df_employees, high_performers, df_training)
        pipeline = analyzer.map_succession_pipeline(ready_now, df_employees)

        print("\n SUCCESSION PIPELINE")
        print(pipeline.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="HR Talent Analytics CLI — Vision 2030 Workforce Intelligence"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Register your 4 commands here
    subparsers.add_parser("report",    help="Generate full executive report")
    subparsers.add_parser("top-talent", help="Show top 5 promotion candidates")
    subparsers.add_parser("declining", help="Show declining talent list")
    subparsers.add_parser("market",    help="Fetch live market indicators")
    subparsers.add_parser("succession", help="Show succession pipeline by department and office")

    args = parser.parse_args()
    config = load_config()

    # Route to the right command handler
    if args.command == "report":
        cmd_report(args, config)
    elif args.command == "top-talent":
        cmd_top_talent(args, config)
    elif args.command == "declining":
        cmd_declining(args, config)
    elif args.command == "market":
        cmd_market(args, config)
    elif args.command == "succession":
        cmd_succession(args, config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()