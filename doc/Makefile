# 该 Makefile 用于编译一个 Latex 文档
# 运行环境：Linux、texlive2010(XeTeX)、evince 阅读器

Compiler = xelatex
Bibcompiler = bibtex
Reader = evince

Target = Thesis.pdf
Source = Thesis.tex
Class = CAS.cls
Chapter = introduction.tex data_method.tex ims.tex conclusion.tex acknowledgment.tex cnds_hinet.tex publish_list.tex
BibSource = Thesis.aux
TmpFile = *.out *.log *.aux *.nav *.snm *.toc *.bbl *.blg

$(Target): $(Source) $(Class) $(Chapter)
	$(Compiler) $(Source)
	$(Bibcompiler) $(BibSource)
	$(Compiler) $(Source)
	$(Compiler) $(Source)

all: $(Target) clean read 

read:
	$(Reader) $(Target)

clean:
	-rm $(TmpFile)

cleanall:
	-rm $(TmpFile) $(Target)

.PHONY: all read clean cleanall
