# invisum-api

[![Build Status](https://travis-ci.com/LionsWrath/invisum-api.svg?token=wigrzBbkCwvBZ4hq2ys8&branch=master)](https://travis-ci.com/LionsWrath/invisum-api)

API for the In Visum service demo.

## Install

We are using the [Continuum Analytics](https://www.continuum.io/) **Anaconda** platform for the necessary data science tools. You can try aliasing all anaconda stuff to get easier access:
	
	$ cd ~/anaconda2/bin
	$ for i in *; do alias "ana-$i"="$(pwd -P)/$i"; done

Install depedencies with:
	
	$ pip install -r requirements.txt

To setup the first time:
	
	$ ana-python manage.py makemigrations datasets
	$ ana-python manage.py migrate

To run:	
	
	$ ana-python manage.py runserver

## Configuration

Please set a **SECRET\_KEY** in your environment variables before executing. If you need to generate a new key, you can use online tools like [this](http://www.miniwebtool.com/django-secret-key-generator/).

***

## API Documentation

### Permissions

- **AllowAny**: Unrestricted access - default
- **IsAuthenticatedOrReadOnly**: Need to be authenticated for non safe methods.
- **IsAuthenticated**: Need to be authenticated for any method.
- **IsOwnerOrReadOnly**: Only owners of a object can edit.

### Requests

- datasets/
    + **Name**: dataset-list
    + **Permissions**: IsAuthenticatedOrReadOnly
    + **GET**: List all datasets.
    + **POST**: Create new dataset.
- datasets/\<id>/
    + **Name**: dataset-detail
    + **Permissions**: IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    + **GET**: Information about \<id> dataset.
    + **PUT/PATCH**: Update \<id> dataset.
    + **DELETE**: Delete the \<id> dataset.
- datasets/personal/\<id>/
    + **Name**: personal-create
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly 
    + **GET**: List all personal datasets related to \<id> and the user.
    + **POST**: Create a new personal dataset related to \<id> and the user.
- personal/
    + **Name**: personal-list
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly 
    + **GET**: List all personal datasets related to the user.
- personal/\<id>/
    + **Name**: personal-detail
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly
    + **GET**: Information about \<id> personal dataset.
    + **PUT/PATCH**: Update \<id> personal dataset.
    + **DELETE**: Delete the \<id> personal dataset.
- users/
    + **Name**: user-list
    + **GET**: List all users.
- users/\<id>/
    + **Name**: user-detail
    + **GET**: Information about \<id> user.
- datasets/rate/\<id>/
    + **Name**: rating-list
    + **Permissions**: IsAuthenticated
    + **GET**: Retrieve the logged user rating related to \<id> dataset.
    + **POST**: Create new rating for \<id> dataset(Only one per dataset-user).
- ratings/\<id>/
    + **Name**: rating-detail
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly
    + **GET**: Retrieve the \<id> rating.
    + **PUT/PATCH**: Update the \<id> rating.
    + **DELETE**: Delete the \<id> rating.
- search/users/\<text>/
    + **Name**: search-users
    + **GET**: Search datasets using \<text> by owner username.
- search/title/\<text>/
    + **Name**: search-title
    + **GET**: Search datasets using \<text> by title.
- discover/
    + **Name**: discover-feed
    + **Permissions**: IsAuthenticated
    + **GET**: List the 10 most ranked datasets.
- personal/operation/\<op>/\<id>/
    + **Name**: dataset-operation
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Execute a new operation \<op> in personal dataset \<id>.
- personal/operation/\<op>/\<l-id>-\<r-id>/
    + **Name**: multiset-operation
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Execute a new multiset operation \<op> in personals datasets \<l-id> and \<r-id>.
- personal/plot/\<chart>/\<id>/
    + **Name**: plot-create
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Create a new chart \<chart> based on dataset \<id>.
- personal/plot/
    + **Name**: plot-list
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: List the plots related to the user.
- personal/\<id>/meta/
    + **Name**: personal-meta
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: Get information about the personal dataset \<id>.
- personal/plot/\<id>/
    + **Name**: plot-serve
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: Serve the plot \<id> to the user.
    + **DELETE**: Delete the plot \<id>.

## Single Dataset Operations

1. Slice
    + Simple pythonic slice.
    + **Arguments**: left, right, step
2. Drop
    + Drop columns/rows based on labels.
    + **Arguments**: labels, axis
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html)
3. Filter
    + Subset of columns/rows based only on labels.
    + **Arguments**: items, like, regex, axis
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.filter.html) 
4. Fillna
    + Fill non existent values.
    + **Arguments**: value
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.fillna.html)
5. Dropna
    + Drop columns/rows with non existent values.
    + **Arguments**: how
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html)
6. Sort
    + Sort values.
    + **Arguments**: by, ascending, axis, na\_position
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html)

## Multi Dataset Operations

1. Merge
    + Merge two personal datasets.
    + **Arguments**: how, on, left\_on, right\_on, right\_index, sort, suffixes, copy, indicator
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html)
2. Closest Match Merge *(Testing)*
    + Merge two personal datasets based on the closest match.
    + **Arguments**: left\_pivot, right\_pivot, how, on, left\_on, right\_on, right\_index, sort, suffixes, copy, indicator
    + [Merge Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html)
    + [Closest Match Reference](https://docs.python.org/2/library/difflib.html#difflib.get_close_matches)

## Charts

[Reference](http://bokeh.pydata.org/en/latest/docs/reference/charts.html)

### Base configuration

- plot\_width
- plot\_height
- legend

### Chart Configuration

1. Histogram
    + **Arguments**: values, label, agg, bins, density
2. Bar
    + **Arguments**: values, label
3. Line
    + **Arguments**: x, y
4. Scatter
    + **Arguments**: x, y
