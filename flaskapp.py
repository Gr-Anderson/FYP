from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

class Form(FlaskForm):
    captured = SelectField('captured', choices=[('sub1', 'Subject1'), ('sub2', 'Subject2'), ('sub3', 'Subject3')])
    template = SelectField('template', choices=[('sub1', 'Subject1'), ('sub2', 'Subject2'), ('sub3', 'Subject3')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    if request.method == 'POST':
        return render_template('result.html', captured=form.captured.data, template=form.template.data)

    return render_template('landingpage2.html', form=form)

@app.route('/result')
def result():
    # form = Form()

    # if request.method == 'POST':
    #     return '<h1>Captured: {}, Template: {}</h1>'.format(form.captured.data, form.template.data)

    return render_template('result.html')
if __name__ == '__main__':
    app.run(debug=True)