all:: reference.html example.html

reference.html: reference.xml paragraph.py preprocess.py stylesheet.xslt style.css styles.xml
	python paragraph.py < reference.xml > reference.par.xml
	python preprocess.py reference.par.xml > reference.hi.xml
	xsltproc stylesheet.xslt reference.hi.xml > reference.html
	cp reference.html style.css ~/ab/website/renpy/devel/doc


example.html: example.xml preprocess.py stylesheet.xslt style.css styles.xml ../demo2/script.rpy
	python preprocess.py example.xml > example.hi.xml
	xsltproc stylesheet.xslt example.hi.xml > example.html
	cp example.html style.css ~/ab/website/renpy/devel/doc