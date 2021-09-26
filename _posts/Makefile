FORMAT=png

SRCS := $(wildcard *.tex)
OUTS := $(SRCS:%.tex=%.pdf)

all: ${OUTS}

%.pdf: %.tex
	@echo "Compiling $<"
	pdflatex --shell-escape -synctex=1 -interaction=nonstopmode $< > /dev/null
	ls -1 $(basename $<).compiled*.${FORMAT}
	mv $(basename $<).compiled*.${FORMAT} ../images


clean: 
	latexmk -C
