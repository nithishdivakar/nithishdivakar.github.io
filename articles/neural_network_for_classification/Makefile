FILE=tiny-neural-network

all: post pdf

post: ${FILE}.tex
	python3 ../convert.py ${FILE}.tex /home/nd/NOTWORK/website/_drafts/${FILE}.md

pdf:
	latexmk -pdf ${FILE}.tex

clean:
	latexmk -c
	rm *.sta

cleanup:
	latexmk -C

#figures:
#	cd figures; pdflatex -shell-escape network_compute_graph.tex
#	cd figures; pdflatex -shell-escape layer_compute_graph.tex
