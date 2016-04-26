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

#### Developers

```
pip install -r requirements_dev.txt
```

## How to run

### Environment variables

**DJANGO_SETTINGS_MODULE**: settings module that will be loaded on start
(by default `config.development`, which will be changed in upcoming versions) 

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

#### Developers

Developers might as well use [Livereload](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei?hl=en).

```
python manage.py livereload // livereload server
python manage.py runserver
```
