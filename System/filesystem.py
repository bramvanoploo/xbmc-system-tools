import os
import shutil
import log
from inspect import stack

def create_backup_file(file_path):
    shutil.copy(file_path, file_path+ ".backup")

def restore_backup_file(file_path):
    if os.path.isFile(file_path+ ".backup"):
        delete_file(file_path)
        shutil.copy(file_path+ ".backup", file_path)
        return True
    return False

def delete(path):
    if os.path.exists(path.strip()):
        try:
            os.remove(path.strip())
            return True
        except:
            pass
    return False

def delete_file(file_path):
    if os.path.isfile(file_path.strip()):
        try:
            os.remove(file_path.strip())
            return True
        except:
            pass
    return False

def delete_directory(directory_path):
    if os.path.isdir(directory_path.strip()):
        try:
            shutil.rmtree(directory_path.strip())
            return True
        except:
            pass
    return False

def create_file(file_path, backup_existing = True, delete_existing = False):
    if delete_existing:
        delete_file(file_path)
    if backup_existing:
        backupFile(file_path)
    open(file_path, 'w').close()
    return True

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False

def get_directory_size(start_path):
    if not os.path.isdir(start_path.strip()):
        return False
    totalSize = 0
    for dir_path, dir_names, file_names in os.walk(start_path.strip()):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            totalSize += os.path.getsize(fp)
    return totalSize

def append_to_file(file_path, content):
    if os.path.isFile(file_path):
        backupFile(file_path)
    else:
        create_file(file_path)
    with open(file_path, "a") as file:
        file.write(content)
        return True
    return False

def move(source, destination):
    shutil.move(source, destination)
    
def get_users():
    return [name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) and not name.startswith('.')]