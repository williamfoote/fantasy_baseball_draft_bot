from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, NumberRange
# from draft_bot_app.packages import mlb_players
import pandas as pd
import numpy as np

mlb_players_df = pd.read_csv("~/Documents/GitHub/fantasy_baseball_draft_bot/data/mcts_players.csv")
names_list = ['Alice', 'Bob', 'Charlie', 'Dave']

# Define a wtforms form with a dropdown field for the names
class NameForm(FlaskForm):
    name = SelectField('Name', choices=[(name, name) for name in names_list])