all: output/ieee-paper.pdf output/ieee-paper.tex output/acm-paper.pdf #output/acm-paper.tex #output/ieee-paper.json # #output/lncs-paper.pdf #output/release-paper.pdf output/double-blind-release-paper.pdf

#output/paper.md: paper/paper.Rmd
#	mkdir -p output
#	Rscript -e "library(knitr); knit(input='paper/paper.Rmd',output='output/paper.md')"

output/ieee-paper.json: paper/paper.md figures
	cp ./styles/IEEEtran.cls .
	mkdir -p output
	pandoc  --wrap=preserve \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		--filter ./pandoc-tools/table-filter.py \
		--number-sections \
		--csl=./styles/ieee.csl \
		./publisher-specifics/ieee-packages.yaml \
		--include-before-body=./templates/acm-longtable-fix-preamble.latex \
		--include-before-body=./publisher-specifics/ieee-author-preamble.latex \
		--template=./templates/acm.latex \
		-t json \
		-o output/ieee-paper.$(subst output/ieee-paper.,,$@) paper/paper.md
	rm ./IEEEtran.cls

output/ieee-paper.pdf output/ieee-paper.tex: paper/paper.md figures
	cp ./styles/IEEEtran.cls .
	mkdir -p output
	pandoc  --wrap=preserve \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		--filter ./pandoc-tools/table-filter.py \
		--filter ./pandoc-tools/bib-filter.py \
		--number-sections \
		--csl=./styles/ieee.csl \
		./publisher-specifics/ieee-packages.yaml \
		--include-before-body=./templates/acm-longtable-fix-preamble.latex \
		--include-before-body=./publisher-specifics/ieee-author-preamble.latex \
		--template=./templates/acm.latex \
		-o output/ieee-paper.$(subst output/ieee-paper.,,$@) paper/paper.md
	rm ./IEEEtran.cls

output/acm-paper.pdf output/acm-paper.tex: paper/paper.md figures
	cp ./styles/acmart.cls .
	mkdir -p output
	pandoc  --wrap=preserve \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		--filter ./pandoc-tools/table-filter.py \
		--csl=./styles/acm.csl \
		--number-sections \
		./publisher-specifics/acm-packages.yaml \
		--include-before-body=./templates/acm-longtable-fix-preamble.latex \
		--include-before-body=./publisher-specifics/acm-author-preamble.latex \
		--template=./templates/acm.latex \
		-o output/acm-paper.$(subst output/acm-paper.,,$@) paper/paper.md
	rm ./acmart.cls

output/lncs-paper.pdf output/lncs-paper.tex: paper/paper.md figures
	cp ./styles/llncs.cls .
	mkdir -p output
	pandoc  --wrap=preserve \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		--csl=./styles/llncs.csl \
		--number-sections \
		./llncs-packages.yaml \
		--template=./templates/llncs.latex \
		-o output/lncs-paper.$(subst output/lncs-paper.,,$@) paper/paper.md
	rm ./llncs.cls

grammarly: paper/paper.md
	pkill Grammarly || true #if grammarly already exists kill it
	pandoc  --wrap=preserve \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		--number-sections \
		-t plain \
		-o output/paper.txt paper/paper.md #now get just the text
	open -a Grammarly output/paper.txt #and open it in grammarly

#output/release-paper.pdf: output/paper.md
#	cp ./styles/llncs.cls .
#	pandoc  --wrap=preserve \
#		--filter pandoc-crossref \
#		--filter pandoc-citeproc \
#		--csl=./styles/lncs.csl \
#		--number-sections \
#		./release-packages.yaml \
#		--template=./templates/llncs.latex \
#		-o output/release-paper.pdf output/paper.md
#	rm ./llncs.cls
#
#output/double-blind-release-paper.pdf: output/paper.md $(TRIMMED_PLOTS)
#	cp ./styles/llncs.cls .
#	pandoc  --wrap=preserve \
#		--filter pandoc-crossref \
#		--filter pandoc-citeproc \
#		--csl=./styles/lncs.csl \
#		--number-sections \
#		./double-blind-release-packages.yaml \
#		--template=./templates/llncs.latex \
#		-o output/double-blind-release-paper.pdf output/paper.md
#	rm ./llncs.cls

clean:
	rm output/*

