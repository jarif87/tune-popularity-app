from flask import Flask, render_template, request, url_for
import pickle
import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Load the trained model
with open('cat_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the features expected by the model
FEATURES = [
    'artist_familiarity', 'artist_hotttnesss', 'song_hotttnesss', 'year', 'start_of_fade_out'
]

# Define a form class for validation with CSRF disabled
class SongForm(FlaskForm):
    artist_familiarity = StringField('Artist Familiarity', validators=[DataRequired()])
    artist_hotttnesss = StringField('Artist Hotttnesss', validators=[DataRequired()])
    song_hotttnesss = StringField('Song Hotttnesss', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    start_of_fade_out = StringField('Start of Fade Out', validators=[DataRequired()])
    
    class Meta:
        csrf = False  # Disable CSRF protection

@app.route('/', methods=['GET', 'POST'])
def predict():
    form = SongForm()
    response = None
    error = None

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Extract and convert inputs to floats
            inputs = {
                'artist_familiarity': float(request.form['artist_familiarity']),
                'artist_hotttnesss': float(request.form['artist_hotttnesss']),
                'song_hotttnesss': float(request.form['song_hotttnesss']),
                'year': float(request.form['year']),
                'start_of_fade_out': float(request.form['start_of_fade_out'])
            }

            # Create DataFrame for prediction with correct feature order
            input_df = pd.DataFrame([inputs], columns=FEATURES)

            # Make prediction
            prediction = model.predict(input_df)[0]
            response = int(prediction)

        except ValueError:
            error = "Invalid input. Please ensure all fields are numeric."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', form=form, response=response, error=error)

if __name__ == '__main__':
    app.run(debug=True)