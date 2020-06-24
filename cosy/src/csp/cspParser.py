# Generated from ./csp.g by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22")
        buf.write("M\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3\3\6\3")
        buf.write("\34\n\3\r\3\16\3\35\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3")
        buf.write("\5\3\5\7\5*\n\5\f\5\16\5-\13\5\3\5\3\5\3\6\3\6\3\6\3\6")
        buf.write("\3\7\6\7\66\n\7\r\7\16\7\67\3\b\3\b\3\b\3\b\3\b\3\t\3")
        buf.write("\t\3\t\7\tB\n\t\f\t\16\tE\13\t\3\n\3\n\3\n\3\n\3\13\3")
        buf.write("\13\3\13\2\2\f\2\4\6\b\n\f\16\20\22\24\2\3\3\2\r\16\2")
        buf.write("F\2\26\3\2\2\2\4\33\3\2\2\2\6\37\3\2\2\2\b%\3\2\2\2\n")
        buf.write("\60\3\2\2\2\f\65\3\2\2\2\169\3\2\2\2\20>\3\2\2\2\22F\3")
        buf.write("\2\2\2\24J\3\2\2\2\26\27\5\4\3\2\27\30\5\n\6\2\30\31\5")
        buf.write("\f\7\2\31\3\3\2\2\2\32\34\5\6\4\2\33\32\3\2\2\2\34\35")
        buf.write("\3\2\2\2\35\33\3\2\2\2\35\36\3\2\2\2\36\5\3\2\2\2\37 ")
        buf.write("\7\3\2\2 !\t\2\2\2!\"\7\6\2\2\"#\5\b\5\2#$\7\5\2\2$\7")
        buf.write("\3\2\2\2%&\7\7\2\2&+\7\r\2\2\'(\7\t\2\2(*\7\r\2\2)\'\3")
        buf.write("\2\2\2*-\3\2\2\2+)\3\2\2\2+,\3\2\2\2,.\3\2\2\2-+\3\2\2")
        buf.write("\2./\7\b\2\2/\t\3\2\2\2\60\61\7\4\2\2\61\62\7\16\2\2\62")
        buf.write("\63\7\5\2\2\63\13\3\2\2\2\64\66\5\16\b\2\65\64\3\2\2\2")
        buf.write("\66\67\3\2\2\2\67\65\3\2\2\2\678\3\2\2\28\r\3\2\2\29:")
        buf.write("\7\16\2\2:;\7\n\2\2;<\5\20\t\2<=\7\5\2\2=\17\3\2\2\2>")
        buf.write("C\5\22\n\2?@\7\13\2\2@B\5\22\n\2A?\3\2\2\2BE\3\2\2\2C")
        buf.write("A\3\2\2\2CD\3\2\2\2D\21\3\2\2\2EC\3\2\2\2FG\7\r\2\2GH")
        buf.write("\7\f\2\2HI\7\16\2\2I\23\3\2\2\2JK\7\21\2\2K\25\3\2\2\2")
        buf.write("\6\35+\67C")
        return buf.getvalue()


