# CodeFlow Engine - Coverage Guide

This guide explains how to measure, improve, and maintain test coverage for CodeFlow Engine.

---

## Table of Contents

- [Coverage Goals](#coverage-goals)
- [Measuring Coverage](#measuring-coverage)
- [Coverage Reports](#coverage-reports)
- [Quality Gates](#quality-gates)
- [Improving Coverage](#improving-coverage)
- [Codecov Integration](#codecov-integration)

---

## Coverage Goals

### Overall Targets

| Component | Target | Current | Status |
|-----------|--------|---------|--------|
| **Core Engine** | >90% | ~30% | 🔴 Needs improvement |
| **Actions** | >80% | ~30% | 🔴 Needs improvement |
| **Integrations** | >80% | ~30% | 🔴 Needs improvement |
| **API Endpoints** | >85% | ~30% | 🔴 Needs improvement |
| **Workflows** | >75% | ~30% | 🔴 Needs improvement |
| **Configuration** | >70% | ~30% | 🔴 Needs improvement |
| **Overall** | >80% | ~30% | 🔴 Needs improvement |

### Quality Gates

- **Minimum**: 70% overall coverage
- **Target**: 80% overall coverage
- **Patch Coverage**: 70% for new/changed code
- **Project Coverage**: 80% for entire project

---

## Measuring Coverage

### Local Measurement

```bash
# Run tests with coverage
poetry run pytest --cov=codeflow_engine --cov-report=term --cov-report=html

# View terminal report
# Coverage percentage shown in terminal

# View HTML report
open htmlcov/index.html
```

### Using Coverage Scripts

**Bash:**
```bash
./tools/coverage/check-coverage.sh [threshold]
# Default threshold: 70%
```

**PowerShell:**
```powershell
.\tools\coverage\check-coverage.ps1 -CoverageThreshold 70
```

### Coverage by Module

```bash
# Show coverage by module
poetry run coverage report --show-missing

# Show only uncovered lines
poetry run coverage report --show-missing | grep -E "codeflow_engine.*[0-9]+.*[0-9]+.*[0-9]+%"
```

---

## Coverage Reports

### Terminal Report

```bash
poetry run pytest --cov=codeflow_engine --cov-report=term
```

**Output:**
```
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
codeflow_engine/__init__.py                5      0   100%
codeflow_engine/engine.py                 150     45    70%
codeflow_engine/actions/__init__.py        10      2    80%
-----------------------------------------------------------
TOTAL                                    4929   3405    31%
```

### HTML Report

```bash
poetry run pytest --cov=codeflow_engine --cov-report=html
open htmlcov/index.html
```

The HTML report provides:
- File-by-file coverage
- Line-by-line highlighting
- Missing lines identification
- Branch coverage

### XML Report (for CI/CD)

```bash
poetry run pytest --cov=codeflow_engine --cov-report=xml
```

Generates `coverage.xml` for CI/CD integration.

---

## Quality Gates

### CI/CD Enforcement

Coverage is checked in CI/CD:

1. **Tests run with coverage**
2. **Coverage uploaded to Codecov**
3. **Threshold check** (70% minimum)
4. **PR status** updated based on coverage

### Coverage Thresholds

**Project Coverage:**
- Target: 80%
- Threshold: 1% (allows 1% drop before failing)

**Patch Coverage (PR changes):**
- Target: 70%
- Threshold: 1%

### Failing Quality Gates

If coverage drops below threshold:

1. **CI/CD will warn** (not fail by default)
2. **Codecov will comment** on PR
3. **Review required** before merge
4. **Add tests** to increase coverage

---

## Improving Coverage

### Identifying Gaps

1. **Run coverage report:**
   ```bash
   poetry run pytest --cov=codeflow_engine --cov-report=html
   open htmlcov/index.html
   ```

2. **Find uncovered files:**
   - Red lines = not covered
   - Green lines = covered
   - Yellow lines = partial coverage

3. **Prioritize:**
   - Critical paths first
   - High-risk code
   - Frequently used functions

### Adding Tests

**Example: Uncovered Function**

```python
# codeflow_engine/utils/helpers.py
def process_data(data: dict) -> dict:
    """Process input data."""
    if not data:
        return {}
    return {"processed": data}
```

**Add Test:**

```python
# tests/unit/test_helpers.py
def test_process_data_with_valid_data():
    """Test processing valid data."""
    result = process_data({"key": "value"})
    assert result == {"processed": {"key": "value"}}

def test_process_data_with_empty_data():
    """Test processing empty data."""
    result = process_data({})
    assert result == {}

def test_process_data_with_none():
    """Test processing None."""
    result = process_data(None)
    assert result == {}
```

### Coverage Best Practices

1. **Test edge cases**
2. **Test error conditions**
3. **Test boundary values**
4. **Test both success and failure paths**
5. **Use fixtures for common setup**
6. **Mock external dependencies**

---

## Codecov Integration

### Setup

Codecov is already configured and integrated:

1. **Codecov App**: Installed on GitHub
2. **CODECOV_TOKEN**: Set in repository secrets
3. **codecov.yml**: Configuration file in repo root

### Features

- **Automatic PR comments** with coverage changes
- **Coverage badges** in README
- **Historical tracking** of coverage trends
- **Branch coverage** tracking
- **File-by-file** coverage reports

### Viewing Coverage

1. **Codecov Dashboard**: https://codecov.io/gh/JustAGhosT/codeflow-engine
2. **PR Comments**: Automatic comments on PRs
3. **GitHub Checks**: Coverage status in PR checks

### Configuration

See `codecov.yml` for:
- Coverage targets
- Ignore patterns
- Status checks
- Comment settings

---

## Coverage Exclusions

### Files Excluded from Coverage

The following are excluded (see `pyproject.toml`):

- `*/tests/*` - Test files
- `*/migrations/*` - Database migrations
- `*/venv/*` - Virtual environments
- `*/__pycache__/*` - Python cache
- `setup.py` - Setup script
- `conftest.py` - Pytest configuration

### Lines Excluded from Coverage

The following lines are excluded:

- `pragma: no cover` - Explicitly marked
- `def __repr__` - String representations
- `raise AssertionError` - Assertions
- `raise NotImplementedError` - Not implemented
- `if __name__ == .__main__.:` - Main blocks
- `@abstractmethod` - Abstract methods

---

## Continuous Improvement

### Tracking Progress

1. **Baseline**: Current coverage ~30%
2. **Target**: 80% overall coverage
3. **Milestones**:
   - 50% coverage (Phase 1)
   - 70% coverage (Phase 2)
   - 80% coverage (Phase 3)
   - 90%+ for critical components (Phase 4)

### Coverage Goals by Phase

**Phase 1 (Current):**
- Measure baseline coverage
- Identify critical gaps
- Add tests for core engine

**Phase 2 (Next):**
- Increase to 50% overall
- Focus on actions
- Add integration tests

**Phase 3 (Future):**
- Increase to 70% overall
- Focus on integrations
- Add E2E tests

**Phase 4 (Future):**
- Increase to 80% overall
- 90%+ for critical components
- Maintain coverage

---

## Troubleshooting

### Coverage Not Uploading

1. **Check CODECOV_TOKEN**: Ensure secret is set
2. **Check CI logs**: Look for upload errors
3. **Check codecov.yml**: Verify configuration

### Coverage Lower Than Expected

1. **Check exclusions**: Verify files aren't excluded
2. **Check test execution**: Ensure tests are running
3. **Check paths**: Verify source paths are correct

### Quality Gate Failing

1. **Check threshold**: Verify threshold is reasonable
2. **Add tests**: Increase coverage for uncovered code
3. **Review exclusions**: Ensure appropriate files excluded

---

## Additional Resources

- [Codecov Documentation](https://docs.codecov.com/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Strategy](./TESTING_STRATEGY.md)
- [CI/CD Workflows](../../.github/workflows/ci.yml)

---

## Support

For coverage questions:
- GitHub Issues: [codeflow-engine/issues](https://github.com/JustAGhosT/codeflow-engine/issues)
- Codecov Dashboard: https://codecov.io/gh/JustAGhosT/codeflow-engine

