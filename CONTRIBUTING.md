# Contributing

Contributions are highly welcomed and appreciated. Every little bit of help counts, so do not hesitate! However, before making a pull request, please open an issue first to discuss what you would like to change.

## Development

### Installation

1. Clone the repository
2. Create a virtual environment
  ```
  cd silkie && python -m venv .venv
  ```
3. Activate your virtual environment
  - **Windows:** `.venv\Scripts\activate.bat`
  - **Unix or MacOS**: `source .venv/bin/activate`
4. Install the dependency packages
  ```
  pip install -r requirements.txt
  ```
5. Run Silkie to check if it's working properly
  ```
  python -m silkie -h
  ```

While working on a feature/bug fix, you can set Pytest to watch for changes in the tests/source code and run tests automatically.

1. Specify tests be run automatically upon changes by editing [pytest.ini](pytest.ini) file:

```ini
[pytest]
minversion = 6.0
testpaths = <path_to_tests>
...
```

2. Run this command inside the project/root directory:

```
$ ptw
```

**NOTE:** Please restore/revert/don't commit your changes on `pytest.ini` after development and testing.

### Preparing Pull Requests

1. Fork the repository
2. Clone your fork locally using [git](https://git-scm.com/) and create a branch
3. Follow the instructions in [Installation](#installation) to set up local development environment
4. Install git hook scripts: `pre-commit install` (Before installation, ensure your Flake8 configuration in `tox.ini` has not been modified)
5. Run all tests and make sure your changes don't break anything: `pytest`

After completing all the steps above, you're all set to make a Pull Request 🎉!

## Testing

We use [Pytest](https://docs.pytest.org/en/6.2.x/) as our testing framework. You can run a specific test by entering this command:

```
$ pytest <path_to_test_file>
```

You can find our automation tests in [tests](tests/). Here's how our `tests` directory is organized:

```
tests/
│
├─ unit/ 
│  │
│  ├─ __init__.py
│
├─ integration/ 
│  │
│  ├─ __init__.py
│
├─ data/ 
│
├─ fixture/
```

If you'd like to add new unit/integration tests, please name your test files in the correct format (`test_*.py` or `*_test.py`) for [test discovery](https://docs.pytest.org/en/6.2.x/goodpractices.html#conventions-for-python-test-discovery) and put them in the right directories (`unit` or `integration`).

You can write your test as easy as adding a Python function. Here's an example from [Pytest](https://docs.pytest.org/en/6.2.x/index.html):

```python
# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
```

You can check our code coverage by running this command:

```
$ pytest --cov-report term-missing  --cov=silkie
```
