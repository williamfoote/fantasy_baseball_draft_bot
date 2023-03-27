from flask import Flask, render_template, request
from wtforms import Form, SelectField

app = Flask(__name__)

# Define the list of names for the dropdown
names_list = ['Alice', 'Bob', 'Charlie', 'Dave']

# Define a counter for the current turn number
turn_counter = 0

# Define a wtforms form with a dropdown field for the names
class NameForm(Form):
    name = SelectField('Name', choices=[(name, name) for name in names_list])

# Define a route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    global turn_counter # Use the global variable for the turn counter
    form = NameForm(request.form)
    if request.method == 'POST' and form.validate():
        # Increment the turn counter
        turn_counter += 1
        # Get the selected name from the form
        selected_name = form.name.data
        # Display a message with the selected name and turn number
        message = f"{selected_name} is up! It's turn {turn_counter}."
        return render_template('message.html', message=message)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
