from src.main import add_subtitles_to_video
import unittest
import os
import ffmpeg


class TestMain(unittest.TestCase):
    def setUp(self):
        self.video_path = 'test/data/test.mp4'
        self.output_path = 'test/data/output.mp4'

    def test_add_subtitles_to_video(self):
        add_subtitles_to_video(self.video_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
        output = ffmpeg.probe(self.output_path)
        stream_names = [stream['codec_name'] for stream in output['streams']]
        self.assertIn('mov_text', stream_names)
