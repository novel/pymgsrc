__author__ = "Roman Bogorodskiy (bogorodskiy@gmail.com)"
__revision__ = "$Rev: 6 $"

import hashlib
import httplib
import os.path
import xml.dom.minidom
import urllib2
from lib import post_multipart

HOST = "imgsrc.ru:80"
PROTO_VERSION = "0.8"
ENCODING = "cp1251"

class ImgSrc(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.md5passwd = hashlib.md5(password).hexdigest()

    def _get_text(self, element):
        text = []
        for node in element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text.append(node.data)
        return ''.join(text)

    def _parse_header(self, doc, check_store = False):
        info_element = doc.getElementsByTagName('info')[0]
        proto_version = info_element.getAttribute('proto')
                
        if proto_version != PROTO_VERSION:
            print """"Warning: written for proto version = %s, reported proto
version = %s, stuff might go wrong, poke the developers""" % (PROTO_VERSION, proto_version)
    
        status_element = doc.getElementsByTagName('status')[0]
        status = self._get_text(status_element)

        #print doc.toxml()
        if check_store is True:
            store_element = doc.getElementsByTagName('store')[0]
            store = self._get_text(store_element)

            self.store = store

        #print "status: ", status
        if status != "OK":
            raise Exception("status != ok")

    def get_store(self):
        """Similar to get_albums(), but returns store id for a user and doesn't
        parse albums info"""
        url = "/cli/info.php?login=%s&passwd=%s" % (self.username, self.md5passwd)

        pconn = httplib.HTTPConnection(HOST)
        pconn.request("GET", url, None, {})
        presponse = pconn.getresponse()

        data = presponse.read()
        doc = xml.dom.minidom.parseString(data)
    
        self._parse_header(doc, True)

        return self.store

    def get_albums(self):
        """Authentificates user and returns a list of albums"""
        url = "/cli/info.php?login=%s&passwd=%s" % (self.username, self.md5passwd)

        pconn = httplib.HTTPConnection(HOST)
        pconn.request("GET", url, None, {})
        presponse = pconn.getresponse()
        
        data = presponse.read()

        doc = xml.dom.minidom.parseString(data)

        self._parse_header(doc, True)
    
        albums = []
        album_nodes = doc.getElementsByTagName('album')

        for i in album_nodes:
            album = {}
            #album['id'] = i.getAttribute('id')
            id = i.getAttribute('id')

            for j in i.childNodes:
                if j.nodeType == j.ELEMENT_NODE:
                    album[j.nodeName] = self._get_text(j)

            #albums.append(album)
            albums.append(ImgSrcAlbum(id, self.store, (self.username, self.password), album))
        
        return albums

    def get_categories(self):
        url = "/cli/cats.php"

        pconn = httplib.HTTPConnection(HOST)
        pconn.request("GET", url, None, {})
        presponse = pconn.getresponse()

        data = presponse.read()

        doc = xml.dom.minidom.parseString(data)

        self._parse_header(doc)

        categories = []
        category_nodes = doc.getElementsByTagName('category')

        for i in category_nodes:
            category = {}
            category['id'] = i.getAttribute('id')

            for j in i.childNodes:
                if j.nodeType == j.ELEMENT_NODE:
                    category[j.nodeName] = self._get_text(j)

            categories.append(category)

        return categories

    def create_album(self, name, cat_id):
        url = \
          "/cli/info.php?login=%(login)s&passwd=%(passwd)s&create=%(name)s&create_category=%(cat_id)s" % \
          {'name': name.encode(ENCODING), 'cat_id': cat_id, 'login': self.username, 'passwd': self.md5passwd}

        pconn = httplib.HTTPConnection(HOST)
        pconn.request("GET", url, None, {})
        presponse = pconn.getresponse()

        data = presponse.read()

        doc = xml.dom.minidom.parseString(data)

        self._parse_header(doc)

        album_nodes = doc.getElementsByTagName('album')

        for i in album_nodes:
#           album = {}
#           id = i.getAttribute('id')
            for j in i.childNodes:
                if j.nodeType == j.ELEMENT_NODE:
                    if j.nodeName == "name":
                        if self._get_text(j) == name:
                            return i.getAttribute('id')
        
        # not reached
        return -1

class ImgSrcAlbum(object):
    photos = None
    modified = None
    name = None

    def __init__(self, id, store, cred, data = None):
        self.id = id
        self.store_id = store

        self.host = "e%s.%s" % (self.store_id, HOST)

        self.username = cred[0]
        self.md5passwd = hashlib.md5(cred[1]).hexdigest()

        if data is not None:
            #wtf?
            #for i in data.keys():
            #getattr(self, i) = data[i]
            self.photos = data['photos']
            self.modified = data['modified']
            self.name = data['name']

    def add_photo(self, url):
#       f = open(path)

        name = 'u1'
        #filename = os.path.basename(url)
        filename = url
        
        print url

        f = urllib2.urlopen(url)
        value = ''.join(f.readlines())

        url = "/cli/post.php?login=%(login)s&passwd=%(passwd)s&album_id=%(id)s" % {'id': self.id,
                'login': self.username,
                'passwd': self.md5passwd }

        # XXX will need to fix it in future, but now imgsrc seem to have only one store
        post_multipart("e0.imgsrc.ru:80", url, (), ((name, filename, value),))
