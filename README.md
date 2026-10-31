# Selenium + Python + pytest (Page Object Model)

A small learning repo that tests the public demo shop <https://www.saucedemo.com>
using Selenium 4, pytest and the Page Object Model (POM).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Needs Python 3.9+ and Chrome (or Firefox). Selenium 4 downloads the matching
driver automatically (Selenium Manager), so there is no chromedriver to install.

## Running tests

```bash
pytest                           # all tests, headless Chrome
pytest --headed                  # watch the browser
pytest --browser firefox
pytest -m smoke                  # only smoke tests
pytest -m api                    # API tests by marker (same as tests/api)
pytest -m "regression or negative"
pytest tests/ui                  # UI tests only
pytest tests/api                 # API tests only
pytest tests/ui/test_login.py    # one file
pytest -k "sort"                 # tests whose name contains "sort"
```

### Environments

Settings per environment live in `envs/<name>.env` (`dev` and `qa`). Pick one
with `TEST_ENV` (default `dev`); real environment variables still override the file.

```bash
TEST_ENV=qa pytest               # Windows PowerShell: $env:TEST_ENV="qa"; pytest
```

Output: an HTML report in `reports/report.html`, and a screenshot in
`screenshots/` for every failed test.

## Structure

```
config.py            loads envs/<TEST_ENV>.env + demo credentials
envs/                dev.env, qa.env: base URLs and timeout per environment
conftest.py          UI fixtures (driver, login_page, inventory_page), CLI options, failure screenshots
pages/
  base_page.py       explicit waits + click/type/get_text helpers
  login_page.py      one class per page: locators + actions
  inventory_page.py
  cart_page.py
  checkout_page.py
api/
  client.py          requests wrapper: base URL + default timeout
  services/          one class per endpoint (PostsService, UsersService): paths + calls, no asserts
tests/
  ui/                Selenium tests only: no locators, no raw Selenium calls
  api/               demo API tests against JSONPlaceholder
    conftest.py      fixtures: api, posts, users (no browser involved)
    posts/  users/   one folder per endpoint
pytest.ini           markers, default options
```

## The POM rules used here

1. **Locators live in page classes**, never in tests.
2. **Page methods describe user actions** (`login()`, `add_to_cart()`), not clicks.
3. **Tests contain the assertions**, page objects don't assert.
4. **Explicit waits only** (`WebDriverWait`), no `time.sleep`, no implicit wait.
5. **Fresh browser per test**, so tests are independent and can run in any order.

## Suggested learning path

1. Read `base_page.py`, then `login_page.py`, then `tests/ui/test_login.py`.
2. Run with `--headed` and watch each test.
3. Break a locator on purpose, run the test, then open the failure screenshot.
4. Exercises:
   - Add a `test_product_names_are_unique` test.
   - Add a product detail page object (click a product name).
   - Add a test for the "Reset App State" menu link.
   - Make the browser configurable via `BROWSER` env var.
   - Run tests in parallel with `pytest-xdist` (`pip install pytest-xdist`, `pytest -n 4`).
   - Add a GitLab CI or GitHub Actions pipeline that runs `pytest -m smoke`.
   - Replace the CSS selectors with XPath for one page and compare readability.
   - Move test data to a JSON/YAML file.
