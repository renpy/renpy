tutorial.html: tutorial.xml preprocess.py stylesheet.xslt style.css
	python preprocess.py tutorial.xml > tutorial.hi.xml
	xsltproc stylesheet.xslt tutorial.hi.xml > tutorial.html
	cp tutorial.html style.css ~/ab/website/renpy/devel/doc