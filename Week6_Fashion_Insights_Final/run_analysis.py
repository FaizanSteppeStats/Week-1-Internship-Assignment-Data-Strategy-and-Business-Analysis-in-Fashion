from pathlib import Path
import json
from src.decision_brief import create_brief
if __name__=='__main__':print(json.dumps(create_brief(Path(__file__).resolve().parent),indent=2))
