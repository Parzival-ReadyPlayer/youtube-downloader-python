from flask import Flask, render_template, url_for, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import download_audio, download_playlist, download_video
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Formulario
class linkForm(FlaskForm):
    link = StringField('Youtube link', validators=[DataRequired()])
    submit = SubmitField('Descargar')
    
# Ruta audio

@app.route('/', methods=['GET', 'POST'])
def index():
    # Create form
    form = linkForm()
    if request.method == "POST":
        flash('Iniciando descarga, espere por favor..', 'warning')
        # Get link from form
        link = request.form.get('link')
        
        while True:
            # Try catch block, if the input is not valid we print a error message
            try:
                # Call function
                audio = download_audio(link)
                flash('Download succesfull', 'success')
                return redirect(url_for('index'))
            except:
                flash('That is an invalid link', 'danger')
                return redirect(url_for('index'))
    return render_template('index.html', form = form)


# Ruta playlist

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    form = linkForm()
    if request.method == 'POST':
        link = request.form.get('link')
        while True:
            try:
                download_playlist(link)
                flash('Download complete', 'success')
                return redirect('playlist')
            except:
                flash('That is an invalid link for a playlist', 'danger')
                return redirect('playlist')
            
    return render_template('playlist.html', form=form)


# Ruta video

@app.route('/video', methods=['GET', 'POST'])
def video():
    # Create form
    form = linkForm()
    if request.method == "POST":
        # Get link from form
        link = request.form.get('link')
        while True:
            # Try catch block, if the input is not valid we print a error message
            try:
                # Call function
                download_video(link)
                flash('Download succesfull', 'success')
                return redirect(url_for('video'))
            except:
                flash('That is an invalid link', 'danger')
                return redirect(url_for('video'))
    return render_template('video.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)