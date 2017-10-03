python3.6 -m venv env
source ./env/bin/activate
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt
