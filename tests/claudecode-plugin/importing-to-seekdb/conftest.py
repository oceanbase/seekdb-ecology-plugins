# pytest configuration for importing-data-files skill tests
import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent.parent.parent.parent / "claudecode-plugin" / "skills" / "importing-to-seekdb" / "scripts"
sys.path.insert(0, str(scripts_dir))
