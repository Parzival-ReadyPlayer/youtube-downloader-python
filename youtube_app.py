from flask import Flask, render_template, url_for, redirect, request, flash, send_file, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from io import BytesIO
from pytube import YouTube, Playlist
from app import download_playlist, download_video, download_audio
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Formulario
class linkForm(FlaskForm):
    link = StringField('Youtube link', validators=[DataRequired()])
    submit = SubmitField('Descargar')
    


@app.route("/", methods = ["GET", "POST"])
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










@app.route("/download_audio", methods = ["GET", "POST"])
def download_audio():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        name = url.title + '.mp3'
        audio = url.streams.get_audio_only()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=name)
    return redirect(url_for("home"))

@app.route("/download_video", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        name = url.title
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=name, mimetype='video/mp4')
    return redirect(url_for("home"))





if __name__ == '__main__':
    app.run(debug=True)