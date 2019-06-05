from flask import Flask, render_template, request
from forms import HealthForm

app = Flask(__name__)
app.secret_key = 'STACKOVERFLOW'


@app.route('/', methods=['post', 'get'])
def home():
    form = HealthForm()
    if form.validate_on_submit():
        return str(form.meditation.data)
    else:
        return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5060)