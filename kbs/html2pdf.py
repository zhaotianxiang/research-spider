# -*- coding: utf-8 -*-
import pdfkit
#启动参数
wkhtmltopdf_options = {
    'enable-local-file-access': None
}

#h.html 输入 out.pdf 输出
pdfkit.from_file("./data/html/ncd=5085536.html", "out.pdf", options=wkhtmltopdf_options)