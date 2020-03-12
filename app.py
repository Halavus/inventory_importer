from flask import Flask, render_template
from flask import Response
from flask import stream_with_context, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from modules.importer import Importer as inv_importer
from modules.prodimporter import Importer as prod_importer
from modules.screenimporter import Importer as screen
from secret_key import secret_key as secret_key

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key

bootstrap = Bootstrap(app)


class InvForm(FlaskForm):
    string = TextAreaField(
        'Paste the html "InventoryView__grid" element and submit',
        render_kw={"placeholder":
            'HTML code: <div class="InventoryView__grid___1y8GFWz"> ...'},
        validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProdForm(FlaskForm):
    string = TextAreaField(
        'Paste the html "SiteProductionLines__column___" element and submit',
        render_kw={"placeholder":
            'HTML code:  <div class="SiteProductionLines__column___ij4g8Kg '
            'SiteProductionLines__columnBase___3eLJ7nE" ...'},
        validators=[DataRequired()])
    submit = SubmitField('Submit')

class ScreenForm(FlaskForm):
    string = TextAreaField(
        'Paste your market infos screen',
        render_kw={"placeholder":
            'SCRN: XXX YYY\n'
            'SCRNS\n'
            'ADD\n'
            'FULL\n'
            'LIC: XYZ\n'
            '...',
            'style': 'height: 152px'},
        validators=[DataRequired()])
    submit = SubmitField('Submit')

def makeinventory(arg):
    imp=inv_importer(arg)
    if imp.nodata==True:
        table = None
    else:
        table=imp.grouped

    return table

def checkdata(module, arg):
    imp=module(arg)
    check=imp.nodata

    return check

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

nav = Nav()

@nav.navigation()
def impnavbar():
    return Navbar(
            'PrUn Data Importer',
            View('Market Infos Screen', 'marketinfos'),
            View('Inventory Importer', 'inventory'),
            View('Production Lines', 'productionlines'),
            Subgroup('Turorials',
                View('Inventory & Prod. Lines Importers', 'tutorial_importers'),
                View('Market Infos Screen', 'tutorial_market'))
            )

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    element = None
    datacheck = False
    form = InvForm()
    if form.validate_on_submit():
        datacheck=checkdata(inv_importer, form.string.data)
        if not datacheck:
            element = makeinventory(form.string.data)
        form.string.data = ''
    return render_template('inventory.html',
            form=form,
            element=element,
            datacheck=datacheck)

@app.route('/productionlines', methods=['GET', 'POST'])
def productionlines():
    element = None
    datacheck = False
    form = ProdForm()
    if form.validate_on_submit():
        datacheck=checkdata(prod_importer, form.string.data)
        if not datacheck:
            element=prod_importer(form.string.data)
        form.string.data = ''
    return render_template('production.html',
            form=form,
            element=element,
            datacheck=datacheck)

class JsonForm(FlaskForm):
    string = TextAreaField('', render_kw={
        'id': 'jsonstring', 
        'style': 'height: 100px'})

@app.route('/', methods=['GET', 'POST'])
@app.route('/marketinfos', methods=['GET', 'POST'])
def marketinfos():
    element = None
    datacheck = False
    form = ScreenForm()
    jsonstring = JsonForm()
    if form.validate_on_submit():
        datacheck=checkdata(screen, form.string.data)
        if not datacheck:
            element=screen(form.string.data)
            jsonstring.string.data = element.json
        form.string.data = ''
    return render_template('marketinfos.html',
            form=form,
            element=element,
            jsonstring=jsonstring,
            datacheck=datacheck)

@app.route('/tutorial_importers')
def tutorial_importers():
    return render_template('tutorial_importers.html')

@app.route('/tutorial_market')
def tutorial_market():
    return render_template('tutorial_market.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    element = None
    datacheck = False
    form = ScreenForm()
    jsonstring = JsonForm()
    if form.validate_on_submit():
        datacheck=checkdata(screen, form.string.data)
        if not datacheck:
            element=screen(form.string.data)
            jsonstring.string.data = element.json
        form.string.data = ''
    return render_template('test.html',
            form=form,
            element=element,
            jsonstring=jsonstring,
            datacheck=datacheck)


nav.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
