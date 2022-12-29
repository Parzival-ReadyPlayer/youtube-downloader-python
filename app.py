from pytube import YouTube, Playlist
import pytube.request
import os

pytube.request.default_range_size = 1048576 



def download_audio(link):
    # Create a object of Youtube class
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_audio_only()
    # Destination of the file
    destination = os.environ.get('NEW_PATH')
    print(f'Este es el path de destino: {destination}')
    
    try:
        # Download object and put the file on the destination
        audio = youtube_object.download(output_path=destination)
        
        # Split the path name into a pair, ext have the extension part
        base, ext = os.path.splitext(audio)
        
        # Add a new extension
        new_file = base + '.mp3'
        # Rename the file, first argument old file, second argumet new_file
        os.rename(audio, new_file)
    except:
        print('DOWNLOAD FAILED!')
    
    
        
        
def download_playlist(link):
    
    # Check if the link corresponds to a playlist
    
    if 'list' in link:
        
        # Create a playlist object
        playlist = Playlist(str(link))
        
        destination = os.environ.get('NEW_PATH')
        try:
            # Loop for videos in a playlist
            for video in playlist.videos:
                # Download 
                audio = video.streams.first().download(output_path=destination)
                # Split the path of the file
                base, ext = os.path.splitext(audio)
                # Add the extension 
                new_file = base + '.mp3'
                # Rename the file
                os.rename(audio, new_file)            
        except:
            print('Download failed')
    else:
        # If not a playlist
        exit()
    
   

def download_video(link):
    # Create a object of Youtube class
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_highest_resolution()
    # Destination of the file
    destination = os.environ.get('NEW_PATH')
    
    try:
        # Download object and put the file on the destination
        video = youtube_object.download(output_path=destination)
        
        # Split the path name into a pair, ext have the extension part
        base, ext = os.path.splitext(video)
        
        # Add a new extension
        new_file = base + '.mp4'
        # Rename the file, first argument old file, second argumet new_file
        os.rename(video, new_file)
    except:
        print('DOWNLOAD FAILED')
    
    


  
    
        
   
        