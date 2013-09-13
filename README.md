# WholeCellDB v1.1.0

WholeCellDB is a standalone Django project for storing and retrieving data generated by whole-cell models.

## Prerequisites

* python 2.7
* Django 1.5
* python-numpy
* python-h5py


## Quick Start

1. Setup your database in the `DATABASES` dict in `WholeCellDB/settings.py`. For more information on how you can do this, see the [django tutorial](https://docs.djangoproject.com/en/1.5/intro/tutorial01/#database-setup).

2. In the `wcdb/models.py` file, change the value of `HDF5_ROOT` to the location you wish to save the HDF5 data.

        HDF5 = "/path/to/my/hdf5/location"

3. Run `python manage.py syncdb` to create the models. 

4. Run `python manage.py runserver` to start the development server.

## Integrating WholeCellDB with your WholeCell Model
Use the following code to import the WholeCellDB packages into Python:

    import sys

    # Add the project to your path.
    sys.path.append('/path/to/WholeCellDB/project')

    # Setup the environment using the projects settings.
    from WholeCellDB import settings
    from django.core.management import setup_environ
    setup_environ(settings)

    # Import the models
    from wcdb.models import Simulation, Property
