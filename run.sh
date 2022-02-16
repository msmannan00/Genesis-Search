pip install -r requirements.txt
python3 manage.py runserver --noreload
virtualenv env
. env/bin/activate
sudo chown -R www-data:www-data db.sqlite3
pause