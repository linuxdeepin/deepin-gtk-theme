PREFIX = /usr

all: 

install: 
	mkdir -p $(DESTDIR)$(PREFIX)/share/themes
	cp -r Deepin $(DESTDIR)$(PREFIX)/share/themes/
