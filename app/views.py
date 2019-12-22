import os

from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Connection
from ftplib import FTP


def index(request):
    connections = Connection.objects.all()
    host = connections[0].host
    data = []
    path = '..'
    message = ""
    if request.method == "POST":
        action = request.POST.get("button")
        if action == "Створити":
            message = ""
            connection = Connection()
            connection.host = request.POST.get("create_host")
            connection.user = request.POST.get("create_user")
            connection.password = request.POST.get("create_password")
            connection.save()

        if action == "Видалити поточний хост":
            message = ""
            try:
                id = request.POST.get("select")
                connection = Connection.objects.get(id=id)
                connection.delete()
            except Connection.DoesNotExist:
                return HttpResponseNotFound("<h2>З'эднання не знайдено</h2>")

        if action == "Оновити":
            message = ""
            try:
                id = request.POST.get("select")
                connection = Connection.objects.get(id=id)
                connection.host = request.POST.get("edit_host")
                connection.user = request.POST.get("edit_user")
                connection.password = request.POST.get("edit_password")
                connection.save()
            except Connection.DoesNotExist:
                return HttpResponseNotFound("<h2>З'эднання не знайдено</h2>")

        if action == "Зв'язатися":
            message = ""
            try:
                id = request.POST.get("select")
                connection = Connection.objects.get(id=id)
                ftp = FTP(connection.host, connection.user, connection.password)
                data = ftp.nlst()
            except:
                return HttpResponseNotFound("<h2>З'эднання не знайдено</h2>")

        if action == "Перейти/Завантажити":
            id = request.POST.get("select")
            path_save = request.POST.get("path_save")
            filename = request.POST.get("filename")
            path = request.POST.get("path")
            initial_path = path
            if filename == '..':
                path = path.split('/')
                path.pop()
                path = '/'.join(path)
            else:
                path += '/' + filename
            connection = Connection.objects.get(id=id)
            ftp = FTP(connection.host, connection.user, connection.password)
            message = ""
            try:
                ftp.cwd(path)
                data = ftp.nlst()
            except:
                if path_save == '':
                    path_save = "C:\\"
                with open(path_save+filename, 'wb') as f:
                    ftp.retrbinary('RETR ' + path, f.write)
                path = initial_path
                ftp.cwd(path)
                data = ftp.nlst()
                message = "Файл було завантажено у "+path_save+filename

        if action == "Upload":
            upload_file_path = request.POST.get("uploadFile")
            print(upload_file_path)
            id = request.POST.get("select")
            path = request.POST.get("path")
            connection = Connection.objects.get(id=id)
            ftp = FTP(connection.host, connection.user, connection.password)
            message = ""
            try:
                ftp.cwd(path)
                dir, file = os.path.split(upload_file_path)
                ftp.storbinary('STOR '+file, open(upload_file_path, 'rb'))
                data = ftp.nlst()
            except:
                print("Error")

    return render(request, "index.html", context={"connections": connections, "path": path, "host": host, "data": data,
                                                  "message": message})
