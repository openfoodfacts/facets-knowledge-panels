"""
This script builds the static HTML dump of information knowledge panels
from a content YAML file.
"""

import argparse
from pathlib import Path

from app.information_kp import build_content
from app.settings import HTML_DIR

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    args = parser.parse_args()
    build_content(HTML_DIR, args.file_path)
