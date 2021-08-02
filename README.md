# capstoneproject-comp3900-h13a-pass

## requirements
- Flask 2.0.1
- Python 3.8.2
- Flask_SQLAlchemy 2.5.1
- SQLAlchemy 1.4.19
- pytest 6.2.4
- Flask 2.0.1
- Werkzeug 2.0.1
- PyJWT 2.1.0

Note that any other python3 version should work, and lower version of Flask could work as well

## run the server on localhost
#### install requirements
```
pip3 install -r requirements.txt
```

### run
1. go to the root directory
2. load some data to database:
```
python3 load_data.py
```
3. set FLASK_APP variable, run this on mac/Linux terminal
```
export FLASK_APP=run.py
```
4. run:
```
flask run
```
if port 5000 is being used, use the other ports
eg:
```
flask run -p 5001
```
or set flask run port variable by
```
export FLASK_RUN_PORT=5001
```

