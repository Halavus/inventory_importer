from flask import Flask, render_template
from flask import Response
from flask import stream_with_context, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from importer import Importer as i
from secret_key import secret_key as secret_key

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key

bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    string = StringField(
        'Paste the html "InventoryView__grid" element and submit',
        validators=[DataRequired()])
    submit = SubmitField('Submit')

def makelist(arg):
    imp=i(arg)
    table=imp.grouped

    return table

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    element = None
    form = NameForm()
    if form.validate_on_submit():
        element = makelist(form.string.data)
        form.string.data = ''
    return render_template('index.html', form=form, element=element)
'''
@app.route('/large.csv')
def generate_large_csv():
    
    form=NameForm()
    arg=makelist(form.string.data)

    def generate(arg=arg):
        for row in arg:
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')
'''

@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        yield request.args['name']
        yield '!'
    return Response(stream_with_context(generate()))

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
