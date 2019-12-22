import os
from ftplib import FTP

from app.models import Connection


class ServerOperations:
    connection: Connection
    ftp: FTP

    def connect(self, connection):
        self.connection = connection
        self.ftp = FTP(self.connection.host, self.connection.user, self.connection.password)

    def get_files(self):
        return self.ftp.nlst()

    def load_directory(self, path):
        self.ftp.cwd(path)

    def download_file(self, path, path_save, filename):
        with open(path_save + filename, 'wb') as f:
            self.ftp.retrbinary('RETR ' + path, f.write)

    def upload_file(self, upload_file_path):
        dir, file = os.path.split(upload_file_path)
        self.ftp.storbinary('STOR ' + file, open(upload_file_path, 'rb'))
