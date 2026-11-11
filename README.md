# README


## Installation
```
python3 -m venv whereisthesun
source whereisthesun/bin/activate
pip install requests
pip install geonamescache
pip install astral
pip install geopy
pip install flask
```

Install dependancies
```bash
py -3.15 -m pip install requests
py -3.15 -m pip install geonamescache
py -3.15 -m pip install astral
py -3.15 -m pip install geopy
py -3.15 -m pip install flask
```

## Run
```
py -3.15 -m flask run --host="0.0.0.0" --port=5001
```



source whereisthesun/bin/activate
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5001 app:app



ExecStart=/bin/bash -c 'source /root/python_environments/whereisthesun/bin/activate && cd /root/webapps/whereisthesun && gunicorn -w 4 -b 127.0.0.1:5001 app:app'



