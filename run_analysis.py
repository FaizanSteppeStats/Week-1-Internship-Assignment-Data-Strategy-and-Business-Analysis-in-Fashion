"""Run the complete reproducible fashion-data analysis offline."""
from pathlib import Path
import json
from src.fashion_strategy_demo import generate_synthetic_data, analyse
from src.case_study_analysis import calculate_case_study

def main():
    root=Path(__file__).resolve().parent
    generate_synthetic_data(root/'data',seed=42)
    analyse(root/'data',root/'outputs')
    print(json.dumps(calculate_case_study(root),indent=2))

if __name__=='__main__':
    main()
