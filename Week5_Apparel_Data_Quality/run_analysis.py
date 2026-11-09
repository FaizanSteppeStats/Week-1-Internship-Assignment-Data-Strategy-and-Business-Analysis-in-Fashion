from pathlib import Path
import json
from src.quality_assessment import run_quality
if __name__=='__main__':
    print(json.dumps(run_quality(Path(__file__).resolve().parent),indent=2))
