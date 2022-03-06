import weasyprint
doc_pdf = weasyprint.HTML('https://www.delftstack.com/').write_pdf('sample.pdf')