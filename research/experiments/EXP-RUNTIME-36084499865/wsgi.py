import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_experiment import create_app
application = create_app("/tmp/spider-runtime/36044045537/single.db")
