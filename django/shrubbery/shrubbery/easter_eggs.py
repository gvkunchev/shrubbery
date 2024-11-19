import random
import re


"""
# Generation process:
from pytube import Playlist
link = "https://www.youtube.com/playlist?list=PLhboEWcuNB1__DiH8Z5MLYigS-KVxWktS"
print(Playlist(link).video_urls)
"""
YOUTUBE_LINKS = [
    'https://www.youtube.com/watch?v=imhrDrE4-mI',
    'https://www.youtube.com/watch?v=W2jgrGtiYHE',
    'https://www.youtube.com/watch?v=epLFeT4qYgc',
    'https://www.youtube.com/watch?v=kYC47DYLq2I',
    'https://www.youtube.com/watch?v=vZw35VUBdzo',
    'https://www.youtube.com/watch?v=pfRdur8GLBM',
    'https://www.youtube.com/watch?v=ZmInkxbvlCs',
    'https://www.youtube.com/watch?v=7DqvweTYTI0',
    'https://www.youtube.com/watch?v=baHsoEAAMZU',
    'https://www.youtube.com/watch?v=vZ9myHhpS9s',
    'https://www.youtube.com/watch?v=J1FfrnOXGHg',
    'https://www.youtube.com/watch?v=ohDB5gbtaEQ',
    'https://www.youtube.com/watch?v=SmzMzmnB-iQ',
    'https://www.youtube.com/watch?v=4JgbOkLdRaE',
    'https://www.youtube.com/watch?v=g3YiPC91QUk',
    'https://www.youtube.com/watch?v=M9DCAFUerzs',
    'https://www.youtube.com/watch?v=t2c-X8HiBng',
    'https://www.youtube.com/watch?v=QDAeJ7eLGGg',
    'https://www.youtube.com/watch?v=jYFefppqEtE',
    'https://www.youtube.com/watch?v=dPOyOM7wxlE',
    'https://www.youtube.com/watch?v=H9PY_3E3h2c',
    'https://www.youtube.com/watch?v=NVhXkQu5_Ig',
    'https://www.youtube.com/watch?v=IxsZN8_l7cc',
    'https://www.youtube.com/watch?v=l9SqQNgDrgg',
    'https://www.youtube.com/watch?v=RbOZccv9ym8',
    'https://www.youtube.com/watch?v=aObgC5A5pr4',
    'https://www.youtube.com/watch?v=qgSzGIkFq2A',
    'https://www.youtube.com/watch?v=Jdf5EXo6I68',
    'https://www.youtube.com/watch?v=1N6OOWtCYQA',
    'https://www.youtube.com/watch?v=FAxkcPoLYcQ',
    'https://www.youtube.com/watch?v=_bW4vEo1F4E',
    'https://www.youtube.com/watch?v=bsFzc0wAtFs',
    'https://www.youtube.com/watch?v=NDbnkYSLwI0',
    'https://www.youtube.com/watch?v=kx_G2a2hL6U',
    'https://www.youtube.com/watch?v=YP2KDUiBI-E',
    'https://www.youtube.com/watch?v=djKPvXDwXcs',
    'https://www.youtube.com/watch?v=AeWI5RcgOLs',
    'https://www.youtube.com/watch?v=SJUhlRoBL8M',
    'https://www.youtube.com/watch?v=e8eHILrlkoM',
    'https://www.youtube.com/watch?v=Hz1JWzyvv8A',
    'https://www.youtube.com/watch?v=0Mu8Hntl1TM',
    'https://www.youtube.com/watch?v=buqtdpuZxvk',
    'https://www.youtube.com/watch?v=E-bIMxB4zA8',
    'https://www.youtube.com/watch?v=hL6QNLBRXCA',
    'https://www.youtube.com/watch?v=pqwgROwL0wM',
    'https://www.youtube.com/watch?v=7Xm_TRekjno',
    'https://www.youtube.com/watch?v=0e2kaQqxmQ0',
    'https://www.youtube.com/watch?v=LtF1ZNqSX3w',
    'https://www.youtube.com/watch?v=QXOKsJViHtY',
    'https://www.youtube.com/watch?v=PuZ24VBrbO4',
    'https://www.youtube.com/watch?v=bzVHjg3AqIQ',
    'https://www.youtube.com/watch?v=PDBjsFAyiwA',
    'https://www.youtube.com/watch?v=uDoQFcQEpOQ',
    'https://www.youtube.com/watch?v=NcHdF1eHhgc',
    'https://www.youtube.com/watch?v=Sp-pU8TFsg0',
    'https://www.youtube.com/watch?v=YXzubuENjHk',
    'https://www.youtube.com/watch?v=mzlCdWwYn2I',
    'https://www.youtube.com/watch?v=kntQNeSge5s',
    'https://www.youtube.com/watch?v=sFBOQzSk14c',
    'https://www.youtube.com/watch?v=rblfKREj50o',
    'https://www.youtube.com/watch?v=tGxAYeeyoIc',
    'https://www.youtube.com/watch?v=Pxbzb8XXiGQ',
    'https://www.youtube.com/watch?v=PAk6KVsJ-l8',
    'https://www.youtube.com/watch?v=G2DCExerOsA',
    'https://www.youtube.com/watch?v=UpPoWGiQIhA',
    'https://www.youtube.com/watch?v=yp_l5ntikaU',
    'https://www.youtube.com/watch?v=xpAvcGcEc0k',
    'https://www.youtube.com/watch?v=JTLeBybJhSo',
    'https://www.youtube.com/watch?v=Cj8n4MfhjUc',
    'https://www.youtube.com/watch?v=U4VjZKPjxnE',
    'https://www.youtube.com/watch?v=a1sn0ZSfnMo',
    'https://www.youtube.com/watch?v=7rwc3VGvlRY',
    'https://www.youtube.com/watch?v=dBPf6P332uM'
]

YOUTUBE_REGEX = re.compile(r'(?<!\[)(?P<monty_python>(Monty +)?Python)(?!\])')

def wrap_match_with_youtube(match):
    link = random.choice(YOUTUBE_LINKS)
    original = match.group('monty_python')
    return f'[{original}]({link})'

def decorate_with_youtube(text):
    return re.sub(YOUTUBE_REGEX, wrap_match_with_youtube, text)
