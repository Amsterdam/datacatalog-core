.. highlight:: bash

Core of the Data Catalog Project
================================

A microservice with API to store, manage and search through meta data of data
sets.

The latest documentation can always be found `here <https://amsterdam.github.io/dcatd/>`_.


API
---

The API spec can be found at /openapi on a running instance with default settings. The API of the current running instance at Amsterdam can be browsed using Swagger UI `here <https://api.data.amsterdam.nl/api/swagger/?url=/dcatd/openapi>`_.


How to run locally
------------------

Requires Python 3.6.1 or above

Default configuration uses a PostgreSQL database which can be spun up in a container:
Requires Docker and a free port 5433 (this is deliberately another port than PG's default one,
to preempt a collision)

This means you can also change the port to 5432 (and other connection parameters)
in `/examples/running/config.yml` and use a locally running instance of PostgreSQL

Create a virtual environment and install all the dependencies:

::

    make alldeps


Example server
##############

::

    docker-compose up -d database
    make example


Running tests
#############

::

    docker-compose up -d database
    make test

or

::

    docker-compose up -d database
    make cov

Update documentation
--------------------

Requires Sphinx plus extras:

::

    pip install -e .[docs]


Run the following command to push latest version to github:

::

    make -C sphinx gh-pages
