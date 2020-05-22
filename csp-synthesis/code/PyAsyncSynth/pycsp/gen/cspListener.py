# Generated from ./csp.g by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cspParser import cspParser
else:
    from cspParser import cspParser

# This class defines a complete listener for a parse tree produced by cspParser.
class cspListener(ParseTreeListener):

    # Enter a parse tree produced by cspParser#cspStream.
    def enterCspStream(self, ctx:cspParser.CspStreamContext):
        pass

    # Exit a parse tree produced by cspParser#cspStream.
    def exitCspStream(self, ctx:cspParser.CspStreamContext):
        pass


    # Enter a parse tree produced by cspParser#extMessages.
    def enterExtMessages(self, ctx:cspParser.ExtMessagesContext):
        pass

    # Exit a parse tree produced by cspParser#extMessages.
    def exitExtMessages(self, ctx:cspParser.ExtMessagesContext):
        pass


    # Enter a parse tree produced by cspParser#extMessage.
    def enterExtMessage(self, ctx:cspParser.ExtMessageContext):
        pass

    # Exit a parse tree produced by cspParser#extMessage.
    def exitExtMessage(self, ctx:cspParser.ExtMessageContext):
        pass


    # Enter a parse tree produced by cspParser#domainSet.
    def enterDomainSet(self, ctx:cspParser.DomainSetContext):
        pass

    # Exit a parse tree produced by cspParser#domainSet.
    def exitDomainSet(self, ctx:cspParser.DomainSetContext):
        pass


    # Enter a parse tree produced by cspParser#initialState.
    def enterInitialState(self, ctx:cspParser.InitialStateContext):
        pass

    # Exit a parse tree produced by cspParser#initialState.
    def exitInitialState(self, ctx:cspParser.InitialStateContext):
        pass


    # Enter a parse tree produced by cspParser#procAlgebra.
    def enterProcAlgebra(self, ctx:cspParser.ProcAlgebraContext):
        pass

    # Exit a parse tree produced by cspParser#procAlgebra.
    def exitProcAlgebra(self, ctx:cspParser.ProcAlgebraContext):
        pass


    # Enter a parse tree produced by cspParser#procStmt.
    def enterProcStmt(self, ctx:cspParser.ProcStmtContext):
        pass

    # Exit a parse tree produced by cspParser#procStmt.
    def exitProcStmt(self, ctx:cspParser.ProcStmtContext):
        pass


    # Enter a parse tree produced by cspParser#transitionAlternatives.
    def enterTransitionAlternatives(self, ctx:cspParser.TransitionAlternativesContext):
        pass

    # Exit a parse tree produced by cspParser#transitionAlternatives.
    def exitTransitionAlternatives(self, ctx:cspParser.TransitionAlternativesContext):
        pass


    # Enter a parse tree produced by cspParser#transition.
    def enterTransition(self, ctx:cspParser.TransitionContext):
        pass

    # Exit a parse tree produced by cspParser#transition.
    def exitTransition(self, ctx:cspParser.TransitionContext):
        pass


    # Enter a parse tree produced by cspParser#comment.
    def enterComment(self, ctx:cspParser.CommentContext):
        pass

    # Exit a parse tree produced by cspParser#comment.
    def exitComment(self, ctx:cspParser.CommentContext):
        pass


