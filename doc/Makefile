COMPILER = rubber
COMPILER_FLAGS = --pdf

all : report2.pdf

%.pdf : %.tex
	$(COMPILER) $(COMPILER_FLAGS) $<

clean :
	-rm -rf *.aux *.toc *.dvi *.log *.pdf *.out

