# 0x03. Unittests and Integration Tests

This project is part of the ALX Backend Python track and focuses on writing proper unit and integration tests to ensure that Python code behaves as expected under different conditions.

## 📌 Purpose

The goal of this project is to learn and demonstrate how to write effective unit tests using Python's `unittest` module, as well as additional tools like `parameterized`. It also introduces integration testing and mocking, which are essential concepts in real-world backend development.

## 📁 Project Structure

- **`utils.py`** - Contains utility functions such as `access_nested_map`, `get_json`, and `memoize`. These functions are used throughout the tests and provide examples of common tasks in backend development.
- **`test_utils.py`** - Contains unit tests for the functions in `utils.py`, using both simple and parameterized testing techniques to cover multiple cases.
- Other test files will be added as you move forward with each task.

## 🧪 Key Concepts Covered

- Writing unit tests with `unittest`
- Using `@parameterized.expand` to run tests with multiple inputs
- Testing for expected exceptions (like `KeyError`)
- Mocking external calls (like `requests.get`)
- Testing memoization and decorators
- Writing docstrings and adhering to `pycodestyle` (PEP 8)

## 🛠️ Installation and Usage

1. Make sure you're using **Python 3.7**.
2. Install dependencies:
   ```bash
   pip install parameterized requests
