from src.main import add_subtitles
import os
import ffmpeg
    
# test add subtitles to video
def test_add_subtitles():
    add_subtitles('test/data/test.mp4', 'test/data/subtitles.srt', 'test/data/output.mp4')
    assert os.path.exists('test/data/output.mp4')
    output = ffmpeg.probe('test/data/output.mp4')
    stream_names = [stream['codec_name'] for stream in output['streams']]
    assert 'mov_text' in stream_names
    os.remove('test/data/output.mp4')