# Uses FDR4 bindings to flatten an environment model and print it in a simple form
# This is not linked to the rest of the code as FDR4 bindings are in Python2 while SPOT bindings are Python3!



# **** REQUIRES Python2 ****

import sys
import fdr

from util import normalize

# Assumptions:
# 1. Actions with names prefixed with "i" are assumed to be internal and are not recorded in the single channel of the output file


def load_cspm_model(filename, processname):
    # link to FDR4 to parse CSPM file
    
    fdr.library_init()

    session = fdr.Session()
    session.load_file(filename)

    # [kedar] not quite sure what the semantic model does, or the final argument
    evalp = session.evaluate_process(processname, fdr.SemanticModel_Traces, None)

    # p is the LTS
    p = evalp.result()

    # initial states
    init = p.root_node()

    # events sets. Each is a list of strings
    public = []
    private = []
    
    cevs = p.alphabet(False)           
    for ce in cevs:
        e = normalize(str(session.uncompile_event(ce)))
        if e[0] == 'i':  # internal/private event
            private.append(e)
        else:
            public.append(e)


    # note private action names
    print "# private actions: ", 
    if len(private) > 0:
        print private[0],
        for e in private[1:]:
            print ", ", e, 
    print ""
    print "" 
        
    # output public action names
    assert(len(public) > 0)
    
    print "chan public: {", public[0], 
    for e in public[1:]:
        print ",", e,
    print "};"

    print "" 
    print "initial", ("E" + str(init.hash_code())), ";" 
    
    # explore state transition graph
    visited = set()
    workset = set()
    workset.add(init)

    while len(workset) != 0:
        n = workset.pop()
        visited.add(n)

        ns = normalize(str(n.hash_code()))  # state name for node n
        
        # get transitions from node n
        trs = p.transitions(n)

        print ""
        print ("E" + ns), " := ", 
        first = True
        
        # scan transitions from n; add destinations to workset if not visited
        for t in trs:
            ce = t.event()
            m = t.destination()

            # add uncompiled transition from ns to ms on event e
            ms = normalize(str(m.hash_code()))
            e = normalize(str(session.uncompile_event(ce)))
            
            if first:
                first = False
            else:
                print "|",

            print e, "->", ("E"+ms), 
            
            if m not in visited:
                workset.add(m)

        # end for
        print ";"
        
    # end while
    print ""
    fdr.library_exit() 


if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv) != 3:
        print "Translator from FDR CSPM to simple CSP format: run with arguments <filename> <environment-process-name>"
    else:
        load_cspm_model(sys.argv[1], sys.argv[2])


