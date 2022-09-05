from algorithms.caesar import caesarEncrypt, caesarDecrypt
from algorithms.vigenere import vigenereEncrypt
from algorithms.affine import affineEncrypt, affineDecrypt
from algorithms.goodies import processInput, InputKeyError

from flask import Flask, redirect, url_for, session, flash, jsonify
from flask.templating import render_template

from algorithms.form import InputForm

import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    if form.validate_on_submit():
        cypher_mode = form.cypher_mode.data
        input_text = processInput(form.input_text.data)
        input_key = form.input_key.data

        if form.encrypt.data:
            if input_key != '':
                try:
                    match cypher_mode:
                        case "Caesar cypher":
                            session["output_text"], session["output_key"] = caesarEncrypt(input_text, input_key)
                        case "Vigenere cypher":
                            session["output_text"], session["output_key"] = vigenereEncrypt(input_text, input_key)
                        case "Affine cypher":
                            session["output_text"], session["output_key"] = affineEncrypt(input_text, input_key)
                   
                    return redirect(url_for('encrypted'))    
                except InputKeyError as e:
                    flash(e.message)     
                         
            else:
                match cypher_mode:
                    case "Caesar cypher":
                        session["output_text"], session["output_key"] = caesarEncrypt(input_text)
                    case "Vigenere cypher":
                        session["output_text"], session["output_key"] = vigenereEncrypt(input_text)
                    case "Affine cypher":
                        session["output_text"], session["output_key"] = affineEncrypt(input_text)

                return redirect(url_for('encrypted')) 
                
        elif form.decrypt.data:
            if input_key != '':
                try:
                    match cypher_mode:
                        case "Caesar cypher":
                            session["analysis_output"] = caesarDecrypt(input_text, input_key)
                            return redirect(url_for('bruteForceAnalysis'))
                        case "Affine cypher":
                            session["analysis_output"] = affineDecrypt(input_text, input_key)
                            return redirect(url_for('bruteForceAnalysis'))

                except InputKeyError as e:
                    flash(e.message)  
            else:
                match cypher_mode:
                    case "Caesar cypher":
                        session["analysis_output"] = caesarDecrypt(input_text)
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Affine cypher":
                        session["analysis_output"] = affineDecrypt(input_text)
                        return redirect(url_for('bruteForceAnalysis'))

    return render_template('index.html', form=form)


@app.route('/encrypted', methods=['GET'])
def encrypted():
    output_text = session.get("output_text", None)
    output_key = session.get("output_key", None)
    return render_template('encrypted.html', output_text=output_text, output_key=output_key)

@app.route('/decrypted', methods=['GET'])
def bruteForceAnalysis():
    output = session.get("analysis_output", None)
    return render_template('bruteforce.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)