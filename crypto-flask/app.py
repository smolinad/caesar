from algorithms.caesar import encryptCaesar
from algorithms.substitution import substitutionEncrypt
from algorithms.goodies import processInput

from flask import Flask, request, redirect, url_for
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
    if form.validate_on_submit:
        if form.encrypt.data:
            cypher_mode = form.cypher_mode.data
            input_text = processInput(form.input_text.data)
            print(input_text)
            input_key = form.input_key.data

            if input_key != '':
                match cypher_mode:
                    case "Caesar cypher":
                        output_text = encryptCaesar(input_text, input_key)
                    case "Substitution cypher":
                        output_text = encryptCaesar(input_text, input_key)
            else:
                match cypher_mode:
                    case "Caesar cypher":
                        output_text = encryptCaesar(input_text)
                    case "Substitution cypher":
                        output_text = encryptCaesar(input_text)

            return redirect(url_for('encrypted', output_text=output_text))
   
        elif form.decrypt.data:
            print("This is the way to go!")

    return render_template('index.html', form=form)


@app.route('/encrypted', methods=['GET'])
def encrypted():
    output_text = request.args['output_text']
    return render_template('encrypted.html', output_text=output_text)


if __name__ == '__main__':
    app.run(debug=True)