from flask import Flask, render_template, url_for, session, send_from_directory
from flask import current_app as app

from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

from .forms import InvForm, ProdForm, ScreenForm, JsonForm

from .modules.importer import Importer as inv_importer
from .modules.prodimporter import Importer as prod_importer
from .modules.screenimporter import Importer as screen

from .modules.branchname import branchname

#bootstrap = Bootstrap(app)


def checkdata(module, arg):
    imp = module(arg)
    check = imp.nodata

    return check


def makeinventory(arg):
    imp = inv_importer(arg)
    if imp.nodata is True:
        table = None
    else:
        table = imp.grouped

    return table


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    element = None
    datacheck = False
    form = InvForm()
    if form.validate_on_submit():
        datacheck = checkdata(inv_importer, form.string.data)
        if not datacheck:
            element = makeinventory(form.string.data)
        form.string.data = ''
    return render_template('inventory.html',
                           form=form,
                           element=element,
                           datacheck=datacheck,
                           )


@app.route('/productionlines', methods=['GET', 'POST'])
def productionlines():
    element = None
    datacheck = False
    form = ProdForm()
    if form.validate_on_submit():
        datacheck = checkdata(prod_importer, form.string.data)
        if not datacheck:
            element = prod_importer(form.string.data)
        form.string.data = ''
    return render_template('production.html',
                           form=form,
                           element=element,
                           datacheck=datacheck,
                           )


def profitredirect(arg):
    return url_for('shippingprofits', arg=arg)


@app.route('/', methods=['GET', 'POST'])
@app.route('/marketinfos', methods=['GET', 'POST'])
def marketinfos():
    element = None
    datacheck = False
    form = ScreenForm()
    jsonstring = JsonForm()
    # Remove Submit btn from JsonForm
    jsonstring.submit = "hello"
    link = ""
    json_filepath = ""

    if form.validate_on_submit():
        datacheck = checkdata(screen, form.string.data)
        if not datacheck:
            element = screen(form.string.data)
            jsonstring.string.data = element.json

            h = str(hash(element.json))
            json_filepath = 'files/'+h+'.json'
            with open(json_filepath, 'w') as f:
                f.write(str(element.json))
        form.string.data = ''

        messages = json_filepath
        session['messages'] = messages

        link = profitredirect(messages)

    return render_template('marketinfos.html',
                           form=form,
                           element=element,
                           jsonstring=jsonstring,
                           json_filepath=json_filepath,
                           datacheck=datacheck,
                           link=link,
                           )


@app.route('/shippingprofits', methods=['GET', 'POST'])
def shippingprofits():
    messages = session["messages"]
    link = profitredirect(messages)
    return render_template('shippingprofits.html', link=link)


@app.route('/files/<path:path>')
def send_file(path):
    return send_from_directory('files', path, as_attachment=True)


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
        datacheck = checkdata(screen, form.string.data)
        if not datacheck:
            element = screen(form.string.data)
            jsonstring.string.data = element.json
        form.string.data = ''
    return render_template('test.html',
                           form=form,
                           element=element,
                           jsonstring=jsonstring,
                           datacheck=datacheck,
                           )


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

#TODO make clickable link as navbar name
#namestring = '<a href="'+url_for("marketinfos")+'"PrUn Data Importer '+branchname()+'</a>'

namestring = "PrUn Data Importer "+branchname()

@nav.navigation()
def impnavbar():
    return Navbar(
        namestring,
        View('Market Infos Screen', 'marketinfos'),
        View('Shipping Profits', 'shippingprofits'),
        View('Inventory Importer', 'inventory'),
        View('Production Lines', 'productionlines'),
        Subgroup('Turorials',
                 View('Inventory & Prod. Lines Importers',
                      'tutorial_importers'),
                 View('Market Infos Screen', 'tutorial_market'))
    )


nav.init_app(app)