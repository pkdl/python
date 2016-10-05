#!/usr/bin/python
import os
import stat
import sys
import hashlib
from collections import defaultdict

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_dir(dir):
    files = defaultdict(list)

    for dirname, dirnames, filenames in os.walk(dir):

        for filename in filenames:
            if not(filename[:1] in '~.'):
                fullname = os.path.join(dirname, filename)
                if not os.path.islink(fullname): #check if file a symlink
                    if not stat.S_ISSOCK(os.stat(fullname).st_mode): #check if file a socket
                        files[md5(fullname)].append(os.path.relpath(fullname, dir))
    return files

def print_equal(dict):
    for hash in dict:
        if len(files[hash]) > 1:
            print(":".join(files[hash]))


files = scan_dir(sys.argv[1])
print_equal(files)

