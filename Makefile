# ivoatex Makefile.  The ivoatex/README for the targets available.

# short name of your document (edit $DOCNAME.tex; would be like RegTAP)
DOCNAME = ivoatexDoc

# count up; you probably do not want to bother with versions <1.0
DOCVERSION = 1.3

# Publication date, ISO format; update manually for "releases"
DOCDATE = 2022-05-25

# What is it you're writing: NOTE, WD, PR, or REC
DOCTYPE = NOTE

# Source files for the TeX document (but the main file must always
# be called $(DOCNAME).tex
SOURCES = $(DOCNAME).tex svnsubstitution.tex verbatimstyles.tex gitmeta.tex \
          fields.xml fields-container.xml tapgen.tex schemadoc.tex

# List of pixel image files to be included in submitted package 
FIGURES = triangle_workflow.png

# List of PDF figures (for vector graphics)
VECTORFIGURES = 

AUX_FILES=custom.css

AUTHOR_EMAIL=msdemlei@ari.uni-heidelberg.de

-include ivoatex/Makefile

ivoatex/Makefile:
	@echo "*** ivoatex submodule not found.  Initialising submodules."
	@echo
	git submodule update --init

STILTS ?= stilts

# This test needs STILTS (http://www.starlink.ac.uk/stilts/)
test:
	$(STILTS) votlint votable=fields-container.xml

