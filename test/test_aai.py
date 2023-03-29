from src.main import upload, transcribe, wait_for_trancription, write_subtitles
import unittest
import os


class TestAAI(unittest.TestCase):
    def setUp(self):
        self.audio_path = 'test/data/output.mp3'
        self.subtitles_path = 'test/data/subtitles.srt'
        self.upload_url = upload(self.audio_path)
        self.transcript_id = transcribe(self.upload_url)
        wait_for_trancription(self.transcript_id)
        write_subtitles(self.transcript_id, self.subtitles_path)

    def test_upload(self):
        self.assertIsNotNone(self.upload_url)

    def test_transcribe(self):
        self.assertIsNotNone(self.transcript_id)

    def test_get_subtitles(self):
        self.assertTrue(os.path.exists(self.subtitles_path))
