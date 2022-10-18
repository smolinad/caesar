from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length

TEXT_CIPHER_MODES = ["Caesar", "Affine", "Vigenere", "Substitution", "Permutation", "Hill (Text)"]
IMG_CIPHER_MODES = ["Hill (Image)"]

class InputForm(FlaskForm):
    cypher_mode = SelectField(label='State', choices=[mode + " cipher"  for mode in TEXT_CIPHER_MODES])
    input_text = TextAreaField("input_text", validators=[DataRequired(), Length(max=1000)], default=None)
    input_key = TextAreaField("input_key", default=None)
    encrypt = SubmitField("Encrypt")
    decrypt = SubmitField("Decrypt")
    
class ImageForm(FlaskForm):
    cypher_mode = SelectField(label='State', choices=[mode + " cipher"  for mode in IMG_CIPHER_MODES])
    input_img = FileField("input_img", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg','png','JPG','JPEG','PNG'])])
    input_key = TextAreaField("input_key", default=None)
    encrypt_img = SubmitField("Encrypt")
    decrypt_img = SubmitField("Decrypt")