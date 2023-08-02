import os
import sys
from os import listdir
from os.path import isfile, join
import importlib
import importlib.util
import os
import shutil
import urllib
import subprocess
from urllib.request import urlopen
from os.path import isdir, dirname, realpath, abspath, join, exists
from zipfile import ZipFile
from configparser import ConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

from tempfile import mkstemp
from shutil import move
from os import remove


def _delete_dir(directory):
    directory = abspath(directory)
    if exists(directory):
        shutil.rmtree(directory)

def _copy_dir(source, target):
    if not exists(target):
        shutil.copytree(abspath(source), abspath(target))

def _rename_dir(source, target):
    os.rename(source, target)

def _fast_scandir_shallow(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    return subfolders

def _fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(_fast_scandir(dirname))
    return subfolders


def _fast_scandfiles(dirname):
    dirs = _fast_scandir(dirname)
    files = [f.path for f in os.scandir(dirname) if f.is_file()]
    for dir in dirs:
        files.extend([f.path for f in os.scandir(dir) if f.is_file()])
    return files

def _replace(source_file_path, pattern, substring):
    fh, target_file_path = mkstemp()
    with open(target_file_path, 'w') as target_file:
        with open(source_file_path, 'r') as source_file:
            for line in source_file:
                target_file.write(line.replace(pattern, substring))
    remove(source_file_path)
    move(target_file_path, source_file_path)