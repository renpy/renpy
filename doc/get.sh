#!/bin/sh

wget http://www.renpy.org/w/skins/common/shared.css -O shared.css
wget http://www.renpy.org/w/skins/monobook/main.css -O monobook.css
wget 'http://www.renpy.org/w/index.php?title=MediaWiki:Common.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=18000' -O common.css
wget 'http://www.renpy.org/w/index.php?title=MediaWiki:Monobook.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=18000' -O monobook2.css

rm -Rf www.renpy.org
wget -e robots=off -m -I /wiki/renpy/doc/reference/,/wiki/renpy/doc/tutorials/,/w/images -m http://www.renpy.org/wiki/renpy/doc/index

rm -Rf images
mkdir -p images
cp `find www.renpy.org -name \*.png -type f` images

# No jpgs yet.
# cp `find www.renpy.org -name \*.jpg -type f` images

rm -Rf reference tutorials
python2.5 process.py
