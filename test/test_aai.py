from src.main import upload, transcribe, wait_for_trancription, write_subtitles
from dotenv import load_dotenv
import unittest
import os


class TestAAI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.audio_path = os.getenv("TEST_AUDIO_PATH")
        self.subtitles_path = os.getenv("TEST_SUBTITLES_PATH")
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
