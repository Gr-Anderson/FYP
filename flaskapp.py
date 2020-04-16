

class Form(FlaskForm):
    state = SelectField('state', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    city = SelectField('city', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    # form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]

    if request.method == 'POST':
    #     # city = City.query.filter_by(id=form.city.data).first()
        return '<h1>State: {}, City: {}</h1>'.format(form.state.data, form.city.data)

    return render_template('landingpage2.html', form=form)

    # <form method="POST">
    #     {{ form.csrf_token }}
    #     {{ form.state }}
    #     {{ form.city }}
    #     <input type="submit">
    # </form>