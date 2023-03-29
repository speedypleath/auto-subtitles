import pprint
import time
import ffmpeg
import requests
import os


CHUNK_SIZE = 5242880
AUTH_KEY = os.getenv('AAI_API_KEY')

def add_subtitles(video_path: str, subtitle_path: str, output_path: str) -> None:
    input = ffmpeg.input(video_path)
    subtitles = ffmpeg.input(subtitle_path)
    output = ffmpeg.output(input.video, input.audio, subtitles, output_path, 
                           scodec='mov_text', vcodec='copy', acodec='copy',
                           **{ 'metadata:s:s:0': "language=eng", 'metadata:s:s:0': "title=English" })
    output_ffmpeg = ffmpeg.overwrite_output(output)
    print(ffmpeg.compile(output_ffmpeg))
    output_ffmpeg.run()
    
def write_mp3_from_video(video_path: str, output_path: str) -> None:
    input = ffmpeg.input(video_path)
    output = ffmpeg.output(input.audio, output_path, acodec='mp3')
    output_ffmpeg = ffmpeg.overwrite_output(output)
    print(ffmpeg.compile(output_ffmpeg))
    output_ffmpeg.run()
    
def read_mp3_file(path):
    with open(path, 'rb') as _file:
        while True:
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data
            
def upload(filename):
    upload_response = requests.post(
        'https://api.assemblyai.com/v2/upload',
        headers={'authorization': AUTH_KEY}, data=read_mp3_file(filename)
    )
    print(upload_response.json())
    return upload_response.json()['upload_url']

def transcribe(audio_url):
    transcript_request = {
       'audio_url': audio_url,
    }
 
    headers = {
        "authorization": AUTH_KEY,
        "content-type": "application/json"
    }
    
    transcript_response = requests.post(
        'https://api.assemblyai.com/v2/transcript', 
        json=transcript_request, 
        headers=headers)
    pprint.pprint(transcript_response.json())
    return transcript_response.json()['id']

def get_subtitles(id):
    while True:
        headers = {
            "authorization": AUTH_KEY,
        }
        
        polling_response = requests.get("https://api.assemblyai.com/v2/transcript/" + id, headers=headers)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            return polling_response

        time.sleep(5)
link = upload('/Users/speedypleath/Projects/auto-subtitles/test/data/input.mp3')
id = transcribe(link)
response = get_subtitles(id)
pprint.pprint(response)