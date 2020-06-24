# Generated from ./csp.g by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cspParser import cspParser
else:
    from cspParser import cspParser

# This class defines a complete generic visitor for a parse tree produced by cspParser.

class cspVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by cspParser#cspStream.
    def visitCspStream(self, ctx:cspParser.CspStreamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#extMessages.
    def visitExtMessages(self, ctx:cspParser.ExtMessagesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#extMessage.
    def visitExtMessage(self, ctx:cspParser.ExtMessageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#domainSet.
    def visitDomainSet(self, ctx:cspParser.DomainSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#initialState.
    def visitInitialState(self, ctx:cspParser.InitialStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#procAlgebra.
    def visitProcAlgebra(self, ctx:cspParser.ProcAlgebraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#procStmt.
    def visitProcStmt(self, ctx:cspParser.ProcStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#transitionAlternatives.
    def visitTransitionAlternatives(self, ctx:cspParser.TransitionAlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#transition.
    def visitTransition(self, ctx:cspParser.TransitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by cspParser#comment.
    def visitComment(self, ctx:cspParser.CommentContext):
        return self.visitChildren(ctx)



del cspParser