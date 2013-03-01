import socket
import urllib

def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com",80))
    return s.getsockname()[0]

def download(file_url, destination_file):
    urllib.urlretrieve (file_url, destination_file)