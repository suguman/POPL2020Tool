# Generated from ./csp.g by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\22")
        buf.write("g\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6")
        buf.write("\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\13")
        buf.write("\3\f\3\f\7\fE\n\f\f\f\16\fH\13\f\3\r\3\r\7\rL\n\r\f\r")
        buf.write("\16\rO\13\r\3\16\6\16R\n\16\r\16\16\16S\3\17\3\17\3\20")
        buf.write("\3\20\7\20Z\n\20\f\20\16\20]\13\20\3\20\3\20\3\21\6\21")
        buf.write("b\n\21\r\21\16\21c\3\21\3\21\2\2\22\3\3\5\4\7\5\t\6\13")
        buf.write("\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37")
        buf.write("\21!\22\3\2\5\7\2\60\60\62;C\\aac|\4\2\f\f\17\17\5\2\13")
        buf.write("\f\17\17\"\"\2k\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2")
        buf.write("\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21")
        buf.write("\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3")
        buf.write("\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2")
        buf.write("\2\3#\3\2\2\2\5(\3\2\2\2\7\60\3\2\2\2\t\62\3\2\2\2\13")
        buf.write("\64\3\2\2\2\r\66\3\2\2\2\178\3\2\2\2\21:\3\2\2\2\23=\3")
        buf.write("\2\2\2\25?\3\2\2\2\27B\3\2\2\2\31I\3\2\2\2\33Q\3\2\2\2")
        buf.write("\35U\3\2\2\2\37W\3\2\2\2!a\3\2\2\2#$\7e\2\2$%\7j\2\2%")
        buf.write("&\7c\2\2&\'\7p\2\2\'\4\3\2\2\2()\7k\2\2)*\7p\2\2*+\7k")
        buf.write("\2\2+,\7v\2\2,-\7k\2\2-.\7c\2\2./\7n\2\2/\6\3\2\2\2\60")
        buf.write("\61\7=\2\2\61\b\3\2\2\2\62\63\7<\2\2\63\n\3\2\2\2\64\65")
        buf.write("\7}\2\2\65\f\3\2\2\2\66\67\7\177\2\2\67\16\3\2\2\289\7")
        buf.write(".\2\29\20\3\2\2\2:;\7<\2\2;<\7?\2\2<\22\3\2\2\2=>\7~\2")
        buf.write("\2>\24\3\2\2\2?@\7/\2\2@A\7@\2\2A\26\3\2\2\2BF\4c|\2C")
        buf.write("E\t\2\2\2DC\3\2\2\2EH\3\2\2\2FD\3\2\2\2FG\3\2\2\2G\30")
        buf.write("\3\2\2\2HF\3\2\2\2IM\4C\\\2JL\t\2\2\2KJ\3\2\2\2LO\3\2")
        buf.write("\2\2MK\3\2\2\2MN\3\2\2\2N\32\3\2\2\2OM\3\2\2\2PR\5\35")
        buf.write("\17\2QP\3\2\2\2RS\3\2\2\2SQ\3\2\2\2ST\3\2\2\2T\34\3\2")
        buf.write("\2\2UV\4\62;\2V\36\3\2\2\2W[\7%\2\2XZ\n\3\2\2YX\3\2\2")
        buf.write("\2Z]\3\2\2\2[Y\3\2\2\2[\\\3\2\2\2\\^\3\2\2\2][\3\2\2\2")
        buf.write("^_\b\20\2\2_ \3\2\2\2`b\t\4\2\2a`\3\2\2\2bc\3\2\2\2ca")
        buf.write("\3\2\2\2cd\3\2\2\2de\3\2\2\2ef\b\21\2\2f\"\3\2\2\2\b\2")
        buf.write("FMS[c\3\2\3\2")
        return buf.getvalue()


class cspLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    CHANNEL = 1
    INITIAL = 2
    SEMI = 3
    COLON = 4
    LCURLY = 5
    RCURLY = 6
    COMMA = 7
    ASSIGN = 8
    BAR = 9
    ARROW = 10
    MID = 11
    PID = 12
    INT = 13
    DIGIT = 14
    LINECOMMENT = 15
    WS = 16

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'chan'", "'initial'", "';'", "':'", "'{'", "'}'", "','", "':='", 
            "'|'", "'->'" ]

    symbolicNames = [ "<INVALID>",
            "CHANNEL", "INITIAL", "SEMI", "COLON", "LCURLY", "RCURLY", "COMMA", 
            "ASSIGN", "BAR", "ARROW", "MID", "PID", "INT", "DIGIT", "LINECOMMENT", 
            "WS" ]

    ruleNames = [ "CHANNEL", "INITIAL", "SEMI", "COLON", "LCURLY", "RCURLY", 
                  "COMMA", "ASSIGN", "BAR", "ARROW", "MID", "PID", "INT", 
                  "DIGIT", "LINECOMMENT", "WS" ]

    grammarFileName = "csp.g"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


