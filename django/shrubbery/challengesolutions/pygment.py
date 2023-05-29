from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def pygmentize(code):
    """Apply syntax highlighting to code."""
    return highlight(code, PythonLexer(), HtmlFormatter(linenos='inline', linespans='code-line'))
