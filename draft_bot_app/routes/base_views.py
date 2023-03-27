from draft_bot_app import app

from flask import render_template, request
from wtforms import Form, SelectField
from draft_bot_app.packages.forms import NameForm
#########################################################################
########################### Base Pages ##################################
#########################################################################

# Define the list of names for the dropdown
names_list = ['Alice', 'Bob', 'Charlie', 'Dave']

# Define a counter for the current turn number
turn_counter = 0

# Define a route for the main page
@app.route('/')
def home():
	return render_template("home.html")

@app.route('/draft_bot', methods=['GET', 'POST'])
def draft_bot():
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
    return render_template('draft_bot.html', form=form)



# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/documentation")
# def documentation():
#     return render_template("documentation.html")

#########################################################################
########################### Error Pages #################################
#########################################################################

@app.errorhandler(404)
def page_not_found(e):
    return(render_template('404.html')), 404

@app.errorhandler(500)
def page_not_found(e):
    return(render_template('500.html')), 404