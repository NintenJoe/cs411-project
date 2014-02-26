COMPILER = python
INTERPRETER = python
COMPILER_FLAGS = 
TEST_FLAGS = -m unittest

ASSET_DIR = ./assets
SRC_DIR = ./src
TEST_DIR = ./test
MAIN_SCRIPT = $(SRC_DIR)/server.py
SERVER_OPTS = 

.PHONY : server tests clean

all : server

server : $(MAIN_SCRIPT) $(wildcard $(SRC_DIR)/*.py)
	$(INTERPRETER) $(COMPILER_FLAGS) $(MAIN_SCRIPT) $(SERVER_OPTS)

tests : $(wildcard $(SRC_DIR)/*.py) $(wildcard $(TEST_DIR)/*.py)
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '*Test.py'

%Test : $(TEST_DIR)/%Test.py $(SRC_DIR)/%.py
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '$@.py'

clean :
	-rm -rf $(SRC_DIR)/*.pyc $(TEST_DIR)/*.pyc
