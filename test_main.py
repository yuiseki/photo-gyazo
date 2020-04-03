import unittest
import os
import main
from PIL import Image

class MainTest(unittest.TestCase):
    def test_getInfoFromFilePath(self):
        image_path = os.path.abspath("test/test_with_exif.jpg")
        title, desc, timestamp = main.getInfoFromFilePath(image_path)
        self.assertEqual(title, None)
        self.assertEqual(desc, "#photo_gyazo #include_no_exif")
        self.assertEqual(timestamp, 1585900168)
    
    def test_getInfoFromExif(self):
        image_path = os.path.abspath("test/test_with_exif.jpg")
        image = Image.open(image_path)
        exif = image._getexif()
        title, desc, timestamp = main.getInfoFromExif(exif)
        print(title, desc ,timestamp)
        self.assertEqual(title, "Apple, iPhone SE")
        self.assertEqual(desc, "#photo_gyazo #Apple #iPhone_SE  ")
        self.assertEqual(timestamp, 1583283648.0)
    
    def test_getInfoFromExifOrFilePath(self):
        image_path = os.path.abspath("test/test_with_exif.jpg")
        title, desc, timestamp = main.getInfoFromExifOrFilePath(image_path)
        self.assertEqual(title,"Apple, iPhone SE")
        self.assertEqual(desc, "#photo_gyazo #Apple #iPhone_SE  ")
        self.assertEqual(timestamp, 1583283648.0)

    def test_getInfoFromExifOrFilePath(self):
        image_path = os.path.abspath("test/test_without_exif.jpeg")
        title, desc, timestamp = main.getInfoFromExifOrFilePath(image_path)
        self.assertEqual(title, None)
        self.assertEqual(desc, "#photo_gyazo #include_no_exif")
        self.assertEqual(timestamp, 1585900154)


    def test_checkFileFormat(self):
        image_path = os.path.abspath("test/test_with_exif.jpg")
        newer_file_format = main.checkFileFormat(image_path)
        if (image_path.endswith("jpg") or image_path.endswith("jpeg")):
            self.assertEqual(newer_file_format, "JPEG")
        elif(image_path.endswith("png")):
            self.assertEqual(newer_file_format, "PNG")
        else:
            print("not a image file")