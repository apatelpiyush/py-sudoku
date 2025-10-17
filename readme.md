# SUDOKU-PY

> Interactive Python Sudoku game with GUI - Generate, play, and solve Sudoku puzzles!


## What is this?

SUDOKU-PY is a Python-based Sudoku game that includes:
- **Puzzle Generator** - Creates valid Sudoku puzzles with varying difficulty
- **Terminal versions** - Command-line puzzle generation for quick testing


## ✨ Features

### Terminal Versions
- `sudoku.py` - Generates completed Sudoku grids (tabulate format)
- `board.py` - Alternative generator with fancy grid display
- `generate-sudoku.py` - Basic ASCII grid generator

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- `tkinter` (usually comes with Python)
- `tabulate` library (for terminal versions)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/py-sudoku.git
cd py-sudoku
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv sudoku
source sudoku/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the app

**Terminal Versions:**
```bash
python sudoku.py        # Pretty table format
python board.py         # Fancy grid format
python generate-sudoku.py  # ASCII grid format
```

