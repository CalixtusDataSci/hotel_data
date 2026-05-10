# Contributing to Hotel Data Project

## Overview
This project welcomes contributions from data scientists, engineers, and domain experts. We maintain high standards for code quality, documentation, and legal compliance.

## Code of Conduct
- Respect intellectual property rights
- Maintain confidentiality of sensitive data
- Follow all applicable data protection regulations (GDPR, CCPA, etc.)
- Provide clear attribution and licensing information

## Legal & Licensing Requirements
- All contributions must be compatible with the MIT License
- Include copyright attribution in submitted code
- Disclose any proprietary algorithms or methods
- Ensure compliance with data usage rights

## Development Setup

```bash
# Clone repository
git clone https://github.com/CalixtusDataSci/hotel_data.git
cd hotel_data

# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate      # macOS/Linux

# Install dependencies with dev extras
pip install -e ".[dev]"
```

## Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, well-documented code
- Follow PEP 8 style guide
- Add type hints where applicable
- Update docstrings

### 3. Testing
```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Code quality checks
flake8 scripts/
pylint scripts/
black scripts/ --check
mypy scripts/
```

### 4. Format Code
```bash
black scripts/
isort scripts/
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: Add descriptive commit message"
```

Follow conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### 6. Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Code Standards

### Style Guide
- **Language**: Python 3.9+
- **Formatter**: Black
- **Linter**: Flake8 + Pylint
- **Type Checking**: MyPy
- **Imports**: Organized with isort

### Documentation Requirements
- Module-level docstrings (description, author, license)
- Function/class docstrings with parameters and returns
- Inline comments for complex logic
- Type hints for all parameters and returns

Example:
```python
def clean_hotel_data(data: pd.DataFrame, validation: bool = True) -> pd.DataFrame:
    """
    Clean and validate hotel booking data.
    
    Parameters
    ----------
    data : pd.DataFrame
        Raw hotel data with columns: hotel_id, check_in_date, room_rate, num_guests
    validation : bool, default=True
        Whether to perform data validation checks
    
    Returns
    -------
    pd.DataFrame
        Cleaned and validated hotel data
        
    License
    -------
    MIT License - See LICENSE file for terms
    
    Notes
    -----
    - Removes rows with zero guests
    - Coerces numeric fields to float
    - Parses dates to datetime format
    """
```

## Testing Requirements
- Minimum 80% code coverage
- Unit tests for all public functions
- Integration tests for workflows
- Test data should be representative and sanitized

## Security & Data Protection
- Never commit sensitive data, API keys, or credentials
- Use `.env` files for configuration (not tracked in git)
- Sanitize any example data in notebooks
- Document data source and licensing

## Documentation Standards
- Update README.md for major changes
- Add docstrings to all functions
- Include usage examples
- Document breaking changes clearly

## Performance Considerations
- Profile code for bottlenecks
- Optimize for production datasets (millions of rows)
- Document expected runtime performance
- Consider memory efficiency

## Release Process
1. Update version in `setup.py`
2. Update `CHANGELOG.md` with changes
3. Tag release: `git tag v1.0.0`
4. GitHub Actions automatically tests and builds

## Questions or Issues?
- Create GitHub Issue for bugs
- Discussion section for feature suggestions
- Email: calixtusnwaeke@gmail.com for legal/licensing questions

---

**Thank you for contributing to professional data science!**
