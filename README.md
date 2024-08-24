# Python playground

This project is a small playground for me to experiment and better understand some behaviors of Python.

## Getting started

```bash
# (Only once) Create the virtual environment (and use python 3.11 min)
python3.11 -m venv .venv

# Activate virtual env
source .venv/bin/activate

# (Only once) Install requirements
python3 -m pip install -r requirements.txt

# (Only once) Setup project to be able to import utils
python3 setup.py

# Launch scripts
python3 /path/to/file.py
```

_Note to my future self:_
As of now, all experiments work with the same version of all dependencies.
In the future, I might have some experiments requiring different versions.
If that comes up, I will need multiple virtual environments.

