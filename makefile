PYTHON := $(shell (command -v python3 >/dev/null 2>&1 && echo python3) || \
                 (command -v python >/dev/null 2>&1 && echo python) || \
                 (echo ""))

ifeq ($(PYTHON),)
$(error No Python interpreter found (python3 or python))
endif

PROGRAMS := decompile compile
EXECUTABLES := nd nco

.PHONY: install

install:
	@$(PYTHON) -m pip install -r requirements.txt --break-system-packages
	@$(foreach i,1 2, echo "$(PYTHON) $(CURDIR)/$(word $(i),$(PROGRAMS))/main.py \$$@" > ~/bin/$(word $(i),$(EXECUTABLES)) && chmod +x ~/bin/$(word $(i),$(EXECUTABLES));)
	@echo "\nMake sure that ~/bin is in your path"
