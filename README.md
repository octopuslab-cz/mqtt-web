# mqtt-web
Web application written in Flask to controll MQTT - receive and messages

use virtual env

```
# create venv (only first time)
python3 -m venv venv


# enable venv (everytime when start working on project)
source ./venv/bin/activate  # on Linux
```

install all dependencies (must have venv enabled)

```
pip install -r requirements.txt
```

`mqtt_paho_test.py` and `mqtt_paho_test2.py` use various config files, please edit script/config to your needs.

run with venv enabled

```
python mqtt_paho_test2.py
```
