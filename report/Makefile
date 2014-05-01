COMPILER = rubber
COMPILER_FLAGS = --pdf

all : report.pdf

report.pdf : report.tex
	$(COMPILER) $(COMPILER_FLAGS) report.tex

clean :
	-rm -rf *.aux *.toc *.dvi *.log *.pdf

