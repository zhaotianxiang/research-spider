import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
w = QWebView()
w.load(QUrl('https://www.delftstack.com'))
p = Qp()
p.setPageSize(Qp.A4)
p.setOutputFormat(Qp.PdfFormat)
p.setOutputFileName("sample.pdf")

def convertIt():
    w.print_(p)
    QApplication.exit()

QObject.connect(w, SIGNAL("loadFinished(bool)"), convertIt)
sys.exit(app.exec_())