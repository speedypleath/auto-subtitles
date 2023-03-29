from src.main import add_subtitles, write_mp3_from_video
import os
import ffmpeg
import unittest


class TestFFmpeg(unittest.TestCase):
    def setUp(self):
        self.video_path = os.getenv("TEST_VIDEO_PATH")
        self.subtitles_path = os.getenv("TEST_SUBTITLES_PATH")
        self.output_path = os.getenv("TEST_OUTPUT_PATH")
        self.audio_path = os.getenv("TEST_AUDIO_PATH")

    def test_add_subtitles(self):
        add_subtitles(self.video_path, self.subtitles_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
        output = ffmpeg.probe(self.output_path)
        stream_names = [stream["codec_name"] for stream in output["streams"]]
        self.assertIn("mov_text", stream_names)

    def test_write_mp3(self):
        write_mp3_from_video(self.video_path, self.audio_path)
        self.assertTrue(os.path.exists(self.audio_path))
