cp -r "static/trustly/libs/nltk_data" "$HOME/nltk_data"
sudo apt-get install python3-setuptools
python3 -m venv venv
source env/bin/activate
pip install -r requirements.txt
python3 manage-dev.py runserver --noreload
