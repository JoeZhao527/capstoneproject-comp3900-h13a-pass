# capstoneproject-comp3900-h13a-pass

## dependencies
- Flask 2.0.1
- Python 3.8.2

Note that any other python3 version should work, and lower version of Flask could work as well

## run the server on localhost
#### install flask
```
pip3 install flask
```
if the above not working, try:
```
pip3 install flask --user
```

### run
1. go to the root directory
2. set FLASK_APP variable, run this on mac terminal
```
export FLASK_APP=run.py
```
3. run:
```
flask run
```
or 
```
python3 -m flask run
```
or if address 5000 is being used, use the other ports
eg:
```
flask run -p 5001
```

