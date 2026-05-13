PREFIX ?= /usr/local
WFLAGS ?= -Wall -Wextra -Wmissing-prototypes -Wdiv-by-zero -Wbad-function-cast -Wcast-align -Wcast-qual -Wfloat-equal -Wmissing-declarations -Wnested-externs -Wno-unknown-pragmas -Wpointer-arith -Wredundant-decls -Wstrict-prototypes -Wswitch-enum -Wno-type-limits
CFLAGS ?= -Os -mtune=native -fno-exceptions $(WFLAGS)
CFLAGS += -I.
OBJ = hydrogen.o
AR ?= ar
RANLIB ?= ranlib

SRC = \
	hydrogen.c \
	hydrogen.h \
	impl/common.h \
	impl/core.h \
	impl/gimli-core.h \
	impl/hash.h \
	impl/hydrogen_p.h \
	impl/kdf.h \
	impl/kx.h \
	impl/pwhash.h \
	impl/random.h \
	impl/secretbox.h \
	impl/sign.h \
	impl/x25519.h

all: lib test

lib: libhydrogen.a

install: lib
	mkdir -p $(PREFIX)/lib
	install -o 0 -g 0 -m 0755 libhydrogen.a $(PREFIX)/lib 2> /dev/null || install -m 0755 libhydrogen.a $(PREFIX)/lib
	mkdir -p $(PREFIX)/include
	install -o 0 -g 0 -m 0644 hydrogen.h $(PREFIX)/include 2> /dev/null || install -m 0644 hydrogen.h $(PREFIX)/include
	ldconfig 2> /dev/null || true

uninstall:
	rm -f $(PREFIX)/lib/libhydrogen.a
	rm -f $(PREFIX)/include/hydrogen.h

test: tests/tests
	rm -f tests/tests.done
	tests/tests && touch tests/tests.done

tests/tests: $(SRC) tests/tests.c
	$(CC) $(CFLAGS) -O3 -o tests/tests hydrogen.c tests/tests.c

$(OBJ): $(SRC)

libhydrogen.a: $(OBJ)
	$(AR) -r $@ $^
	$(RANLIB) $@

.PHONY: clean

clean:
	rm -f libhydrogen.a $(OBJ)
	rm -f tests/tests tests/*.done

check: test

distclean: clean
