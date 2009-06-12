#!/usr/bin/env python

__author__ = "Roman Bogorodskiy (bogorodskiy@gmail.com)"
__revision__ = "$Rev: 6 $"

VERSION = "0.1.2 'AD/HD ??'"

import os.path
import sys
import urlparse
import urllib
from imgsrc.ImgSrc import ImgSrc,ImgSrcAlbum

CONFIG = "~/.imgsrc"
username = password = None

def usage():

    print """Usage: %(script)s cmd cmd_arg1 cmd_arg2 ... cmd_argN

Type '%(script)s help' for help.
""" % {'script': sys.argv[0]}
    sys.exit(0)

def version(args):
    print """imgsrc.py %s

Roman Bogorodskiy <bogorodskiy@gmail.com>""" % VERSION

def help(args):
    print """imgsrc.py

Commands:

    version - show version info
    help    - show this message
    lsalb   - list albums
    lscat   - list categories
    cralb <name> <cat_id> - create a new album
    addphoto <alb_id> <path1> <path2> ... <pathN> - adds photos to album with <alb_id> id
"""

def read_account_data():

    config = os.path.expanduser(CONFIG)
    
    if os.path.isfile(config) is False:
        sys.stderr.write("""%s does not exist!\nTo create it, type:\n
echo user:pass > %s\n\nWhere 'user' and 'pass' is your username and password at imgsrc.ru\n""" % (config, config))
        sys.exit(0)

    data = open(config).readline().strip().split(':')
    username = data[0]
    password = data[1]
    # XXX exceptions... laaazy

    #print username, password
    #sys.exit(0)
    return username, password

def list_albums(args):
    imgsrc = ImgSrc(username, password)

    albums = imgsrc.get_albums()

    for i in albums:
        #print i.name
        if i.photos and i.modified and i.name:
            print "%s : %s (%s; %s)" % (i.id, i.name, i.photos, i.modified)
        else:
            print "%s : <no data>" % (i.id)

def list_categories(args):
    imgsrc = ImgSrc(username, password)

    categories = imgsrc.get_categories()

    for i in categories:
        if int(i['parent_id']) == 0:
            print "+ %s : %s" % (i['id'], i['name'])
            for j in categories:
                if int(j['parent_id']) == int(i['id']):
                    print "  + %s : %s" % (j['id'], j['name'])

def create_album(args):
    if len(args) != 2:
        usage()

    imgsrc = ImgSrc(username, password)
    
    name = unicode(args[0], sys.stdin.encoding)
    cat_id = args[1]

    album_id = imgsrc.create_album(name, cat_id)
    print "New album created, id = %s" % album_id

def add_photo(args):
    if len(args) < 2:
        usage()

    album_id = args[0]
    files = args[1:]

    imgsrc = ImgSrc(username, password)
    store_id = imgsrc.get_store()

    album = ImgSrcAlbum(album_id, store_id, (username, password))

    for file in files:
        if urlparse.urlparse(file)[0] == '':
            url = ''.join(["file://", urllib.pathname2url(os.path.abspath(file))])
        else:
            url = file
        album.add_photo(url)

        print "Image '%s' uploaded!" % url

actions = {'version': version,
        'help': help,
        'lsalb': list_albums,
        'lscat': list_categories,
        'cralb': create_album,
        'addphoto': add_photo}

if __name__ == "__main__":
    username, password = read_account_data()

    if len(sys.argv) < 2:
        usage()

    command = sys.argv[1]

    if command not in actions:
        usage()
    else:
        actions[command](sys.argv[2:])
