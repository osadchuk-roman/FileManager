from django.shortcuts import render
from django.http import HttpResponseNotFound

from app.server_operations import ServerOperations
from .models import Connection


def index(request):
    connections = Connection.objects.all()
    host = connections[0].host
    data = []
    path = '..'
    message = ""
    server_op = ServerOperations()
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
                server_op.connect(connection)
                data = server_op.get_files()
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
            server_op.connect(connection)
            message = ""
            try:
                server_op.load_directory(path)
                data = server_op.get_files()
            except:
                if path_save == '':
                    path_save = "C:\\"
                server_op.download_file(path, path_save, filename)
                path = initial_path
                server_op.load_directory(path)
                data = server_op.get_files()
                message = "Файл було завантажено у " + path_save + filename

        if action == "Upload":
            upload_file_path = request.POST.get("uploadFile")
            print(upload_file_path)
            id = request.POST.get("select")
            path = request.POST.get("path")
            connection = Connection.objects.get(id=id)
            server_op.connect(connection)
            message = ""
            try:
                server_op.load_directory(path)
                server_op.upload_file(upload_file_path)
                data = server_op.get_files()
            except:
                print("Error")

    return render(request, "index.html", context={"connections": connections, "path": path, "host": host, "data": data,
                                                  "message": message})
