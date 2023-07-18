# THIS REPO IS ARCHIVED
## Please visit https://code.usgs.gov/WiM/cbrsservices for the active repo of this project.

CBRS Services Django
====

![USGS](USGS_ID_black.png) ![WIM](wimlogo.png)

# CBRS Web Services v1

This is the web services codebase for version 1 of the Coastal Barrier Resources System Determinations Management System (the web client application codebase can be found [here](https://github.com/USGS-WiM/cbrsdms)). CBRS DMS allows the FWS CBRS team and contractors to enter, query, and manage determinations on whether properties under consideration are in or out of boundaries of federally-designated units, as well as generate reports for completed determinations.

This project was built with Django, Django REST Framework, and Psycopg2.

#### Installation
*Prerequisite*: Please install Python 3 by following [these instructions](https://wiki.python.org/moin/BeginnersGuide/Download).

*Prerequisite*: Please install PostgreSQL by following [these instructions](https://www.postgresql.org/docs/devel/tutorial-install.html).

```bash
git clone https://github.com/USGS-WiM/cbrsservices_django.git
cd cbrsservices_django

# install virtualenv
pip3 install virtualenv

# create a virtual environment
virtualenv env

# activate the virtual environment
source /env/bin/activate

# install the project's dependencies
pip3 install -r requirements.txt

# migrate the database
python3 manage.py migrate

```

## Environments

Note that on Windows, the default arrangement of a settings.py file reading a settings.cfg file (to keep sensitive information out of code repositories) seems to  work fine, but in Linux this does not seem to work, and so all the `CONFIG.get()` calls should be replaced by simple values.

## Development server

Run `python3 manage.py runserver` for a dev server with live reload. Navigate to `http://localhost:8000/cbrsservices/`. The web services will automatically reload if you change any of the source files. This will use the development environment configuration.

Note: If developing on Windows, the python magic library must be manually installed by placing all the *.dll files from this repo's "libmagicwin64" folder into "C:\Windows\System32".

## Production server

In a production environment (or really, any non-development environment) this Django project should be run through a dedicated web server, likely using the Web Server Gateway Interface [(WSGI)](https://wsgi.readthedocs.io/en/latest/). This repository includes sample configuration files (*.conf in the root folder) for running this project in [Apache HTTP Server](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/).

## Authors

* **[Aaron Stephenson](https://github.com/aaronstephenson)**  - *Lead Developer* - [USGS Web Informatics & Mapping](https://wim.usgs.gov/)

See also the list of [contributors](../../graphs/contributors) who participated in this project.

## License

This software is in the Public Domain. See the [LICENSE.md](LICENSE.md) file for details

## Suggested Citation
In the spirit of open source, please cite any re-use of the source code stored in this repository. Below is the suggested citation:

`This project contains code produced by the Web Informatics and Mapping (WIM) team at the United States Geological Survey (USGS). As a work of the United States Government, this project is in the public domain within the United States. https://wim.usgs.gov`


## About WIM
* This project authored by the [USGS WIM team](https://wim.usgs.gov)
* WIM is a team of developers and technologists who build and manage tools, software, web services, and databases to support USGS science and other federal government cooperators.
* WIM is a part of the [Upper Midwest Water Science Center](https://www.usgs.gov/centers/wisconsin-water-science-center).
