SHELL = /bin/sh

# help message by default
all:
	@echo "make: available targets: examples clean deepclean"
	@echo "      - examples: build examples/ folder"
	@echo "      - clean: clean the examples folder and remove .pyc files"


# build examples/
.PHONY: examples
examples:
	$(MAKE) -C examples build


# clean examples/ folder
clean: cleanpyc cleanexamples


# clean examples folder
cleanexamples:
	$(MAKE) -C examples clean


# clean .pyc
cleanpyc:
	@echo "Cleaning *.pyc files..."
	@find . -type f -name "*.pyc" | xargs rm -f

