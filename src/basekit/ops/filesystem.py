import os
import sys
from pathlib import Path
from shutil import copyfile, move, rmtree

def is_writable(path):
    try:
        testfile = tempfile.TemporaryFile(dir = path)
        testfile.close()
    except OSError as e:
        if e.errno == errno.EACCES:  # 13
            return False
        e.filename = path
        raise
    return True

def dir_exists(path):
    return os.path.isdir(path)

def dir_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

def dir_delete(path):
    try:
        rmtree(path)
    except FileNotFoundError:
        pass

def file_delete(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

def file_copy(src, dst):
    copyfile(src, dst)

def file_rename(src, dst):
    os.rename(src, dst)

def file_move(src, dst):
    move(src, dst)