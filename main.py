# coding:utf-8
import os
import json
import platform
import requests

def uploadGyazo(file_name, imagedata, content_type, title, url, desc, timestamp):
    """
    画像のバイナリと各種メタデータを指定してGyazoへのアップロードを実行するメソッド
     
    Args:
        file_name (str): 画像のファイル名
        imagedata (binary): 画像のバイナリ
        content_type (str): 画像の mime content type
        title (str): 画像を取得したウェブサイトのタイトル
        url (str): 画像を取得したウェブサイトのURL
        desc (str): Gyazo の Description 欄に記入されるメモ
        timestamp (int): 画像の最終変更日時
    """
    # Device IDを取得する
    appdata_path = None
    appdata_filename = None
    if 'Darwin' in platform.system():
        appdata_path = os.path.expanduser('~/Library/Gyazo/')
        appdata_filename = 'id'
    elif 'Windows' in platform.system() or 'CYGWIN' in platform.system():
        appdata_path = os.getenv('APPDATA') + '\\Gyazo\\'
        appdata_filename = 'id.txt'
    elif 'Linux' in platform.system():
        appdata_path = os.path.expanduser('~/')
        appdata_filename = '.gyazo.id'
    with open(('%s%s' % (appdata_path, appdata_filename)), 'r') as device_id_file:
        device_id = device_id_file.read()

    # Gyazoにアップロードするための multipart/form-data をつくる
    # filedata
    files = {'imagedata': (file_name, imagedata, content_type)}

    # metadata
    metadata = {
        'app': "photo-gyazo",
        'title': title,
        'url': url,
        'desc': desc
    }

    # formdata
    formdata = {
        'id': device_id,
        'scale': "1.0",
        'created_at': timestamp,
        'metadata': json.dumps(metadata)
    }
    print(formdata)
    gyazo_res = requests.post("https://upload.gyazo.com/upload.cgi", data=formdata, files=files)
    print(gyazo_res)
    print(gyazo_res.text)

def getInfoFromFilePath(image_path):
    title = None
    desc = "#photo_gyazo #include_no_exif"
    datefloat = os.stat(image_path).st_ctime
    datetimeobj = datetime.datetime.fromtimestamp(datefloat)
    timestamp = int(datetimeobj.timestamp())
    return title, desc, timestamp

def getInfoFromExif(exif):
    exif_table = {}
    for tag_id, value in exif.items():
        tag_key = TAGS.get(tag_id, tag_id)
        exif_table[tag_key] = value
    datetimestr = exif_table.get("DateTimeOriginal")
    print(datetimestr)
    if datetimestr is not None:
        if "MakerNote" in exif_table:
            exif_table.pop("MakerNote")
        datetimeobj = None
        try:
            datetimeobj = datetime.datetime.strptime(datetimestr, '%Y:%m:%d %H:%M:%S')
        except ValueError:
            return
        maker = exif_table.get("Make", "")
        model = exif_table.get("Model", "")
        gpsinfo = exif_table.get("GPSInfo")
        lonstr = ""
        latstr = ""
        try:
            lon = int(gpsinfo[4][0][0]) +\
                float(gpsinfo[4][1][0]) /60 +\
                (float(gpsinfo[4][2][0])/float(gpsinfo[4][2][1])) /3600
            lonstr = "#lon_"+str(lon)
            lat = int(gpsinfo[2][0][0]) +\
                float(gpsinfo[2][1][0]) /60 +\
                (float(gpsinfo[2][2][0])/float(gpsinfo[2][2][1])) /3600
            latstr = "#lat_"+str(lat)
        except TypeError:
            pass
        except KeyError:
            pass
        timestamp = datetimeobj.timestamp()
        title = u"{}, {}".format(maker, model)
        desc = u"#photo_gyazo {} {} {} {}".format(
            "#"+maker.replace(" ", "_"),
            "#"+model.replace(" ", "_"),
            lonstr,
            latstr)
    return title, desc, timestamp

def getInfoFromExifOrFilePath(image_path):
    exif = None
    try:
        image = Image.open(image_path)
        try:
            exif = image._getexif()
        except AttributeError:
            exif = None
    except IOError:
        return
    title, desc, timestamp = getInfoFromFilePath(image_path)
    if exif is not None:
        title, desc, timestamp = getInfoFromExif(exif)
    return title, desc, timestamp

import io
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
def uploadPhotoFile(dir_path, file_path):
    image_path = os.path.join(dir_path, file_path)
    file_name = os.path.basename(file_path)
    file_format = "JPEG"
    if (image_path.endswith("png")):
        file_format = "PNG"
    elif not (image_path.endswith("jpeg") or image_path.endswith("jpg")):
        return
    print(image_path)

    title, desc, timestamp = getInfoFromExifOrFilePath(image_path)

    output = io.BytesIO()
    image.save(output, file_format)
    uploadGyazo(file_name, output.getvalue(), "image/jpeg", title, None, desc, timestamp)
    

def uploadPhotoFileFromDir(dir_path, recursive):
    dir_path = os.path.abspath(dir_path)
    file_and_dir = os.listdir(dir_path)
    for file_or_dir in file_and_dir:
        isFile = os.path.isfile(os.path.join(dir_path, file_or_dir))
        if isFile:
            uploadPhotoFile(dir_path, file_or_dir)
        else:
            if recursive:
                uploadPhotoFileFromDir(os.path.join(dir_path, file_or_dir), recursive)


import sys
targetMethod = None
optionalArg = False
if __name__ == "__main__":
    if (len(sys.argv) == 1):
        print("python main.py dir_path recursive")
    if (len(sys.argv) >= 2):
        targetDir = sys.argv[1]
    if (len(sys.argv) >= 3):
        optionalArg = sys.argv[2]
    uploadPhotoFileFromDir(targetDir, optionalArg)
