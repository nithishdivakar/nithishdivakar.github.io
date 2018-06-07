FILE=a-different-way-to-derive-backprop

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

