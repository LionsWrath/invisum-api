# invisum-api

[![Build Status](https://travis-ci.com/LionsWrath/invisum-api.svg?token=wigrzBbkCwvBZ4hq2ys8&branch=master)](https://travis-ci.com/LionsWrath/invisum-api)

API for the In Visum service.

Try aliasing all anaconda stuff to get easier access:
	
	$ cd ~/anaconda2/bin
	$ for i in *; do alias ana-xz=/home/certorio/Desktop/project/invisum-api/xz; done;

Install depedencies with:
	
	$ pip install -r requirements.txt

To setup the first time:
	
	$ ana-python manage.py makemigrations datasets
	
	$ ana-python manage.py migrate

To run:	
	
	$ ana-python manage.py runserver
