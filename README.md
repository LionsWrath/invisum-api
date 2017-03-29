# invisum-api

[![Build Status](https://travis-ci.com/LionsWrath/invisum-api.svg?token=wigrzBbkCwvBZ4hq2ys8&branch=master)](https://travis-ci.com/LionsWrath/invisum-api)

API for the In Visum service.

Try aliasing all anaconda stuff to get easier access:
	
	$ cd ~/anaconda2/bin
	$ for i in *; do alias "ana-$i"="$(pwd -P)/$i"; done

Install depedencies with:
	
	$ pip install -r requirements.txt

To setup the first time:
	
	$ ana-python manage.py makemigrations datasets
	
	$ ana-python manage.py migrate

To run:	
	
	$ ana-python manage.py runserver

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
- datasets/<id>/
    + **Name**: dataset-detail
    + **Permissions**: IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    + **GET**: Information about <id> dataset.
    + **PUT/PATCH**: Update <id> dataset.
    + **DELETE**: Delete the <id> dataset.
- datasets/personal/<id>/
    + **Name**: personal-create
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly 
    + **GET**: List all personal datasets related to <id> and the user.
    + **POST**: Create a new personal dataset related to <id> and the user.
- personal/
    + **Name**: personal-list
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly 
    + **GET**: List all personal datasets related to the user.
- personal/<id>/
    + **Name**: personal-detail
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly
    + **GET**: Information about <id> personal dataset.
    + **PUT/PATCH**: Update <id> personal dataset.
    + **DELETE**: Delete the <id> personal dataset.
- users/
    + **Name**: user-list
    + **GET**: List all users.
- users/<id>/
    + **Name**: user-detail
    + **GET**: Information about <id> user.
- datasets/rate/<id>/
    + **Name**: rating-list
    + **Permissions**: IsAuthenticated
    + **GET**: Retrieve the logged user rating related to <id> dataset.
    + **POST**: Create new rating for <id> dataset(Only one per dataset-user).
- ratings/<id>/
    + **Name**: rating-detail
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly
    + **GET**: Retrieve the <id> rating.
    + **PUT/PATCH**: Update the <id> rating.
    + **DELETE**: Delete the <id> rating.
- search/users/<text>/
    + **Name**: search-users
    + **GET**: Search datasets using <text> by owner username.
- search/title/<text>/
    + **Name**: search-title
    + **GET**: Search datasets using <text> by title.
- discover/
    + **Name**: discover-feed
    + **Permissions**: IsAuthenticated
    + **GET**: List the 10 most ranked datasets.
- personal/operation/<op>/<id>/
    + **Name**: dataset-operation
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Execute a new operation <op> in personal dataset <id>.
- personal/operation/<op>/<l-id>-<r-id>/
    + **Name**: multiset-operation
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Execute a new multiset operation <op> in personals datasets <l-id> and <r-id>.
- personal/plot/<chart>/<id>/
    + **Name**: plot-create
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **POST**: Create a new chart <chart> based on dataset <id>.
- personal/plot/
    + **Name**: plot-list
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: List the plots related to the user.
- personal/<id>/meta/
    + **Name**: personal-meta
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: Get information about the personal dataset <id>.
- personal/plot/<id>/
    + **Name**: plot-serve
    + **Permissions**: IsAuthenticated, IsOwnerOrReadOnly\*
    + **GET**: Serve the plot <id> to the user.
    + **DELETE**: Delete the plot <id>.
- media/<id>/
    + **Name**: media-dataset
    + **GET**: Serve the file related to dataset <id>.
- media/<file>/
    + **Name**: media-filename
    + **GET**: Serve the file based on the name <file>

## Single Dataset Operations

- Slice
    + Simple pythonic slice.
    + **Arguments**: left, right, step
- Drop
    + Drop columns/rows based on labels.
    + **Arguments**: labels, axis
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html)
- Filter
    + Subset of columns/rows based only on labels.
    + **Arguments**: items, like, regex, axis
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.filter.html) 
- Fillna
    + Fill non existent values.
    + **Arguments**: value
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.fillna.html)
- Dropna
    + Drop columns/rows with non existent values.
    + **Arguments**: how
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html)
- Sort
    + Sort values.
    + **Arguments**: by, ascending, axis, na\_position
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html)

## Multi Dataset Operations

- Merge
    + Merge two personal datasets.
    + **Arguments**: how, on, left\_on, right\_on, right\_index, sort, suffixes, copy, indicator
    + [Reference](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html)

## Charts

[Reference](http://bokeh.pydata.org/en/latest/docs/reference/charts.html)

### Base configuration

- plot\_width
- plot\_height
- legend

### Chart Configuration

- Histogram
    + **Arguments**: values, label, agg, bins, density
- Bar
    + **Arguments**: values, label
- Line
    + **Arguments**: x, y
- Scatter
    + **Arguments**: x, y
