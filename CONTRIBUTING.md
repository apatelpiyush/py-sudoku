## CONTRIBUTING

### 1. Find an Issue

- Browse [open issues](../../issues)
- Check the `ISSUES.md` file for suggested tasks with bounty points
- Look for `good-first-issue` label if you're new

### 2. Claim an Issue

1. Comment on the issue: **"I would like to work on this"**
2. Wait for maintainer approval (we'll assign you)
3. Start working only after assignment
4. If no response within 24 hours, ping maintainers

### 3. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/py-sudoku.git
cd py-sudoku
```

### 4. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv sudoku
source sudoku/bin/activate  # On Windows: sudoku\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If working on tests, install dev dependencies
pip install -r requirements-dev.txt  # (if exists)
```

### 5. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - for new features
- `fix/` - for bug fixes
- `refactor/` - for code refactoring
- `docs/` - for documentation updates
- `test/` - for adding tests
