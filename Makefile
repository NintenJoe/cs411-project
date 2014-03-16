ifdef COMPILER
ifndef INTERPRETER
INTERPRETER = $(COMPILER)
endif
else ifdef INTERPRETER
COMPILER = $(INTERPRETER)
else
COMPILER = python2.7
INTERPRETER = python2.7
endif
COMPILER_FLAGS = 
TEST_FLAGS = -m unittest

PROJECT_ROOT = .
PACKAGE_ROOT = $(PROJECT_ROOT)/datbigcuke
ASSET_DIR = $(PROJECT_ROOT)/assets
BIN_DIR = $(PROJECT_ROOT)/bin
TEST_DIR = $(PACKAGE_ROOT)/test
CONFIG_DIR = $(PROJECT_ROOT)/config
MAIN_SCRIPT = $(BIN_DIR)/datbigcuke-server
SERVER_OPTS = --config=$(CONFIG_DIR)/server.conf

.PHONY : server tests test clean

all : server

server : $(MAIN_SCRIPT)
	$(MAIN_SCRIPT) $(SERVER_OPTS)

test : tests
tests :
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(PROJECT_ROOT) -p '*Test.py'

%Test : $(TEST_DIR)/%Test.py $(PACKAGE_ROOT)/%.py
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(PROJECT_ROOT) -p '$@.py'

clean :
	-find "$(PROJECT_ROOT)" -name '*.pyc' | xargs rm -f
	-find "$(PROJECT_ROOT)" -name __pycache__ | xargs rm -rf
