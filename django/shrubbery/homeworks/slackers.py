import os
import sys
import re

from copydetect import CopyDetector


if os.environ.get('SHRUBBERY_ENV') == 'prd':
    DOMAIN = 'https://2024.y-fmi.org'
    SOURCE = r'/var/shrubbery/media/homeworksolutions/\d+/(\d+)/latest.py'
    TARGET = fr"<a href='{DOMAIN}/student/\1' target='_blank'>{DOMAIN}/student/\1</a>"
else:
    DOMAIN = 'http://localhost:8080'
    SOURCE = r"C:\\Users\\Georgi Kunchev\\Desktop\\shrubbery\\django\\shrubbery\\media\\homeworksolutions\\\d+\\(\d+)\\latest.py"
    TARGET = fr"<a href='{DOMAIN}/student/\1' target='_blank'>{DOMAIN}/student/\1</a>"


detector = CopyDetector(test_dirs=[sys.argv[1]],
                        extensions=["py"], display_t=0.5,
                        ignore_leaf=True, same_name_only=True)
detector.run()
html = detector.generate_html_report(output_mode='return')
html = re.sub(SOURCE, TARGET, html)
print(html)
