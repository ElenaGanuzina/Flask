from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/clothes/')
def clothes():
    context = {
        'title': "Clothes"
    }
    return render_template("clothes.html", **context)


@app.route('/shoes/')
def shoes():
    context = {
        'title': "Shoes"
    }
    return render_template("shoes.html", **context)


@app.route('/dress/')
def dress():
    context = {
        'title': "Dress",
        'price': "$100"
    }
    return render_template("dress.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
