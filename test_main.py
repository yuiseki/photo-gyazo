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
        self.assertEqual(timestamp, 1585821679)
    
    def test_getInfoFromExif(self):
        image_path = os.path.abspath("test/test.jpg")
        image = Image.open(image_path)
        exif = image._getexif()
        title, desc, timestamp = main.getInfoFromExif(exif)
        print(title, desc ,timestamp)
        self.assertEqual(title, "Apple, iPhone SE")
        self.assertEqual(desc, "#photo_gyazo #Apple #iPhone_SE  ")
        self.assertEqual(timestamp, 1583283648.0)
    
    def test_getInfoFromExifOrFilePathWithExif(self):
        image_path = os.path.abspath("test/test.jpg")
        title, desc, timestamp = main.getInfoFromExifOrFilePath(image_path)
        self.assertEqual(title,"Apple, iPhone SE")
        self.assertEqual(desc, "#photo_gyazo #Apple #iPhone_SE  ")
        self.assertEqual(timestamp, 1583283648.0)

    def test_getInfoFromExifOrFilePathWithNoExif(self):
        image_path = os.path.abspath("test/test_with_noexif.jpeg")
        title, desc, timestamp = main.getInfoFromExifOrFilePath(image_path)
        self.assertEqual(title, None)
        self.assertEqual(desc, "#photo_gyazo #include_no_exif")
        self.assertEqual(timestamp, 1585889318)