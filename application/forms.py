from flask_wtf import FlaskForm

from wtforms.validators import DataRequired
from wtforms import TextAreaField, SubmitField


class InvForm(FlaskForm):
    '''Used in inventory importer'''
    string = TextAreaField(
        'Paste the html "InventoryView__grid" element and submit',
        render_kw={"placeholder":
                   'HTML code: '
                   '<div class="InventoryView__grid___1y8GFWz"> ...'},
        validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProdForm(FlaskForm):
    '''Used in production lines'''
    string = TextAreaField(
        'Paste the html "SiteProductionLines__column___" element and submit',
        render_kw={"placeholder":
                   'HTML code: '
                   '<div class="SiteProductionLines__column___ij4g8Kg '
                   'SiteProductionLines__columnBase___3eLJ7nE" ...'},
        validators=[DataRequired()])
    submit = SubmitField('Submit')


class ScreenForm(FlaskForm):
    '''Used in marketinfos'''
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


class JsonForm(FlaskForm):
    string = TextAreaField('json string of all data', render_kw={
        'id': 'jsonstring',
        'style': 'height: 100px'})
    submit = SubmitField('Submit')
