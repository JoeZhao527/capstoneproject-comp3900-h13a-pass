# Pytest usage

## 1. Install and get start
Make sure pytest is installed on your local device, run one of the following commands
```
pytest --version
```

```
python3 -m pytest --version
```

If pytest not found, install it with one of the following commands
```
pip install -U pytest
```

```
pip3 install -U pytest
```

Run all pytest with command in root directory or test directory:
```
pytest 
```
```
python3 -m pytest
```

## 2. Notes on writing pytest
Each test function name must be start with `test_`. For example:
```Python
def test_diner_login():
  clear_db()
  email = "1@gmail.com"
  password = "12345678"
  res = diner_login(email, password)
  assert res['diner_id'] == 1
```

For more information of writing tests, please refer 
to *test_auth.py* and *test_vouchers.py* in /backend/test,
or read the pytest documentation here
[pytest documentation](https://docs.pytest.org/en/6.2.x/getting-started.html)
