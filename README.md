# Simple

## Requeriments

- Python 2.7.5
- Ruby

## Installation

### Source code
 
```
git clone https://github.com/zurfyx/simple
```

### Install dependencies

```
pip install -r requirements.txt
gem install sass
```

## How to run

### Environment variables

_coming soon_

### Create superuser(s)

```
cd simple/;
python manage.py createsuperuser;
```

### Start the website

By default it will start in development mode 
(will be changed in upcoming versions):

```
cd simple/;
python manage.py migrate;
python manage.py runserver;
```

Check it out at [127.0.0.1:8000](http://127.0.0.1:8000).
