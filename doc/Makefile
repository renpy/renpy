all:: tutorial.html example.html

tutorial.html: tutorial.xml preprocess.py stylesheet.xslt style.css styles.xml
	python preprocess.py tutorial.xml > tutorial.hi.xml
	xsltproc stylesheet.xslt tutorial.hi.xml > tutorial.html
	cp tutorial.html style.css ~/ab/website/renpy/devel/doc


example.html: example.xml preprocess.py stylesheet.xslt style.css styles.xml ../demo2/script.rpy
	python preprocess.py example.xml > example.hi.xml
	xsltproc stylesheet.xslt example.hi.xml > example.html
	cp example.html style.css ~/ab/website/renpy/devel/doc