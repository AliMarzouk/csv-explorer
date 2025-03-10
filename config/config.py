import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'output')
OUTPUT_TMP_FOLDER = os.path.join(OUTPUT_FOLDER, 'tmp')
OUTPUT_TMP_CSV_FILE = os.path.join(OUTPUT_TMP_FOLDER, 'tmp.csv')
OUTPUT_CSV_FILE = os.path.join(OUTPUT_FOLDER, 'inter.csv')