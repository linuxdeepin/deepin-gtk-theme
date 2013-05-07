all: gtk3

gtk3: test_gtk3.c
	gcc $^ `pkg-config --libs --cflags gtk+-3.0` -o test_gtk3
