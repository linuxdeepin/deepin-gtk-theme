PREFIX= /usr

all:

install:
	mkdir -pv  $(DESTDIR)$(PREFIX)/share/themes/Deepin
	cp -r Deepin/*  $(DESTDIR)$(PREFIX)/share/themes/Deepin


