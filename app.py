from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class Playlist(FlaskForm):
    song_title = StringField(
        'Keyword', 
        validators=[DataRequired()]
    )

playlist = []

def store_song(my_song):
    playlist.append(dict(
        song = my_song,
        date = datetime.today()
    ))

@app.route('/', methods=('GET', 'POST'))
def index():
    form = Playlist()
    if form.validate_on_submit():
        store_song(form.song_title.data)
        return redirect('/view_playlist')
    return render_template('index.html', form=form)

# @app.route('/view_playlist')
# def vp():
#     return render_template('vp.html', playlist=playlist)