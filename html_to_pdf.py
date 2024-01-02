import pdfkit
from flask import Flask, render_template
from pyvirtualdisplay import Display
import json
import data_treat

REPORT_OPTION = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.76in',
    'margin-bottom': '0.75in',
    'margin-left': '0.76in',
    'encoding': "UTF-8",
    'enable-local-file-access': None,
    'log-level': 'warn',
    'enable-toc-back-links': None,  # 目录反向链接
}


def html_str_to_pdf(data, filename='tmp01.pdf', option=None, toc=None, cover=None, css=None):
    """根据html文本内容生成pdf文件.
    pdfkit依赖：
        xvfb, wkhtmltopdf>=0.12.6
    """
    if option is None:
        option = REPORT_OPTION
    with Display():
        pdfkit.from_string(data, filename, options=option, toc=toc, cover=cover, css=css, cover_first=True)


if __name__ == "__main__":
    param = {}
    # data_treat.start()
    with open('./translate.json', 'r') as fp:
        param = fp.read()

    param = json.loads(param)

    app = Flask(__name__, template_folder='/Users/angel/Documents/MyProgram/pythonProject/openvas/')
    with app.app_context():
        content = render_template('reportdemo.html', **param)
    html_str_to_pdf(data=content)

