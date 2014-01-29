UI_SOURCES=$(wildcard ui/*.ui)
UI_FILES=$(patsubst %.ui,%_ui.py,$(UI_SOURCES))

RC_SOURCES=$(wildcard *.qrc)
RC_FILES=$(patsubst %.qrc,%_rc.py,$(RC_SOURCES))

GEN_FILES = ${UI_FILES} ${RC_FILES}

all: $(GEN_FILES)
ui: $(UI_FILES)
resources: $(RC_FILES)

$(UI_FILES): %_ui.py: %.ui
	pyuic4 -o $@ $<
	
$(RC_FILES): %_rc.py: %.qrc
	pyrcc4 -o $@ $<


clean:
	rm -f $(GEN_FILES) *.pyc


PLUGIN_DIR=$(CURDIR) 
PLUGIN_NAME=`basename $(CURDIR)`
PLUGIN_ZIP_NAME = 'pstimeseries'

package:
	make all && cd .. && mv $(PLUGIN_NAME) $(PLUGIN_ZIP_NAME) && rm -f $(PLUGIN_NAME).zip && zip -r $(PLUGIN_ZIP_NAME).zip $(PLUGIN_ZIP_NAME) -x \*testdata\* -x \*.svn* -x \*.pyc -x \*~ -x \*entries\* -x \*.git\* -x \*.skip\* && mv $(PLUGIN_ZIP_NAME) $(PLUGIN_NAME) && cd $(PLUGIN_NAME)

