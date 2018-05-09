#pdflatex -shell-escape figure.tex
#pdflatex -shell-escape table.tex
python3 ../convert.py softmax_classifier.tex /home/nd/NOTWORK/website/_drafts/softmax-classifier-from-scratch.md
latexmk -pdf softmax_classifier.tex
latexmk -c
