# TOMIS-nptadwords

A django-rest test project for TOMIS

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Developed on Windows 7 but should work with any OS.  

```
Python 3.5
django 2.0.7
djangorestframework 3.8.2
django-filter 1.1.0
django-rest-auth 0.9.6
django-rest-swagger 2.2.0
django-chartit 0.2.9
postressql 10.4
gunicorn 19.8.1
nginx 1.10.3
fabric 2.0
pipenv 8.3.2
```

### Installing

A step by step series of examples that tell you how to get a development env running

Clone repo to your local system

```
git clone https://github.com/mrnitrate/TOMIS_nptadwords.git
```

Setup pipenv virtual enviroment and install required python packages

```
cd django-TOMIS-nptadwords
pipenv install --dev
```

From the TOMIS_nptadwords folder run the development server

```
cd TOMIS_nptadwords
pipenv run python manage.py runserver
```

## Running the tests

To run the unit test use django's builtin test

```
pipenv run python manage.py test
```

## Deployment

Clone to webserver, setup nginx or apache to serve.   

## Built With

* [Django](https://docs.djangoproject.com/en/2.0/) - The web framework used
* [Django Rest Framework ](http://www.django-rest-framework.org/) - Rest framework for django
* [django-filter](https://django-filter.readthedocs.io/en/1.1.0/) - Used to filter down a queryset based on a model's fields.
* [django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/) - A set of REST API endpoints to handle User Registration and Authentication Tasks.
* [django-rest-swagger](https://django-rest-swagger.readthedocs.io/en/latest/) - Swagger/OpenAPI Documentation Generator for Django REST Framework
* [Django-Chartit 2](http://django-chartit2.readthedocs.io/en/latest/) - Used to create the Highcharts on the index page.
* [Fabric](http://docs.fabfile.org/en/2.1/) - Used for devops deployments to production webserver.
* [Pipenv](https://docs.pipenv.org/) - Used for python package management and virtualenv.

## Author

* **Aemil Estvold** - [MrNitrate](https://github.com/mrnitrate)

