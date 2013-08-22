#!/usr/bin/python

import os, sys, time, subprocess, re

# recursive list all items by given directory
def traversal_by_ext(dir, ext):
    rc = []
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            path = path.replace(dir, '.')
            file, extension = os.path.splitext(path)
            if extension.upper() == ext.upper(): rc.append(path)
    return rc

def rmdir(d):
    subprocess.call(['rm', '-rf', d])


def mkdir(d):
    subprocess.call(['mkdir', '-p', d])


def mvdir(d, x):
    subprocess.call(['mv', d, x])

def tok():
    tok = '/'
    return tok


def compose(args):
    rc = ""
    for arg in args:
        rc += arg+tok()
    return rc[:-1]


def filesplit(file):
    return file.rsplit(tok(), 1)


def create_newpath(path, suffix):
    if path[-1] == tok(): path = path[:-1]
    return "%s_%s_%s%s" % (path, suffix, time.strftime('%Y%m%d_%H%M%S'), tok())


def load_languages(path):
    langf = open("languages1.cfg")
    rc = langf.readlines()
    items = []
    empty = re.compile(" ")
    ret = re.compile("\n")
    for l in rc:
        l = empty.sub("",l)
        l = ret.sub("",l)
        if l.startswith('.') : continue
        if '#' in l : continue
        if l == '' : continue
        items.append(l)
    langf.close()
    return items

def load_packages(path):
    langf = open("packages1.cfg")
    rc = langf.readlines()
    items = []
    empty = re.compile(" ")
    ret = re.compile("\n")
    for l in rc:
        l = empty.sub("",l)
        l = ret.sub("",l)
        if l.startswith('.') : continue
        if '#' in l : continue
        if l == '' : continue
        items.append(l)
    langf.close()
    return items

def find_min(display):
    min = 99999
    rc = None
    for d in display:
        if d[0] < min:
            min = d[0]
            rc = d
    return rc



if __name__ == '__main__' :

    print '#'*80
    print 'test traversal()'
    for item in traversal('.') : print item

    print '#'*80
    print 'test traversal_by_ext()'
    for item in traversal_by_ext('.', '.png') : print item
