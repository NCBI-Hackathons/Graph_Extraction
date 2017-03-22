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

build: svgen twopaco

svgen:
	$(MAKE) -C SVGen

install-svgen:
	$(MAKE) -C SVGen install
	install -m 0755 Simulation/generate_reads.sh $(BIN_INSTALL_PREFIX)

twopaco:
	cd TwoPaCo mkdir build && cd build && \
	cmake ../src && \
	$(MAKE)

clean:
	git clean -f .

update-repo:
	git reset --hard
	git pull origin master

install: install-svgen install-mfa install-gfa install-vg install-webs

install-mfa:
	install -m 0755 grc/grc2mfa $(BIN_INSTALL_PREFIX)

install-gfa:
	install -m 0755 gfautils/gfa2dot $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfa2json $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfa2svg $(BIN_INSTALL_PREFIX)
	install -m 0755 gfautils/gfatools $(BIN_INSTALL_PREFIX)

install-vg:
	install -m 0755 gfautils/vg2svg $(BIN_INSTALL_PREFIX)

install-webs:
	@:$(call check_defined, SRV_INSTALL_PREFIX, web component install directory)
	cp -R html/* $(SRV_INSTALL_PREFIX)


.PHONY: install install-mfa install-gfa install-vg
