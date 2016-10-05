#!/usr/bin/python
import os
import stat
import sys
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

files = {}

for dirname, dirnames, filenames in os.walk(sys.argv[1]):

    for filename in filenames:
        if not os.path.islink(os.path.join(dirname, filename)): #check if file a symlink
            if not stat.S_ISSOCK(os.stat(os.path.join(dirname, filename)).st_mode): #check if file a socket
                files[md5(os.path.join(dirname, filename))] = files.get( md5(os.path.join(dirname, filename)), '') + os.path.join(dirname, filename) + ':'

for hash in files:
    if files[hash].count(':') > 1:
        print(files[hash][:-1])
