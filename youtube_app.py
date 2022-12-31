from flask import Flask, render_template, url_for, redirect, request, flash, send_file, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from io import BytesIO
from pytube import YouTube
from app import download_playlist, download_video, download_audio
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
                download_audio(link)
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





@app.route("/home", methods = ["GET", "POST"])
def home():
    
    form = linkForm()
    if request.method == "POST":
        session['link'] = request.form.get('link')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            flash('Link invalido', 'danger')
            return redirect('home')
        return render_template("download.html", url = url, form = form)
    return render_template("home.html", form=form)

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        name = url.title
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=name, mimetype="video/mp4")
    return redirect(url_for("home"))


@app.route("/download_audio", methods = ["GET", "POST"])
def download_audio():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        name = url.title
        audio = url.streams.get_audio_only()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=name, mimetype="audio/mp3")
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)