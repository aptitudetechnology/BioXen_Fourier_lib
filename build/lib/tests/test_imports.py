import sys
from pathlib import Path

modules_to_test = [
    "questionary",
    "genome.parser",
    "genome.schema",
    "hypervisor.core",
    "chassis"
]

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("Testing module imports...")

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ Successfully imported {module}")
    except ImportError as e:
        print(f"❌ Failed to import {module}: {e}")

print("Import test completed.")
