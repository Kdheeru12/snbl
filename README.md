## Installing the Deps & Running the application (Tested using Python 3.1.0)

```
python -m venv snbl-venv

source snbl-venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

python manage.py test
```

* plan/ -> crud operations on plan
* promotion/ -> crud operations on promotion
* goals/ -> to get CustomerGoals along with the max benifit