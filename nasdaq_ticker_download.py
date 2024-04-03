import os
import ftplib


def download_files(file_names, target_path):
    ftp_server = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp_server.login()
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('Symboldirectory')
    ftp_server.dir()

    for filename in file_names:
        file_path = os.path.join(target_path, filename)
        with open(file_path, "wb") as file:
            ftp_server.retrbinary(f"RETR {filename}", file.write)
    ftp_server.quit()