import unittest
import os
import main
from PIL import Image

class MainTest(unittest.TestCase):
    def test_getInfoFromFilePath(self):
        image_path = os.path.abspath("test/test.jpg")
        title, desc, timestamp = main.getInfoFromFilePath(image_path)
        self.assertEqual(title, None)
        self.assertEqual(desc, "#photo_gyazo #include_no_exif")
        self.assertEqual(timestamp, 1585821274)
    
    def test_getInfoFromExif(self):
        image_path = os.path.abspath("test/test.jpg")
        image = Image.open(image_path)
        exif = image._getexif()
        title, desc, timestamp = main.getInfoFromExif(exif)