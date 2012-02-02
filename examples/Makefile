# Build all examples at once.
# You can also build them one by one from here:
# % make EX=example2
#
# But you can also just enter a directory
# read the README and type "make"

SHELL = /bin/sh

# list of buildable examples
EX = basic_example example1 example2 example3 example4 example5 inherit bytebuffer \
bug_no_param_int_array bug_disable_return


# verify that JAVA_HOME is set to something (should be the bare minimum)
ifndef JAVA_HOME
    $(error ERROR: Variable JAVA_HOME is not set!)
endif


all:	build
clean:	$(patsubst %,%.clean,$(EX))

# run build and print the help message at the end
build: $(patsubst %,%.build,$(EX))
	@echo ""
	@echo "==========================================================================="
	@echo "Dont forget to set library path before running the example:"
	@echo "# export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):$(JAVA_HOME)/jre/lib/i386:$(JAVA_HOME)/jre/lib/i386/client/"
	@echo "or"
	@echo "# export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):$(JAVA_HOME)/jre/lib/amd64:$(JAVA_HOME)/jre/lib/amd64/server/"
	@echo "==========================================================================="


# build selected examples
%.build:
	$(MAKE) -C $(patsubst %.build,%,$@)


# clean selected examples
%.clean:
	$(MAKE) -C $(patsubst %.clean,%,$@) clean
