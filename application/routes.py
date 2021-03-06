from flask import render_template, url_for, session, send_from_directory, request
from flask import current_app as app

from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup

from .forms import InvForm, ProdForm, ScreenForm, JsonForm

from .modules.invimporter import Importer as invimporter
from .modules.prodimporter import Importer as prodimporter
from .modules.screenimporter import Importer as screenimporter
from .modules.branchname import branchname

from .modules.shipping_profits.findProfits import Filewriter


def checkdata(module, arg):
    '''returns bool'''
    imp = module(arg)
    check = imp.nodata

    return check


def makeinventory(arg):
    imp = invimporter(arg)
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
        datacheck = checkdata(invimporter, form.string.data)
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
        datacheck = checkdata(prodimporter, form.string.data)
        if not datacheck:
            element = prodimporter(form.string.data)
        form.string.data = ''
    return render_template('production.html',
                           form=form,
                           element=element,
                           datacheck=datacheck,
                           )


def profitredirect(**kwarg):
    return url_for('shippingprofits', **kwarg)


@app.route('/', methods=['GET', 'POST'])
@app.route('/marketinfos', methods=['GET', 'POST'])
def marketinfos():
    element = None
    datacheck = False
    submitform = ScreenForm()
    jsonform = JsonForm()

    # Blank values to load an empty page properly
    jsonstring = ""
    link = ""

    if submitform.validate_on_submit():
        datacheck = checkdata(screenimporter, submitform.string.data)
        if not datacheck:
            element = screenimporter(submitform.string.data)
            jsonform.string.data = element.jsondict
            jsonstring = element.jsonstring
            jsondict = element.jsondict

            h = str(hash(jsonstring))

            # url message
            messages = h
            # json stored in a cookie
            # Has to be a dict for in order to get it in shippingprofits
            session[h] = jsondict
            # for testing purposes
            session['hash'] = h

            link = profitredirect(messages=messages)

        submitform.string.data = ''

    return render_template('marketinfos.html',
                           submitform=submitform,
                           element=element,
                           jsonform=jsonform,
                           jsonstring=jsonstring,
                           datacheck=datacheck,
                           link=link,
                           )


# This view still under construction
@app.route('/shippingprofits', methods=['GET', 'POST'])
def shippingprofits():
    filepath = ""

    # check if redirected from marketinfos and get the cookie data
    try:
        h = request.args['messages']
        jsonstring = session.get(h)
        filepath = "application/files/"+h+".csv"
        data = Filewriter(jsonstring, filepath)
        Filewriter.csvmaker(data)

    except KeyError:
        jsonstring = None

    return render_template('shippingprofits.html',
                           jsonstring=jsonstring,
                           filepath=filepath
                           )


# File downloader
@app.route('/application/files/<path:path>')
def send_file(path):
    return send_from_directory('files',
                               path,
                               as_attachment=True,
                               )


@app.route('/tutorial_importers')
def tutorial_importers():
    prodlink = url_for('productionlines')
    return render_template('tutorial_importers.html', prodlink=prodlink)


@app.route('/tutorial_market')
def tutorial_market():
    return render_template('tutorial_market.html')


'''
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
'''


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

    # TODO make navbar name a clickable link redirecting to /home
    # following code doesn't work
    #namestring = '<a href="'+url_for("marketinfos")+'"PrUn Data Importer '+branchname()+'</a>'
    namestring = "PrUn Data Importer "+branchname()

    return Navbar(
        namestring,
        View('Market Infos Screen', 'marketinfos'),
        #View('Shipping Profits', 'shippingprofits'),
        View('Inventory Importer', 'inventory'),
        View('Production Lines', 'productionlines'),
        Subgroup('Turorials',
                 View('Inventory & Prod. Lines Importers',
                      'tutorial_importers'),
                 View('Market Infos Screen', 'tutorial_market'))
    )


nav.init_app(app)
