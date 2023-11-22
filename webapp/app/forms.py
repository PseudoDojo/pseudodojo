from flask_wtf import FlaskForm
from wtforms import SelectField

class FormatForm(FlaskForm):
    type_dropdown = SelectField('Select Type', choices=["NC SR (ONCVPSP v0.4)", "NC FR (ONCVPSP v0.4)"])
    xc_dropdown = SelectField('Select Exchange Correlation', choices=["PBE", "PBEsol", "LDA"])
    table_dropdown = SelectField('Select Table', choices=["standard", "stringent"])
    format_dropdown = SelectField('Select Type', choices=["psp8", "html", "in", "out"])