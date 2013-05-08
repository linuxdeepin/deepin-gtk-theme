all: gtk3 nautilus

gtk3: test_gtk3.c
	gcc $^ `pkg-config --libs --cflags gtk+-3.0` -o test_gtk3

nautilus: test_application.c
	gcc $^ `pkg-config --libs --cflags gtk+-3.0` -o test_$@ -DAPP_NAME=\"$@\"
