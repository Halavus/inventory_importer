# inventory_importer

Requirements
- Python 3
- Git repo

Installation (linux)

1. Create a virtualenv in the base dir `pyhon3 -m venv venv`
2. Activate virtualenv `source venv/bin/activate`
3. Install python dependencies `pip install -r requirements.txt`
4. Edit `.env_to_edit` with your secret key and server name. Rename or copy this file to `.env`
5. Run `git init` if not already done.
6. Webapp startup with `py wsgi.py`
