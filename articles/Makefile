all: The-Standard-Tibetan-Syllable-tib.pdf

tibliographyltx.bib: tibliography/tibliography.bib
	cat tibliography/tibliography.bib | perl -CS -p -e 's/(\p{Tibetan}+)/\\tibbib\{\1\}/g' | perl -CS -p -e 's/(\p{Han}+)/\\chinbib\{\1\}/g' > tibliographyltx.bib

The-Standard-Tibetan-Syllable-tib.tex: The-Standard-Tibetan-Syllable.tex
	cat The-Standard-Tibetan-Syllable.tex | perl -CS -p -e 's/((◌|\p{Tibetan})+)/\{\\tibetanfont \1\}/g' > The-Standard-Tibetan-Syllable-tib.tex

The-Standard-Tibetan-Syllable-tib.pdf: tibliographyltx.bib The-Standard-Tibetan-Syllable-tib.tex tib-articles.sty
	latexmk -lualatex The-Standard-Tibetan-Syllable-tib.tex

clean:
	rm tibliographyltx.bib
	latexmk -C -bibtex -lualatex The-Standard-Tibetan-Syllable-tib.tex
	rm The-Standard-Tibetan-Syllable-tib.tex