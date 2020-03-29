# inventory_importer

Requirements
- Python 3
- Git repo

Installation (linux)

1. Create a virtualenv in the base dir `python3 -m venv venv`
2. Activate virtualenv `source venv/bin/activate`
3. Install python dependencies `pip install -r requirements.txt`
4. Edit `.env_to_edit` 
 1. Add a secret key 
 2. Change the server name if required
 3. Comment/uncomment `FLASK_ENV` for the desired environment
 4. Rename or copy the file from `.env_to_edit` to `.env`
5. Run `git init` if not already done.

App startup
- Activate virtualenv (see above) and run `python wsgi.py`

or
- `./path/to/venv/bin/gunicorn -b 0.0.0.0:5000 wsgi:app`

Online version of the website 
http://prun.halavus.com
