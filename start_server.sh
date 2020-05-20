export FLASK_DEBUG=1
export FLASK_APP="run.py"
export APP_SETTINGS="development"
export SECRET="openthesea"
export DATABASE_URL='sqlite:///app.db'
python -m flask run