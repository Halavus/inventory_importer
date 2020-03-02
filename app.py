from flask import Flask, render_template
from flask import Response
from flask import stream_with_context, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from modules.importer import Importer as inventory
from modules.prodimporter import Importer as production
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

def makeinventory(arg):
    imp=inventory(arg)
    table=imp.grouped

    return table

def checkdata(module, arg):
    imp=module(arg)
    check=imp.nodata

    return check 

def makeproduction(arg):
    p=production(arg)

    return p

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    element = None
    datacheck = False
    form = InvForm()
    if form.validate_on_submit():
        datacheck=checkdata(inventory, form.string.data)
        element = makeinventory(form.string.data)
        form.string.data = ''
    return render_template('index.html', form=form, element=element, datacheck=datacheck)

@app.route('/production_lines', methods=['GET', 'POST'])
def production_lines():
    element = None
    datacheck = False
    form = ProdForm()
    if form.validate_on_submit():
        datacheck=checkdata(production, form.string.data)
        element=production(form.string.data)
        form.string.data = ''
    return render_template('production.html', form=form, element=element, datacheck=datacheck)

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
