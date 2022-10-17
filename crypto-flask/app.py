from algorithms.caesar import caesarEncrypt, caesarDecrypt
from algorithms.vigenere import vigenereEncrypt, vigenereDecrypt
from algorithms.affine import affineEncrypt, affineDecrypt
from algorithms.substitution import substitutionEncrypt, substitutionDecrypt, substitutionCryptanalysis
from algorithms.permutation import permutationDecrypt, permutationEncrypt
from algorithms.hillText import hillCryptoAnalysis, hillEncrypt, hillDecrypt
# from algorithms.hillImage import hillImgEncrypt, hillImgDecrypt
from algorithms.goodies import processInput, InputKeyError


from flask import Flask, redirect, url_for, session, flash, send_from_directory
from flask_session import Session
from flask.templating import render_template
from werkzeug.utils import secure_filename
import cv2 as cv

from PIL import Image
import base64 
from io import BytesIO

from algorithms.form import InputForm, ImageForm

import os


UPLOAD_FOLDER = 'web/static/uploads/uploaded'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

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
                            session["output_text"], session["output_key"] = caesarEncrypt(input_text, input_key) #Ok
                        case "Vigenere cipher":
                            session["output_text"], session["output_key"] = vigenereEncrypt(input_text, input_key) #Ok
                        case "Affine cipher":
                            session["output_text"], session["output_key"] = affineEncrypt(input_text, input_key) #Ok 
                        case "Substitution cipher":
                            session["output_text"], session["output_key"] = substitutionEncrypt(input_text, input_key) #Ok
                        case "Permutation cipher":
                            session["output_text"], session["output_key"] = permutationEncrypt(input_text, input_key) #Ok
                        case "Hill (Text) cipher":
                            session["output_text"], session["output_key"] = hillEncrypt(input_text, input_key) # Ok
                   
                    return redirect(url_for('outputTextAndKey')) 

                except InputKeyError as e:
                    flash(e.message)     
                         
            else:
                match cypher_mode:
                    case "Caesar cipher":
                        session["output_text"], session["output_key"] = caesarEncrypt(input_text) #Ok 
                    case "Vigenere cipher":
                        session["output_text"], session["output_key"] = vigenereEncrypt(input_text) #Ok
                    case "Affine cipher":
                        session["output_text"], session["output_key"] = affineEncrypt(input_text) #Ok
                    case "Substitution cipher":
                        session["output_text"], session["output_key"] = substitutionEncrypt(input_text) # Ok (I hope :s)
                    case "Permutation cipher":
                        session["output_text"], session["output_key"] = permutationEncrypt(input_text) # Ok
                    case "Hill (Text) cipher":
                        session["output_text"], session["output_key"] = hillEncrypt(input_text) # Ok
                return redirect(url_for('outputTextAndKey')) 
                
        elif form.decrypt.data:
            if input_key != '':
                try:
                    session["encrypted_or_decrypted"] = "decrypted"
                    match cypher_mode:
                        case "Caesar cipher":
                            session["output_text"], session["output_key"] = caesarDecrypt(input_text, input_key) # Ok
                        case "Vigenere cipher":
                            session["output_text"], session["output_key"] = vigenereDecrypt(input_text, input_key) # Ok
                        case "Affine cipher":
                            session["output_text"], session["output_key"] = affineDecrypt(input_text, input_key) # Ok
                        case "Substitution cipher":
                            session["output_text"], session["output_key"] = substitutionDecrypt(input_text, input_key) #Ok
                        case "Permutation cipher":
                            session["output_text"], session["output_key"] = permutationDecrypt(input_text, input_key) # Ok
                        case "Hill (Text) cipher":
                            session["output_text"], session["output_key"] = hillDecrypt(input_text, input_key) #Ok

                    return redirect(url_for('outputTextAndKey'))  

                except InputKeyError as e:
                    flash(e.message) 

            else:
                match cypher_mode:
                    case "Caesar cipher":
                        session["analysis_output"] = caesarDecrypt(input_text) # Ok
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Vigenere cipher":
                        session["analysis_output"] = vigenereDecrypt(input_text) # Ok
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Affine cipher":
                        session["analysis_output"] = affineDecrypt(input_text) # Ok
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Substitution cipher":
                        session["analysis_output"] = substitutionCryptanalysis(input_text) #Ok
                        return redirect(url_for('substitutionAnalysis'))
                    case "Permutation cipher":
                        session["analysis_output"] = permutationDecrypt(input_text) # Ok
                        return redirect(url_for('bruteForceAnalysis'))
                    case "Hill (Text) cipher":
                        return
                        # session["output_text"] = hillCryptoAnalysis(input_text)
                        # return redirect(url_for('outputTextAndKey'))  

                

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


@app.route('/decrypted-', methods=['GET'])
def substitutionAnalysis():
    frequency, digraphs = session.get("analysis_output", None)
    return render_template('subsanalysis.html', frequency=frequency, digraphs=digraphs)


@app.route('/image-ciphers', methods=['GET', 'POST'])
def imgAlgorithms():
    form = ImageForm()
    if form.validate_on_submit():
        cypher_mode = form.cypher_mode.data
        input_key = form.input_key.data
        input_img = form.input_img.data
        filename = secure_filename(input_img.filename)
        path_ = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        input_img.save(path_)

        # encoded = b64encode(input_img)
        # mime = "image/jpeg"
        # session["input_img"] = "data:%s;base64,%s" % (mime, encoded)
        session["input_img_folder"] = 'uploads/uploaded/'
        session["input_img_filename"] = filename
        if form.encrypt_img.data:
            session["encrypted_or_decrypted"] = "encrypted"

            try:
                match cypher_mode:
                    case "Hill (Image) cipher":
                        return redirect(url_for('outputImgAndKey')) 

            except InputKeyError as e:
                flash(e.message)                          
                
        # elif form.decrypt.data:
        #     try:
        #         session["encrypted_or_decrypted"] = "decrypted"
        #         match cypher_mode:
        #             case "Hill (Image) cipher":
        #                 path_ = '/uploads/img' + filename
        #                 form.file.data.save(path_)
        #                 hillImgDecrypt(path_, input_key)
        #                 # session["output_img"], session["output_key"] = hillImgDecrypt(input_img, input_key) 

        #         return redirect(url_for('outputImgAndKey'))  

        #     except InputKeyError as e:
        #         flash(e.message)           
    return render_template('imgalg.html', form=form)


@app.route('/encrypted-img', methods=['POST', 'GET'])
def outputImgAndKey():
    mode = session.get("encrypted_or_decrypted", None) 

    input_img_folder = session.get("input_img_folder", None)
    input_img_filename = session.get("input_img_filename", None)

    output_img_folder = "uploads/" + mode
    output_img_filename = session.get("output_img_filename", None)

    return render_template(
        'imgoutput.html',
        input_img_folder=input_img_folder,
        input_img_filename=input_img_filename,
        output_img_folder=output_img_folder,
        output_img_filename=output_img_filename,
    )



if __name__ == '__main__':
    app.run(debug=True)