from flask import Flask, render_template, url_for, redirect, request, flash, send_file, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from io import BytesIO
from pytube import YouTube, Playlist
from zipfile import ZipFile
import os, requests




app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')



# Handlers

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html',error=error), 500

# Formulario
class linkForm(FlaskForm):
    link = StringField('Youtube link', validators=[DataRequired()])
    submit = SubmitField('Descargar')
    
class playlistForm(FlaskForm):
    link = StringField('Playlist', validators=[DataRequired()])
    submit = SubmitField('Convertir')
    
def is_valid_url(url):
    try:
        # Hace una solicitud a la URL y almacena la respuesta
        response = requests.get(url)

        # Si la respuesta tiene un código de estado OK (200)
        if response.status_code == 200:
            # Regresa True
            return True
        else:
            # Si no es OK, regresa False
            return False
    except:
        # Si ocurre cualquier otro error, regresa False
        return False

@app.route("/", methods = ["GET", "POST"])
def home():
    form = linkForm()
    
    if request.method == "POST":
        try:
            
            if is_valid_url(request.form.get('link')):
                session['link'] = request.form.get('link')
                try:
                    url = YouTube(session['link'])
                    url.check_availability()
                except:
                    print("url no disponible")
                return render_template("download.html", url = url, form = form)
            else:
                flash('No es un link valido', 'danger')
        except:
            flash('Link invalido', 'danger')
            return redirect(url_for('home'))
    return render_template("home.html", form=form)


@app.route("/download_audio", methods = ["GET", "POST"])
def download_audio():
    if request.method == "POST":
        buffer = BytesIO()
        print(f"esto es buffer {buffer}")
        url = YouTube(session['link'])
        print(url)
        name = url.title + '.mp3'
        audio = url.streams.get_audio_only()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=name)
    return redirect(url_for("home"))

@app.route("/download_video", methods = ["GET", "POST"])
def download_video():
    # Action of the method POST 
    if request.method == "POST":
        # Create a buffer to save songs
        buffer = BytesIO()
        # Instantiate a Youtube object
        url = YouTube(session['link'])
        # Save song title
        name = url.title
        # Quality of video
        itag = request.form.get('itag')
        # Get song by itag
        video = url.streams.get_by_itag(itag)
        # Send to buffer
        video.stream_to_buffer(buffer)
        # Sets the reference point at the beginning of the file 
        buffer.seek(0)
        # Download function
        return send_file(buffer, as_attachment=True, download_name=name, mimetype='video/mp4')
    return redirect(url_for("home"))



@app.route("/playlist", methods = ["GET", "POST"])
def playlist():
    form = playlistForm()
    if request.method == "POST":
        session['link'] = request.form.get('link')
        if 'list' in session['link']:
            try:
                url = Playlist(session['link'])
            except:
                flash('Link invalido', 'danger')
                return redirect('playlist')
            return render_template("playlist_download.html", url = url, form = form)
        flash('Link invalid', 'danger')
        return redirect(url_for('playlist'))
    return render_template("playlist.html", form=form)






# Crea una función para descargar una canción individual
def download_song(video):
    # Crea un buffer de bytes para almacenar el audio
    buffer = BytesIO()

    # Obtiene el título de la canción y el audio en formato MP3
    name = video.title + '.mp3'
    audio = video.streams.get_audio_only()

    # Escribe el audio en el buffer
    audio.stream_to_buffer(buffer)

    # Regresa al principio del buffer
    buffer.seek(0)

    # Regresa el buffer como un archivo adjunto
    return buffer



@app.route("/playlist_download", methods = ["POST"])
def playlist_download():
    # Crea un buffer de bytes para almacenar el archivo ZIP
    buffer = BytesIO()

    # Crea un archivo ZIP en el buffer
    with ZipFile(buffer, 'w') as zip:
        # Si se hace una solicitud POST
        if request.method == 'POST':
            # Crea una instancia de Playlist con la URL de la playlist
            playlist = Playlist(session['link'])
            
            name_playlist = playlist.title
            
            print(name_playlist)

            # Para cada video en la playlist
            for video in playlist.videos:
                # Descarga la canción
                song = download_song(video)

                # Agrega la canción al archivo ZIP
                zip.writestr(video.title + '.mp3', song.getvalue())

    # Regresa al principio del buffer
    buffer.seek(0)
    
    # Crea una respuesta con el archivo adjunto
    return send_file(buffer, as_attachment=True, mimetype='application/zip', download_name=name_playlist + '.zip')



if __name__ == '__main__':
    app.run(debug=True)