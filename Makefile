INSTALL_PREFIX=/usr/local
BIN_INSTALL_PREFIX=$(INSTALL_PREFIX)/bin

# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
        $(error Undefined $1$(if $2, ($2))$(if $(value @), \
                required by target `$@\')))

all: build install

build: svgen twopaco k8

k8:
	cd k8 && wget -O- https://github.com/attractivechaos/k8/releases/download/v0.2.1/v8-3.16.4.tar.bz2 | tar jxf -
	cd k8/v8-3.16.4 && $(MAKE) x64.release snapshot=off
	cd k8/v8-3.16.4 && $(CXX) -O2 -Wall -o k8 -Iinclude ../k8.cc -lpthread -lz `find out -name "libv8_base.a"` `find out -name "libv8_snapshot.a"`

svgen:
	$(MAKE) -C SVGen

install-svgen:
	$(MAKE) -C SVGen install
	install -m 0755 Simulation/generate_sequences.sh $(BIN_INSTALL_PREFIX)/svgen_generate_sequences
	install -m 0755 Simulation/assemble.sh $(BIN_INSTALL_PREFIX)/svgen_assemble

twopaco:
	cd TwoPaCo mkdir build && cd build && \
	cmake ../src && \
	$(MAKE)

clean:
	git clean -f .

update-repo:
	git reset --hard
	git pull origin master

install: install-svgen install-grc install-gfa install-vg install-webs

install-grc:
	install -m 0755 grc/grc2gfa $(BIN_INSTALL_PREFIX)

install-gfa:
	install -m 0755 gfautils/gfa2dot $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfa2json $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfa2svg $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfatools $(BIN_INSTALL_PREFIX)

install-vg:
	install -m 0755 gfautils/vg2svg $(BIN_INSTALL_PREFIX)

install-k8:
	install -m 0755 k8/k8 $(BIN_INSTALL_PREFIX)

install-webs:
	@:$(call check_defined, SRV_INSTALL_PREFIX, web component install directory)
	cp -R html/* $(SRV_INSTALL_PREFIX)
	install sequenceTubeMap/app/scripts/tubemap.js $(SRV_INSTALL_PREFIX)/scripts


.PHONY: k8 install install-grc install-gfa install-vg install-k8
