from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalTrueColorFormatter


lexer = PythonLexer(ensurenl=False)
formatter = TerminalTrueColorFormatter(style="rainbow_dash")


def code_highlight(code: str) -> str:
    return highlight(code, lexer, formatter)


__all__ = ("code_highlight",)
