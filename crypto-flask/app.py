from algorithms.caesar import caesar
from algorithms.vigenere import vigenere

from flask import Flask, request
from flask.templating import render_template

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

@app.route('/',methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        # cypher_mode = request.form.get('cypher_mode')
        print(request.form.get('caesar'))
        cypher_mode = "vigenere"
        input_text = request.form.get('input_text')
        input_key = request.form.get('input_key')

        match cypher_mode:
            case "caesar":
                if input_key != '':
                    output_text = caesar(input_text, int(input_key))
                else:
                    output_text = caesar(input_text)
            case "vigenere":
                if input_key != '':
                    output_text = vigenere(input_text, input_key)
                else:
                    output_text = vigenere(input_text)
    else:
        return render_template('index.html')

    return render_template('index.html', 
                            input_text=input_text, 
                            input_key=input_key, 
                            output_text=output_text)


if __name__ == '__main__':
    app.run(debug=True)