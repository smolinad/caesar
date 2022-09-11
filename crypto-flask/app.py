from algorithms.caesar import caesarEncrypt, caesarDecrypt
from algorithms.vigenere import vigenereEncrypt, vigenereDecrypt
from algorithms.affine import affineEncrypt, affineDecrypt
from algorithms.substitution import substitutionEncrypt
from algorithms.permutation import permutationEncrypt
from algorithms.hillText import hillEncrypt, hillDecrypt
from algorithms.goodies import processInput, InputKeyError

from flask import Flask, redirect, url_for, session, flash
from flask.templating import render_template

from algorithms.form import InputForm, ImageForm

import os

UPLOAD_FOLDER = '/uploads/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    if form.validate_on_submit():
        cypher_mode = form.cypher_mode.data
        input_text = processInput(form.input_text.data)
        input_key = form.input_key.data

        if form.encrypt.data:
            session["encrypted_or_decrypted"] = "encrypted"
            if input_key != '':
                try:
                    match cypher_mode:
                        case "Caesar cipher":
                            session["output_text"], session["output_key"] = caesarEncrypt(input_text, input_key)
                        case "Vigenere cipher":
                            session["output_text"], session["output_key"] = vigenereEncrypt(input_text, input_key)
                        case "Affine cipher":
                            session["output_text"], session["output_key"] = affineEncrypt(input_text, input_key)
                        case "Substitution cipher":
                            session["output_text"], session["output_key"] = substitutionEncrypt(input_text, input_key)
                        case "Permutation cipher":
                            session["output_text"], session["output_key"] = permutationEncrypt(input_text, input_key)
                        case "Hill (Text) cipher":
                            session["output_text"], session["output_key"] = hillEncrypt(input_text, input_key)
                   
                    return redirect(url_for('outputTextAndKey')) 

                except InputKeyError as e:
                    flash(e.message)     
                         
            else:
                match cypher_mode:
                    case "Caesar cipher":
                        session["output_text"], session["output_key"] = caesarEncrypt(input_text)
                    case "Vigenere cipher":
                        session["output_text"], session["output_key"] = vigenereEncrypt(input_text)
                    case "Affine cipher":
                        session["output_text"], session["output_key"] = affineEncrypt(input_text)
                    case "Substitution cipher":
                        session["output_text"], session["output_key"] = substitutionEncrypt(input_text)
                    case "Permutation cipher":
                        session["output_text"], session["output_key"] = permutationEncrypt(input_text)
                    case "Hill (Text) cipher":
                        session["output_text"], session["output_key"] = hillEncrypt(input_text)

                return redirect(url_for('outputTextAndKey')) 
                
        elif form.decrypt.data:
            if input_key != '':
                try:
                    session["encrypted_or_decrypted"] = "decrypted"
                    match cypher_mode:
                        case "Caesar cipher":
                            session["output_text"], session["output_key"] = caesarDecrypt(input_text, input_key)
                        case "Vigenere cipher":
                            session["output_text"], session["output_key"] = vigenereDecrypt(input_text, input_key)
                        case "Affine cipher":
                            session["output_text"], session["output_key"] = affineDecrypt(input_text, input_key)

                    return redirect(url_for('outputTextAndKey'))  

                except InputKeyError as e:
                    flash(e.message) 

            else:
                match cypher_mode:
                    case "Caesar cipher":
                        session["analysis_output"] = caesarDecrypt(input_text)
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Vigenere cipher":
                        session["analysis_output"] = vigenereDecrypt(input_text)
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Affine cipher":
                        session["analysis_output"] = affineDecrypt(input_text)
                        return redirect(url_for('bruteForceAnalysis'))

                

    return render_template('textalg.html', form=form)


@app.route('/encrypted', methods=['GET'])
def outputTextAndKey():
    output_text = session.get("output_text", None)
    output_key = session.get("output_key", None)
    encrypted_or_decrypted = session.get("encrypted_or_decrypted", None)
    return render_template(
        'output.html', 
        encrypted_or_decrypted=encrypted_or_decrypted, 
        output_text=output_text, 
        output_key=output_key)

@app.route('/decrypted', methods=['GET'])
def bruteForceAnalysis():
    output = session.get("analysis_output", None)
    return render_template('bruteforce.html', output=output)

@app.route('/image-ciphers', methods=['GET', 'POST'])
def imgAlgorithms():
    form = ImageForm()
    # if form.validate_on_submit():
    #     cypher_mode = form.cypher_mode.data
    #     img = form.photo_or_pdf_file.data
    #     input_key = form.input_key.data

    #     if form.encrypt.data:
    #         try:
    #             match:
    #                 case "Hill (Image) cipher":
    #                     session["output_text"], session["output_key"] = caesarEncrypt(input_text)

    #         except InputKeyError as e:
    #                 flash(e.message) 
    return render_template('imgalg.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)