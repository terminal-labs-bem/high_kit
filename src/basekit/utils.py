import os
import sys
import time
import json
import yaml
import shutil
import hashlib
import zipfile
import base64
import uuid
from pathlib import Path

from lightrunnercommon.config import tmp_dirs
from lightrunnercommon.readconfig import getconfig

def test():
    return getconfig()

def remove(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)

def create_dirs(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)

def init_runner_env():
    create_dirs(tmp_dirs)
    dir = '.tmp/runners/'
    if not os.path.exists(dir):
        os.mkdir(dir)

    dir = '.tmp/runners/runs'
    if not os.path.exists(dir):
        os.mkdir(dir)


import configparser
from pathlib import Path
from os.path import abspath, isfile, dirname, islink, isdir
from os import walk, symlink, listdir, path

config = configparser.ConfigParser()

package_link = ".tmp/symlink"
_setuppy = "/setup.py"
_setupcfg = "/setup.cfg"
_dsstore = ".DS_Store"
_repo = "repo"
_back = ".."
_blank = ""
_slash = "/"
_path = str(Path(__file__).parent.absolute())
_src = ""


def cwd():
    return path.join(dirname(__file__))


def join(*args):
    return abspath(path.join(*args))


def split(a):
    return a.split(_slash)


def backout(path):
    return join(path, _back)


def import_fun(mod, func):
    return getattr(__import__(mod, fromlist=[func]), func)


def get_pkg_dir():
    currentpath = cwd()
    i = len(currentpath.split(_slash))
    while i > 0:
        currentpath = join(currentpath, _back)
        if isfile(currentpath + _setuppy):
            return currentpath
            i = -1
        i = i - 1


def find_file(name, path):
    for root, dirs, files in walk(path):
        if name in files:
            return join(root, name)


def find_src_dir():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    build_new_path = False
    new_path = []
    for dir in currentpath:
        if dir == "src":
            build_new_path = True
        if build_new_path:
            new_path.append(dir)
    new_path.reverse()
    return "/".join(new_path)


def find_config_file():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    search = currentpath[:]
    for dir in currentpath:
        search.pop(0)
        candidate = search[:]
        candidate.reverse()
        if find_file("setup.cfg", "/".join(candidate)):
            return find_file("setup.cfg", "/".join(candidate))


def find_local_file():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    search = currentpath[:]
    for dir in currentpath:
        search.pop(0)
        candidate = search[:]
        candidate.reverse()
        if find_file("local.py", "/".join(candidate)):
            return find_file("local.py", "/".join(candidate))


def is_install_editable():
    if find_src_dir() == "":
        return False
    else:
        return True


def get_pkg_name():
    config.read(find_config_file())
    NAME = config["metadata"]["name"]
    return NAME


def setup_links(package_name):
    _link = package_link + _slash
    Path(_path + _slash + _link).mkdir(parents=True, exist_ok=True)
    if not islink(_path + _slash + _link + package_name):
        symlink(join(_path, _src), _path + _slash + _link + _slash + package_name)


def smart_reqs(repos, package_name):
    # styles = standalone, repo

    def _get_deploy_style():
        currentpath = _path
        for _ in range(len(split(currentpath))):
            currentpath = backout(currentpath)
            if isdir(currentpath + _slash + ".tmp" + _slash + _repo):
                return _repo

    if _get_deploy_style() == _repo:
        local_repos = listdir(join(_path, _back))
        if _dsstore in local_repos:
            local_repos.remove(_dsstore)
        if package_name in local_repos:
            local_repos.remove(package_name)
        for repo in local_repos:
            repos = [_ for _ in repos if not _.endswith(repo + ".git")]
        return repos
    return repos
