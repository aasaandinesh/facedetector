import os

import requests

rootdir = "/Users/dineshsingh/Downloads/profiles_filtered"


def upload_face_pics():
    folders = []
    counter = 0
    for subdir, dirs, files in os.walk(rootdir):
        if(len(files)) > 0 and len(subdir.split('/')) == 6:
            counter += 1
            file = subdir + '/' + files[0]
            faces = {'file': (file, open(file, 'rb'))}
            url = "http://localhost:8080/facebox/teach?name={0}&id={0}".format(subdir.split('/')[5])
            # url = "http://localhost:8080/facebox/teach/{0}".format(subdir.split('/')[5])
            # print(file)
            print(url)
            # r = requests.delete(url)
            r = requests.post(url, files=faces )
            print(r.reason)

    print(counter)


if __name__ == '__main__':
    upload_face_pics()