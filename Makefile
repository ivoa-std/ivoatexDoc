# ivoatex Makefile.  The ivoatex/README for the targets available.

# short name of your document (edit $DOCNAME.tex; would be like RegTAP)
DOCNAME = ivoatexDoc

# count up; you probably do not want to bother with versions <1.0
DOCVERSION = 1.6

# Publication date, ISO format; update manually for "releases"
DOCDATE = 2025-11-16

# What is it you're writing: NOTE, WD, PR, or REC
DOCTYPE = NOTE

# Source files for the TeX document (but the main file must always
# be called $(DOCNAME).tex
SOURCES = $(DOCNAME).tex verbatimstyles.tex gitmeta.tex \
          fields.xml fields-container.xml tapgen.tex \
          schemadoc-example.tex vocterms-example.tex

# List of pixel image files to be included in submitted package
FIGURES = triangle_workflow.png hello.tikz.tex

# List of PDF/SVG figures (for vector graphics)
VECTORFIGURES = hello.tikz.svg

AUX_FILES=custom.css

AUTHOR_EMAIL=msdemlei@ari.uni-heidelberg.de

DOCREPO_BASEURL=http://ivoa.net/documents/Notes/IVOATexDoc

-include ivoatex/Makefile

ivoatex/Makefile:
	@echo "*** ivoatex submodule not found.  Initialising submodules."
	@echo
	git submodule update --init

STILTS ?= stilts

# This test needs STILTS (http://www.starlink.ac.uk/stilts/)
test:
	$(STILTS) votlint votable=fields-container.xml

