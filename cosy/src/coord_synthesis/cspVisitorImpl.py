#from antlr4 import *
#from gen.cspLexer import cspLexer

if __name__ is not None and "." in __name__:
    print("nop")
    # from .cspParser import cspParser
else:
    from gen.cspParser import cspParser

from gen.cspVisitor import cspVisitor
from util import cond_print
from util import VERBOSE_LOW, VERBOSE_MID


global_states = {}
# unique internal state
global_states['STOP'] = {}

global_transitions = {}
# unique internal channel
global_transitions['_internal'] = []

# initial state
initial = ["***FIXME***"]

class cspVisitorVarDecl(cspVisitor):

    def visitCspStream(self, ctx:cspParser.CspStreamContext):
        cond_print(VERBOSE_LOW, "==> Starting cspVisitorVarDecl visit =========")
        ret = self.visitChildren(ctx)
        cond_print(VERBOSE_LOW, "----> Done cspVisitorVarDecl visit")
        return ret

    def visitInitialState(self, ctx:cspParser.InitialStateContext):
        initial[0] = str(ctx.state_name.text)
        cond_print(VERBOSE_LOW, "Initial state: " + initial[0])

        
    def visitExtMessage(self, ctx:cspParser.ExtMessageContext):
        ## evaluating children to check the format first...
        ret = self.visitChildren(ctx)
        ## processing channel
        chan_name = str(ctx.chan_name.text)
        if (chan_name in global_transitions):
            raise Exception("Channel '" + chan_name + "' already exists")
        ## processing transitions/messages
        all_trans_vals = []
        for trans_val_item in ctx.trans_vals.MID():
            trans_val = trans_val_item.getText()
            if (trans_val in all_trans_vals):
                raise Exception("Value '" + trans_val + "' is already exists in channel '" + chan_name + "'")
            ## searching values in other channel (remove following to implement channel namespace)
            for global_chan_name in global_transitions:
                if (trans_val in global_transitions[global_chan_name]):
                    raise Exception("Value '" + global_chan_name + "' is already exists in other channel (channel namespace is not support yet)")
                
            all_trans_vals.append(trans_val)
        ## adding to the global list of channels
        cond_print(VERBOSE_MID, "----> Defining EXTERNAL CHANNEL variable '" + chan_name + "' with values: " + str(all_trans_vals))
        global_transitions[chan_name] = all_trans_vals
        #
        return ret 

    def visitProcStmt(self, ctx:cspParser.ProcStmtContext):
        ## evaluating children to check the format first...
        ret = self.visitChildren(ctx)
        ## checking if process is already defined
        state_name = str(ctx.state_name.text)
        if (state_name in global_states):
            raise Exception("Definition for process '" + state_name + "' already exists")
        ## adding to the global list of states
        cond_print(VERBOSE_MID, "----> Defining process '" + state_name + "'")
        global_states[state_name] = {}
        #
        return ret
    
class cspVisitorTransDecl(cspVisitor):

    def visitCspStream(self, ctx:cspParser.CspStreamContext):
        cond_print(VERBOSE_LOW, "==> Starting cspVisitorTransDecl visit =======")
        ret =  self.visitChildren(ctx)
        cond_print(VERBOSE_LOW, "----> Done cspVisitorTransDecl visit")
        return ret
    
    ###############################
    # def visitProcStmt():
    # could be implemented more cleanly by extending ProcStmtContext to hold the context.
    state_name_context = None
    def visitProcStmt(self, ctx:cspParser.ProcStmtContext):
        ## only reserving context (see note above) 
        self.state_name_context = str(ctx.state_name.text)
        global_states[self.state_name_context] = {}
        ## and then evaluating children to check the format...
        return self.visitChildren(ctx)

    def visitTransition(self, ctx:cspParser.TransitionContext):
        ## need to evaluate expression before working
        ret = self.visitChildren(ctx)
        #
        trans_val = str(ctx.trans_val.text)
        state_name = str(ctx.state_name.text)
        ## checking if process does not exits
        if (state_name not in global_states):
            raise Exception("Cannot define a transition to process '" + state_name + "' that does not exists")
        
        ## checking if transition exists
        trans_val_exists = False
        for global_chan_name in global_transitions:
            if (trans_val in global_transitions[global_chan_name]):
                trans_val_exists = True
                break
        ## if does not exists, then it is internal transition
        if (not trans_val_exists):
            global_transitions['_internal'].append(trans_val)
        ## adding the transition to the state
        cond_print(VERBOSE_MID, "----> Defining transition from '" + self.state_name_context +
                  "' to '" + state_name + "' over message '" + trans_val + "'")
        global_states[self.state_name_context][trans_val] = state_name
        #
        return ret
    

del cspParser
