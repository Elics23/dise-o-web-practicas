from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/galeria')
def galeria():
    return render_template('diseno.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)