class cspParser ( Parser ):

    grammarFileName = "csp.g"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'chan'", "'initial'", "';'", "':'", "'{'", 
                     "'}'", "','", "':='", "'|'", "'->'" ]

    symbolicNames = [ "<INVALID>", "CHANNEL", "INITIAL", "SEMI", "COLON", 
                      "LCURLY", "RCURLY", "COMMA", "ASSIGN", "BAR", "ARROW", 
                      "MID", "PID", "INT", "DIGIT", "LINECOMMENT", "WS" ]

    RULE_cspStream = 0
    RULE_extMessages = 1
    RULE_extMessage = 2
    RULE_domainSet = 3
    RULE_initialState = 4
    RULE_procAlgebra = 5
    RULE_procStmt = 6
    RULE_transitionAlternatives = 7
    RULE_transition = 8
    RULE_comment = 9

    ruleNames =  [ "cspStream", "extMessages", "extMessage", "domainSet", 
                   "initialState", "procAlgebra", "procStmt", "transitionAlternatives", 
                   "transition", "comment" ]

    EOF = Token.EOF
    CHANNEL=1
    INITIAL=2
    SEMI=3
    COLON=4
    LCURLY=5
    RCURLY=6
    COMMA=7
    ASSIGN=8
    BAR=9
    ARROW=10
    MID=11
    PID=12
    INT=13
    DIGIT=14
    LINECOMMENT=15
    WS=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class CspStreamContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def extMessages(self):
            return self.getTypedRuleContext(cspParser.ExtMessagesContext,0)


        def initialState(self):
            return self.getTypedRuleContext(cspParser.InitialStateContext,0)


        def procAlgebra(self):
            return self.getTypedRuleContext(cspParser.ProcAlgebraContext,0)


        def getRuleIndex(self):
            return cspParser.RULE_cspStream

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCspStream" ):
                listener.enterCspStream(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCspStream" ):
                listener.exitCspStream(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCspStream" ):
                return visitor.visitCspStream(self)
            else:
                return visitor.visitChildren(self)




    def cspStream(self):

        localctx = cspParser.CspStreamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cspStream)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.extMessages()
            self.state = 21
            self.initialState()
            self.state = 22
            self.procAlgebra()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExtMessagesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def extMessage(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cspParser.ExtMessageContext)
            else:
                return self.getTypedRuleContext(cspParser.ExtMessageContext,i)


        def getRuleIndex(self):
            return cspParser.RULE_extMessages

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExtMessages" ):
                listener.enterExtMessages(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExtMessages" ):
                listener.exitExtMessages(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtMessages" ):
                return visitor.visitExtMessages(self)
            else:
                return visitor.visitChildren(self)




    def extMessages(self):

        localctx = cspParser.ExtMessagesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_extMessages)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 24
                self.extMessage()
                self.state = 27 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==cspParser.CHANNEL):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExtMessageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.chan_name = None # Token
            self.trans_vals = None # DomainSetContext

        def CHANNEL(self):
            return self.getToken(cspParser.CHANNEL, 0)

        def COLON(self):
            return self.getToken(cspParser.COLON, 0)

        def SEMI(self):
            return self.getToken(cspParser.SEMI, 0)

        def domainSet(self):
            return self.getTypedRuleContext(cspParser.DomainSetContext,0)


        def MID(self):
            return self.getToken(cspParser.MID, 0)

        def PID(self):
            return self.getToken(cspParser.PID, 0)

        def getRuleIndex(self):
            return cspParser.RULE_extMessage

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExtMessage" ):
                listener.enterExtMessage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExtMessage" ):
                listener.exitExtMessage(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtMessage" ):
                return visitor.visitExtMessage(self)
            else:
                return visitor.visitChildren(self)




    def extMessage(self):

        localctx = cspParser.ExtMessageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_extMessage)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.match(cspParser.CHANNEL)
            self.state = 30
            localctx.chan_name = self._input.LT(1)
            _la = self._input.LA(1)
            if not(_la==cspParser.MID or _la==cspParser.PID):
                localctx.chan_name = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 31
            self.match(cspParser.COLON)
            self.state = 32
            localctx.trans_vals = self.domainSet()
            self.state = 33
            self.match(cspParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DomainSetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LCURLY(self):
            return self.getToken(cspParser.LCURLY, 0)

        def MID(self, i:int=None):
            if i is None:
                return self.getTokens(cspParser.MID)
            else:
                return self.getToken(cspParser.MID, i)

        def RCURLY(self):
            return self.getToken(cspParser.RCURLY, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(cspParser.COMMA)
            else:
                return self.getToken(cspParser.COMMA, i)

        def getRuleIndex(self):
            return cspParser.RULE_domainSet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDomainSet" ):
                listener.enterDomainSet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDomainSet" ):
                listener.exitDomainSet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDomainSet" ):
                return visitor.visitDomainSet(self)
            else:
                return visitor.visitChildren(self)




    def domainSet(self):

        localctx = cspParser.DomainSetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_domainSet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(cspParser.LCURLY)
            self.state = 36
            self.match(cspParser.MID)
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==cspParser.COMMA:
                self.state = 37
                self.match(cspParser.COMMA)
                self.state = 38
                self.match(cspParser.MID)
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
            self.match(cspParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class InitialStateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.state_name = None # Token

        def INITIAL(self):
            return self.getToken(cspParser.INITIAL, 0)

        def SEMI(self):
            return self.getToken(cspParser.SEMI, 0)

        def PID(self):
            return self.getToken(cspParser.PID, 0)

        def getRuleIndex(self):
            return cspParser.RULE_initialState

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitialState" ):
                listener.enterInitialState(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitialState" ):
                listener.exitInitialState(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitialState" ):
                return visitor.visitInitialState(self)
            else:
                return visitor.visitChildren(self)




    def initialState(self):

        localctx = cspParser.InitialStateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_initialState)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(cspParser.INITIAL)
            self.state = 47
            localctx.state_name = self.match(cspParser.PID)
            self.state = 48
            self.match(cspParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ProcAlgebraContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cspParser.ProcStmtContext)
            else:
                return self.getTypedRuleContext(cspParser.ProcStmtContext,i)


        def getRuleIndex(self):
            return cspParser.RULE_procAlgebra

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProcAlgebra" ):
                listener.enterProcAlgebra(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProcAlgebra" ):
                listener.exitProcAlgebra(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProcAlgebra" ):
                return visitor.visitProcAlgebra(self)
            else:
                return visitor.visitChildren(self)




    def procAlgebra(self):

        localctx = cspParser.ProcAlgebraContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_procAlgebra)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 50
                self.procStmt()
                self.state = 53 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==cspParser.PID):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ProcStmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.state_name = None # Token

        def ASSIGN(self):
            return self.getToken(cspParser.ASSIGN, 0)

        def transitionAlternatives(self):
            return self.getTypedRuleContext(cspParser.TransitionAlternativesContext,0)


        def SEMI(self):
            return self.getToken(cspParser.SEMI, 0)

        def PID(self):
            return self.getToken(cspParser.PID, 0)

        def getRuleIndex(self):
            return cspParser.RULE_procStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProcStmt" ):
                listener.enterProcStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProcStmt" ):
                listener.exitProcStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProcStmt" ):
                return visitor.visitProcStmt(self)
            else:
                return visitor.visitChildren(self)




    def procStmt(self):

        localctx = cspParser.ProcStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_procStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            localctx.state_name = self.match(cspParser.PID)
            self.state = 56
            self.match(cspParser.ASSIGN)
            self.state = 57
            self.transitionAlternatives()
            self.state = 58
            self.match(cspParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TransitionAlternativesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def transition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cspParser.TransitionContext)
            else:
                return self.getTypedRuleContext(cspParser.TransitionContext,i)


        def BAR(self, i:int=None):
            if i is None:
                return self.getTokens(cspParser.BAR)
            else:
                return self.getToken(cspParser.BAR, i)

        def getRuleIndex(self):
            return cspParser.RULE_transitionAlternatives

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransitionAlternatives" ):
                listener.enterTransitionAlternatives(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransitionAlternatives" ):
                listener.exitTransitionAlternatives(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransitionAlternatives" ):
                return visitor.visitTransitionAlternatives(self)
            else:
                return visitor.visitChildren(self)




    def transitionAlternatives(self):

        localctx = cspParser.TransitionAlternativesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_transitionAlternatives)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.transition()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==cspParser.BAR:
                self.state = 61
                self.match(cspParser.BAR)
                self.state = 62
                self.transition()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TransitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.trans_val = None # Token
            self.state_name = None # Token

        def ARROW(self):
            return self.getToken(cspParser.ARROW, 0)

        def MID(self):
            return self.getToken(cspParser.MID, 0)

        def PID(self):
            return self.getToken(cspParser.PID, 0)

        def getRuleIndex(self):
            return cspParser.RULE_transition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransition" ):
                listener.enterTransition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransition" ):
                listener.exitTransition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransition" ):
                return visitor.visitTransition(self)
            else:
                return visitor.visitChildren(self)




    def transition(self):

        localctx = cspParser.TransitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_transition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            localctx.trans_val = self.match(cspParser.MID)
            self.state = 69
            self.match(cspParser.ARROW)
            self.state = 70
            localctx.state_name = self.match(cspParser.PID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CommentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LINECOMMENT(self):
            return self.getToken(cspParser.LINECOMMENT, 0)

        def getRuleIndex(self):
            return cspParser.RULE_comment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment" ):
                listener.enterComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment" ):
                listener.exitComment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComment" ):
                return visitor.visitComment(self)
            else:
                return visitor.visitChildren(self)




    def comment(self):

        localctx = cspParser.CommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_comment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(cspParser.LINECOMMENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





