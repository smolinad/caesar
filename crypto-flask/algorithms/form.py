from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

CYPHER_MODES = ["Caesar", "Vigenere", "Substitution", "Permutation", "Hill"]

class InputForm(FlaskForm):
    cypher_mode = SelectField(label='State', choices=[mode + " cypher"  for mode in CYPHER_MODES])
    input_text = TextAreaField("input_text", validators=[DataRequired()], default=None)
    input_key = TextAreaField("input_key", default=None)
    encrypt = SubmitField("Encrypt")
    decrypt = SubmitField("decrypt")