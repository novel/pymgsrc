#!/bin/sh

URL="freefall.freebsd.org:~/public_html/misc"
CHANGELOG="CHANGELOG"
SITE_TEMPLATE="site/pyimgsrc.tpl"
HTML_OUT="site/pyimgsrc.html"
VERSION=`grep version setup.py|sed  's|^[ ]*version[ ]*\=[ ]*"\(.*\)".|\1|'`

RELEASES_DATA=`sed 's|^[\ ]*\-[\ ]*\(.*\)$|<li>\1</li>|;s|^\([0-9]\.[0-9]\.[0-9]*.*\)|<h3>\1</h3><ul>|;s|^$|</ul>|' ${CHANGELOG}`

echo "Creating source distribution..."
python setup.py sdist > /dev/null 2>&1

DISTFILE="dist/pymgsrc-${VERSION}.tar.gz"

echo "Creating HTML page..."
sed -E "s|%%CHANGELOG%%|`echo ${RELEASES_DATA}`|;s|%%VERSION%%|${VERSION}|g" ${SITE_TEMPLATE} > ${HTML_OUT}

echo "Copying distfile and HTML page to ${URL}..."
scp ${DISTFILE} ${HTML_OUT} ${URL}

echo "Cleaning up..."

rm ${HTML_OUT}

echo "Done!"
