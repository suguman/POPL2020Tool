

##BoSy Location w.r.t. this file. 
BOSYPATH = "../bosy"

import argparse
import os
import sys
import signal
import subprocess



import spot

from buddy import bdd_not, bdd_imp, bdd_biimp, bdd_exist, bddtrue, bddfalse, bdd_ithvar, bdd_nodecount

from antlr4.FileStream import InputStream 
from antlr4.CommonTokenStream import CommonTokenStream

from gen.cspLexer import cspLexer
from gen.cspParser import cspParser
from util import cond_print, set_verbosity, normalize
from util import VERBOSE_NONE, VERBOSE_LOW, VERBOSE_HIGH, VERBOSE_MID 
import cspVisitorImpl

bdict = spot.make_bdd_dict();

bdd_print_limit = 100 # nodes

def bdd_str(bdd):
    # return string version of bdd only if it is not too large,
    # else an apologetic message.
    n = bdd_nodecount(bdd)
    if n <= bdd_print_limit:
        return spot.bdd_format_formula(bdict, bdd)
    else:
        return ("[sorry, bdd is too large, #nodes="+str(n)+"]")


def load_csp_file(filename):
    cond_print(VERBOSE_NONE, ">> Loading CSP file " + str(filename.name) + " <<")
    ifs = InputStream(filename.read())
    lexer = cspLexer(ifs)
    stream = CommonTokenStream(lexer)
    parser = cspParser(stream)
    tree = parser.cspStream()
    
    cspVisitorImpl.cspVisitorVarDecl().visit(tree)
    cspVisitorImpl.cspVisitorTransDecl().visit(tree)
    
    cond_print(VERBOSE_NONE, ">> Done loading CSP file <<\n")


def build_vars(var_dict):
    ret = bddtrue
    for var_idx in var_dict:
        ret &= var_dict[var_idx]
    return ret


def build_bvec_domain_inv(var_dict):
    ret = bddfalse
    for var_idx in var_dict:
        val = var_dict[var_idx]
        for other_var_idx in var_dict:
            if (var_idx == other_var_idx): continue
            val &= bdd_not(var_dict[other_var_idx])
        ret |= val
    return ret

    
def build_id(var_dict, other_var_dict):
    ret = bddfalse
    domain = build_bvec_domain_inv(var_dict)
    other_domain = build_bvec_domain_inv(other_var_dict)
    for var_idx in var_dict:
        #ret |= domain & other_domain & bdd_biimp(var_dict[var_idx], other_var_dict[var_idx]) 
        ret |= var_dict[var_idx] & domain & other_var_dict[var_idx] & other_domain
    return ret


def build_bvec_1hot_inv(var_dict):
    ## I think is redundant... the same as: build_bvec_domain_inv 
    ret = bddfalse
    domain = build_bvec_domain_inv(var_dict)
    for var_idx in var_dict:
        bdd_only_idx = var_dict[var_idx] & domain
        ret |= bdd_only_idx
    
    return ret


def build_async_spec():
    action_ap_dict = []
    for action_chan in cspVisitorImpl.global_transitions:
        for action_ap in cspVisitorImpl.global_transitions[action_chan]:
            action_ap_dict.append(action_ap)
    
    async_spec = 'G('
    for action_ap in action_ap_dict:
        clause = '(' + action_ap
        for other_action_ap in action_ap_dict:
            if (action_ap == other_action_ap): continue
            clause = clause + ' & !' + other_action_ap
        async_spec = async_spec + clause + ') | ' 
    #
    if (len(async_spec) > 3): async_spec = async_spec[:-3] # removing the last ' | '
    async_spec = async_spec + ')' # closing
    
    return async_spec



def optimize_spin_file(final_aut, spin_file_temp, spin_file):
    
    #cond_print(VERBOSE_MID, "final aut (dot): \n" + final_aut.to_str("dot"))


    #### without optimize
    #spin_file.write(final_aut.to_str("spin"))

    
    #############################################
    ## writing output
    spin_file_temp.write(final_aut.to_str("spin")) 
    spin_file_temp.close()
    cmd = "autfilt --remove-unreachable-states " + spin_file_temp.name + " --spin > " + spin_file.name
    #cmd = "autfilt --remove-unreachable-states " + spin_file_temp.name + " --spin > " + "tempfile.txt"
    cond_print(VERBOSE_LOW, cmd)
    os.system(cmd)

    cond_print(VERBOSE_NONE, ">> Optimized spin file <<\n")

    
#####
def rename_input_variables(bosy_input_prefix):
    ## first replace all action <name> to y<name>
    for action_chan in cspVisitorImpl.global_transitions:
        renamed_actions = []
        for action_name in cspVisitorImpl.global_transitions[action_chan]:
            renamed_actions.append(bosy_input_prefix + action_name)
        cspVisitorImpl.global_transitions[action_chan] = renamed_actions
        
    for state_name in cspVisitorImpl.global_states:
        new_state_action_dict = {}
        for action_name in cspVisitorImpl.global_states[state_name]:
            new_state_action_dict[bosy_input_prefix + action_name] = cspVisitorImpl.global_states[state_name][action_name]
        cspVisitorImpl.global_states[state_name] = new_state_action_dict


def write_bosy_output(final_aut, spin_file, bosy_file):
    
    #cond_print(VERBOSE_MID, "final aut (dot): \n" + final_aut.to_str("dot"))
    
    #############################################
    ## writing output
    #spin_file.write(final_aut.to_str("spin")) ## need replace?
    #
    bosy_input_list_str = '['
    bosy_output_list_str = '['
    for action_chan in cspVisitorImpl.global_transitions:
        for action_name in cspVisitorImpl.global_transitions[action_chan]:
            if (action_chan != '_internal'):
                bosy_input_list_str += '"' + action_name + '", '
                bosy_output_list_str += '"' + bosy_output_prefix + "set_" + action_name + '", '
    if (len(bosy_input_list_str) > 14): bosy_input_list_str = bosy_input_list_str[:-2] # removing the last ', '
    if (len(bosy_output_list_str) > 13): bosy_output_list_str = bosy_output_list_str[:-2] # removing the last ', '
    bosy_input_list_str += ']'
    bosy_output_list_str += ']'
    #
    bosy_file.write('{\n')
    bosy_file.write('\t"semantics": "moore",\n')
    #bosy_file.write('\t"semantics": "mealy",\n')
    bosy_file.write('\t"inputs": ' + bosy_input_list_str + ',\n')
    bosy_file.write('\t"outputs": ' + bosy_output_list_str + ',\n')
    bosy_file.write('\t"assumptions": [],\n')
    bosy_file.write('\t"guarantees": [],\n')
    bosy_file.write('\t"automaton": "./' + spin_file.name + '"\n')
    bosy_file.write('}\n')

    cond_print(VERBOSE_NONE, ">> Done loading LTL specs <<\n")



def run_bosy(bosy_file, qbf_backend, tout=100):
    os.chdir(BOSYPATH)
    cmd = ['./bosy.sh', './.build-sys/']
    #cmd += '--semantics mealy '
    
    if (qbf_backend):
        cmd += ['--backend input-symbolic ']
    else:
        cmd += ['--backend explicit-one-hot-inputs ']
        
    cmd += ['--semantics moore ']

    # search strategy
    #cmd += '--strategy linear '
    #cmd += ['--strategy exponential ']
    cmd += ['--strategy linear ']

    #output options
    #cmd += '--synthesize --target smv '
    #cmd += '--synthesize --target all '
    cmd += ['--synthesize --target dot ']

    #backend options
    #cmd += '--backend input-symbolic '
    #cmd += '--backend explicit '
    #cmd += '--backend state-symbolic '
    
    cmd += ['--statistics ']
    cmd += ['--player system ']
    cmd += [bosy_file]
    # cmd_array = cmd.split()

    """
    proc = subprocess.Popen("exec " + cmd, shell=True)
    try:
        proc.run(cmd, timeout=tout)
    except TimeoutExpired:
        print("TimeOut")
        #os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        proc.kill()

    """
    try:
        subprocess.run(cmd, timeout=tout)
    except subprocess.TimeoutExpired:
        print("TimeOut")
        #os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        #p.kill()
    

# def run_bosy(bosy_file, qbf_backend, timeout=10):
#     os.chdir(BOSYPATH)
#     cmd = './bosy.sh ./.build-sys/ '
#     #cmd += '--semantics mealy '
    
#     if qbf_backend:
#         cmd += '--backend input-symbolic '
#     else:
#         cmd += '--backend explicit-one-hot-inputs '
        
#     cmd += '--semantics moore '

#     # search strategy
#     #cmd += '--strategy linear '
#     cmd += '--strategy exponential '

#     #output options
#     #cmd += '--synthesize --target smv '
#     #cmd += '--synthesize --target all '
#     cmd += '--synthesize --target dot '

#     #backend options
#     #cmd += '--backend input-symbolic '
#     #cmd += '--backend explicit '
#     #cmd += '--backend state-symbolic '
    
#     cmd += '--statistics '
#     cmd += '--player system '
#     cmd += bosy_file
#     # cmd_array = cmd.split()
#     print("Starting SUBPROCESS with TIMEOUT ", timeout)
#     p = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
#     try:    
#         p.wait(timeout)
#     except subprocess.TimeoutExpired:
#         print("TimeOut")
#         os.killpg(os.getpgid(p.pid), signal.SIGTERM)
#         p.kill()


# API for TWA: twa_graph: https://spot.lrde.epita.fr/doxygen/classspot_1_1twa__graph.html
def build_bosy_instance(safety_spec, liveness_spec, bosy_file, spin_file, spin_file_temp):

    ###########################################################################
    ## rewriting the variable names to align to bosy format
    for action_chan in cspVisitorImpl.global_transitions:
        for action_name in cspVisitorImpl.global_transitions[action_chan]:
            safety_spec = safety_spec.replace(action_name, bosy_input_prefix + action_name)
            liveness_spec = liveness_spec.replace(action_name, bosy_input_prefix + action_name)
    rename_input_variables(bosy_input_prefix)
    
    # async_spec = build_async_spec()
    # cond_print(VERBOSE_LOW, "async part is: " + async_spec)
    
    ###########################################################################
    ## loading specifications
    cond_print(VERBOSE_NONE, ">> Loading LTL specs <<")
    cond_print(VERBOSE_LOW, "==> Parsing LTL spec")
    safety_spec = '(!(' + safety_spec + '))'
    safety_spec_aut = spot.translate(safety_spec, 'BA', 'Deterministic', dict=bdict)

    #print("\nsafety_spec_aut ap\n")
    #for ap in safety_spec_aut.ap():
    #    print(' ', ap, ' (=', bdict.varnum(ap), ')', sep='', end='')    


    liveness_spec = '(!(' + liveness_spec + '))'
    liveness_spec_aut = spot.translate(liveness_spec, 'BA', 'Deterministic', dict=bdict)
    #liveness_spec_aut = spot.translate(liveness_spec, dict=bdict)
    cond_print(VERBOSE_LOW, "----> Done parsing LTL spec")
    

    ## required since it affects the way we handle accepting states
    if (not safety_spec_aut.is_sba()): 
        raise Exception("ERROR: safety_spec_aut is not a state based buchi automata")
    if (not liveness_spec_aut.is_sba()):
        raise Exception("ERROR: liveness_spec_aut is not a state based buchi automata")
    
    ## sanity printouts
    cond_print(VERBOSE_LOW, "A_S aut: \n" + safety_spec_aut.to_str("dot"))
    cond_print(VERBOSE_LOW, "A_L aut: \n" + liveness_spec_aut.to_str("dot"))
        
    cond_print(VERBOSE_LOW, "==> Building statespace components: r - A_S; q - A_L; e - csp")
    
    #############################################
    ## Building safety states and safety transitions
    ## (a) Safety States
    ## (b) Safety Transitions
    #############################################

    #################################
    ### (a) Safety States begin
    #################################
    
    ## - 'r' is a state of A_S 
    ## NEXT: currently XOR aut states --> reduce to bitvec log(N) bits representation
    safety_state = {}
    mid0_safety_state = {}
    mid1_safety_state = {}
    prime_safety_state = {}
    
    for idx in range(safety_spec_aut.num_states()):
        safety_state[idx] = bdd_ithvar(safety_spec_aut.register_ap("safety_state" + str(idx)))
        mid0_safety_state[idx] = bdd_ithvar(safety_spec_aut.register_ap("_mid0_safety_state" + str(idx)))
        mid1_safety_state[idx] = bdd_ithvar(safety_spec_aut.register_ap("_mid1_safety_state" + str(idx)))
        prime_safety_state[idx] = bdd_ithvar(safety_spec_aut.register_ap("_pri_safety_state" + str(idx)))

    ## vars (for quantification)
    safety_state_vars = build_vars(safety_state)
    mid0_safety_state_vars = build_vars(mid0_safety_state)
    mid1_safety_state_vars = build_vars(mid1_safety_state)
    prime_safety_state_vars = build_vars(prime_safety_state)

    ## id (association between versions of the variables)
    safety_state_id = build_id(safety_state, prime_safety_state)
    mid0_safety_state_id = build_id(safety_state, mid0_safety_state)
    mid0_prime_safety_state_id = build_id(prime_safety_state, mid0_safety_state)
    mid1_safety_state_id = build_id(safety_state, mid1_safety_state)
    mid1_prime_safety_state_id = build_id(prime_safety_state, mid1_safety_state)

    ## 1-hot encoding invariant
    safety_state_bvec_inv = build_bvec_1hot_inv(safety_state)
    prime_safety_state_bvec_inv = build_bvec_1hot_inv(prime_safety_state)

    #################################
    ### (a) Safety States end
    ### (b) Safety Transition begin
    #################################

    safety_trans = bddfalse
    safety_acc = bddfalse
    for src_idx in range(safety_spec_aut.num_states()):
        for edge in safety_spec_aut.out(src_idx):
            safety_trans |= (safety_state[edge.src] & edge.cond & prime_safety_state[edge.dst])
            if (edge.acc.count() != 0): safety_acc |= safety_state[edge.src]
    safety_trans &= safety_state_bvec_inv & prime_safety_state_bvec_inv
    safety_acc &= safety_state_bvec_inv 
    
    cond_print(VERBOSE_HIGH, "Safety transitions BDD:\n\t" + bdd_str(safety_trans))
    cond_print(VERBOSE_HIGH, "Safety accepting states:\n\t" + bdd_str(safety_acc))
    cond_print(VERBOSE_LOW, "----> Done building system safety A_S states and transitions")

    #################################
    ### (b) Safety Transition begin
    ### Safety automaton completed
    #################################

    #############################################
    ## Building livness states and livness transitions
    ## (a) livness States
    ## (b) livness Transitions
    #############################################

    #################################
    ### (a) Livness States begin
    ## - 'q' is a state of A_L 
    ## NEXT: currently XOR aut states --> reduce to bitvec log(N) bits representation
    #################################
    
    liveness_state = {}
    mid0_liveness_state = {}
    mid1_liveness_state = {}
    prime_liveness_state = {}
    
    for idx in range(liveness_spec_aut.num_states()):
        liveness_state[idx] = bdd_ithvar(liveness_spec_aut.register_ap("liveness_state" + str(idx)))
        mid0_liveness_state[idx] = bdd_ithvar(liveness_spec_aut.register_ap("_mid0_liveness_state" + str(idx)))
        mid1_liveness_state[idx] = bdd_ithvar(liveness_spec_aut.register_ap("_mid1_liveness_state" + str(idx)))
        prime_liveness_state[idx] = bdd_ithvar(liveness_spec_aut.register_ap("_pri_liveness_state" + str(idx)))

    ## vars (for quantification)
    liveness_state_vars = build_vars(liveness_state)
    mid0_liveness_state_vars = build_vars(mid0_liveness_state)
    mid1_liveness_state_vars = build_vars(mid1_liveness_state)
    prime_liveness_state_vars = build_vars(prime_liveness_state)

    ## id (association between versions of the variables)
    liveness_state_id = build_id(liveness_state, prime_liveness_state)
    mid0_liveness_state_id = build_id(liveness_state, mid0_liveness_state)
    mid0_prime_liveness_state_id = build_id(prime_liveness_state, mid0_liveness_state)
    mid1_liveness_state_id = build_id(liveness_state, mid1_liveness_state)
    mid1_prime_liveness_state_id = build_id(prime_liveness_state, mid1_liveness_state)

    ## 1-hot encoding invariant
    liveness_state_bvec_inv = build_bvec_1hot_inv(liveness_state)
    prime_liveness_state_bvec_inv = build_bvec_1hot_inv(prime_liveness_state)

    #################################
    ### (a) Liveness States end
    ### (b) Liveness Transition begin
    #################################

    liveness_trans = bddfalse
    liveness_acc = bddfalse
    for src_idx in range(liveness_spec_aut.num_states()):
        for edge in liveness_spec_aut.out(src_idx):
            liveness_trans |= (liveness_state[edge.src] & edge.cond & prime_liveness_state[edge.dst])
            # for the non-generalized buchi, (edge.acc.count() != 0) is enough to check if accepting
            if (edge.acc.count() != 0): liveness_acc |= liveness_state[edge.src]
    liveness_trans &= liveness_state_bvec_inv & prime_liveness_state_bvec_inv
    liveness_acc &= liveness_state_bvec_inv 
    prime_liveness_acc = bdd_exist(liveness_acc & liveness_state_id, liveness_state_vars)
    
    cond_print(VERBOSE_HIGH, "Liveness transitions BDD:\n\t" + bdd_str(liveness_trans))
    cond_print(VERBOSE_HIGH, "Liveness accepting states:\n\t" + bdd_str(liveness_acc))
    cond_print(VERBOSE_LOW, "----> Done building system liveness A_L states and transitions")

    #################################
    ### (b) Liveness Transition end
    ### Liveness completed
    #################################

    #############################################
    ## Building env states and env transitions
    ## (a) Env States
    ## (b) Env actions
    ## (c) Env Transitions
    #############################################

    #################################
    ### (a) Env States begin
    ## - 'e' is a state of the environment (CSP)
    #################################
    
    ## NEXT: currently XOR proc --> reduce to bitvec log(N) bits representation
    
    env_aut = spot.make_twa_graph(bdict)
    env_proc_state = {}
    mid0_env_proc_state = {}
    mid1_env_proc_state = {}
    prime_env_proc_state = {}

    env_state_names = sorted(cspVisitorImpl.global_states.keys())
    for state_name in env_state_names:
        env_proc_state[state_name] = bdd_ithvar(env_aut.register_ap(state_name))
        mid0_env_proc_state[state_name] = bdd_ithvar(env_aut.register_ap("_mid0_" + state_name))
        mid1_env_proc_state[state_name] = bdd_ithvar(env_aut.register_ap("_mid1_" + state_name))
        prime_env_proc_state[state_name] = bdd_ithvar(env_aut.register_ap("_pri_" + state_name))

    ## vars (for quantification)
    env_proc_state_vars = build_vars(env_proc_state)
    mid0_env_proc_state_vars = build_vars(mid0_env_proc_state)
    mid1_env_proc_state_vars = build_vars(mid1_env_proc_state)
    prime_env_proc_state_vars = build_vars(prime_env_proc_state)

    ## id (association between versions of the variables)
    env_proc_state_id = build_id(env_proc_state, prime_env_proc_state)
    mid0_env_proc_state_id = build_id(env_proc_state, mid0_env_proc_state)
    mid0_prime_env_proc_state_id = build_id(prime_env_proc_state, mid0_env_proc_state)
    mid1_env_proc_state_id = build_id(env_proc_state, mid1_env_proc_state)
    mid1_prime_env_proc_state_id = build_id(prime_env_proc_state, mid1_env_proc_state)

    ## 1-hot encoding invariant
    env_proc_state_bvec_inv = build_bvec_1hot_inv(env_proc_state)
    prime_env_proc_state_bvec_inv = build_bvec_1hot_inv(prime_env_proc_state)


    #################################
    ### (a) Env States ends
    ### (b) Env Action begins
    #################################
    
    public_actions = {}
    private_actions = {}
    for action_chan in cspVisitorImpl.global_transitions:
        for action_ap in cspVisitorImpl.global_transitions[action_chan]:
            if (action_chan != '_internal'):
                public_actions[action_ap] = bdd_ithvar(env_aut.register_ap(action_ap))
            else:
                private_actions[action_ap] = bdd_ithvar(env_aut.register_ap(action_ap))
                
    ## vars (for quantification)
    public_actions_vars = build_vars(public_actions)
    private_actions_vars = build_vars(private_actions)


    ## 1-hot encoding invariant
    all_actions_bvec_inv = build_bvec_domain_inv({**public_actions, **private_actions})
    public_actions_bvec_inv_temp = build_bvec_domain_inv(public_actions)
    public_actions_bvec_inv = public_actions_bvec_inv_temp & all_actions_bvec_inv
    cond_print(VERBOSE_HIGH, "Public_actions_bvec_inv:\n\t" + bdd_str(public_actions_bvec_inv))
    private_actions_bvec_inv_temp = build_bvec_domain_inv(private_actions)
    private_actions_bvec_inv = private_actions_bvec_inv_temp & all_actions_bvec_inv
    cond_print(VERBOSE_HIGH, "Private_actions_bvec_inv:\n\t" + bdd_str(private_actions_bvec_inv))


    #################################
    ### (b) Env action ends
    ### (c) Env Transition begins
    #################################
    
    public_env_proc_trans = bddfalse
    private_env_proc_trans = bddfalse
    
    public_state_and_actions_bvec_inv = env_proc_state_bvec_inv & prime_env_proc_state_bvec_inv & public_actions_bvec_inv
    private_state_and_actions_bvec_inv = env_proc_state_bvec_inv & prime_env_proc_state_bvec_inv & private_actions_bvec_inv

    # otherwise the BDDs blow up quite dramatically (over a million BDD nodes for an environment process with 30 nodes)
    
    for state_name in env_state_names:
        cond_print(VERBOSE_LOW, "Transition for state " + state_name)
        src = env_proc_state[state_name]
        for action_name in cspVisitorImpl.global_states[state_name]:
            cond_print(VERBOSE_LOW, "             on action " + action_name)
            dst = prime_env_proc_state[cspVisitorImpl.global_states[state_name][action_name]]
            if (action_name in public_actions):
                #public_env_proc_trans |= (src & public_actions[action_name] & dst)
                #public_env_proc_trans |= (src & public_actions[action_name] & public_actions_bvec_inv & dst)
                public_env_proc_trans |= (src & public_actions[action_name] & public_state_and_actions_bvec_inv & dst)
                cond_print(VERBOSE_LOW, "                 public_trans bdd #nodes="+str(bdd_nodecount(public_env_proc_trans)))
                #public_env_proc_trans |= (src & public_actions[action_name] & all_actions_bvec_inv & dst)
            else:
                #private_env_proc_trans |= (src & private_actions[action_name] & dst)
                #private_env_proc_trans |= (src & private_actions[action_name] & private_actions_bvec_inv & dst)
                private_env_proc_trans |= (src & private_actions[action_name] & private_state_and_actions_bvec_inv & dst)
                cond_print(VERBOSE_LOW, "                 private_trans bdd #nodes="+str(bdd_nodecount(private_env_proc_trans)))
                #private_env_proc_trans |= (src & private_actions[action_name] & all_actions_bvec_inv & dst)

    # Note: the next two lines are not needed if all 1-hot restrictions are taken care of during construction
    #public_env_proc_trans &= env_proc_state_bvec_inv & prime_env_proc_state_bvec_inv
    #private_env_proc_trans &= env_proc_state_bvec_inv & prime_env_proc_state_bvec_inv
    
    env_proc_trans = public_env_proc_trans | private_env_proc_trans 
    # cond_print(VERBOSE_HIGH, "Environment initial BDD:\n\t" + bdd_str(env_proc_init))
    cond_print(VERBOSE_HIGH, "Environment private transitions BDD:\n\t" + bdd_str(private_env_proc_trans))
    cond_print(VERBOSE_HIGH, "Environment public transitions BDD:\n\t" + bdd_str(public_env_proc_trans))
    cond_print(VERBOSE_HIGH, "Environment transitions BDD:\n\t" + bdd_str(env_proc_trans))
    cond_print(VERBOSE_LOW, "----> Done building environment E states, actions and transition system")

    #################################
    ### (c) Env Transition ends
    ### Env completed
    #################################

    cond_print(VERBOSE_LOW, "--> Done building statespace components: r - A_S; q - A_L; e - csp")

    #################################
    ### Computing A_L, A_S, E joint transitions
    #################################

    
    joint_transition = env_proc_trans & safety_trans & liveness_trans
    public_joint_transition = public_env_proc_trans & safety_trans & liveness_trans
    private_joint_transition = private_env_proc_trans & safety_trans & liveness_trans
    
    
    cond_print(VERBOSE_HIGH, "Joint (A_L , A_S, & E) transitions BDD:\n\t" + bdd_str(joint_transition))
    cond_print(VERBOSE_HIGH, "Joint public transitions BDD:\n\t" + bdd_str(public_joint_transition))
    cond_print(VERBOSE_HIGH, "Joint private transitions BDD:\n\t" + bdd_str(private_joint_transition))
    cond_print(VERBOSE_LOW, "----> Done building joint executions of A_S, A_L, E")

    #################################
    ### Completed: Computing A_L, A_S, E joint transitions
    #################################

    #################################
    ### Building utility predicates
    ### (a) enabled_public_action : For public action a is in set of public actions L?
    ### (b) Fixed points - Esink, Efail, Eprivate
    #################################

    #################################
    ### (a) enabled_public_action : Begins
    ##### - 'a' is a selected public action
    ##### - 'L' is a set of enabled public actions
    #################################

    ## Meaning y_set_ai is the collection of all sets containing ai
    ## ai => y_set_ai
    ## NOT one-hot. Since it is a set-theoretic relation.
    
    actions_set = {}

    enabled_public_action = bddtrue
    for action_chan in sorted(cspVisitorImpl.global_transitions.keys()):
        for action_ap in sorted(cspVisitorImpl.global_transitions[action_chan]):
            ## actions are currently unique (no need for channel prefix...).
            if (action_chan != '_internal'):
                actions_set[action_ap] = bdd_ithvar(env_aut.register_ap(bosy_output_prefix + "set_" + action_ap))
                
                enabled_public_action &= bdd_imp(public_actions[action_ap], actions_set[action_ap])
                
    cond_print(VERBOSE_HIGH, "Enabled public actions is:\n\t" + (bdd_str(enabled_public_action)))

    #################################
    ### (a) enabled_public_action : Ends
    ### (b) Fixed point computation begins:
    ### 1. EFail
    ### 2. ESink
    ### 3. Eprivate
    #################################

    cond_print(VERBOSE_LOW, "==> Building FixPoints")

    #########################
    # 1. Efail(r; e; L')
    # (Base case) If r is a final state of A_S, e has no private transitions, and none
    # of its enabled public actions is in L', then Y (r; e; L') is true, and
    # (Induction) If there exists r0; e0 and a private action b such that Y (r0; e0; L'),
    # A_S(r; b; r0) and E(e; b; e0) hold, then Y (r; e; L') holds.
    #########################
    
    #(Base case)
    
    Efail = (
        # r is a final state of A_S
        safety_acc &
        # e has no private transitions
        bdd_not(
            #states of env from which transition on private action exists
            #Recall -  private-env-transition  also contains public-actions
            bdd_exist(private_env_proc_trans, private_actions_vars & public_actions_vars & prime_env_proc_state_vars)
        ) & 
        # none of its enabled public actions is in L  
        bdd_not(
            bdd_exist(
                #recall - public env transition includes private actions. 
                bdd_exist(public_env_proc_trans, prime_env_proc_state_vars &  private_actions_vars) & enabled_public_action,
                public_actions_vars
            )
        ) &
        # Make environment actions one-hot
        env_proc_state_bvec_inv 
    )

    #(Efail Fixed point computation begins)
    
    cond_print(VERBOSE_HIGH, "----> Least FixPoint Efail -------------------")
    cond_print(VERBOSE_HIGH, "Efail-init: " + bdd_str(Efail))
    Efail_prev = bddfalse
    while (Efail != Efail_prev):
        Efail_prev = Efail
        #renaming variables
        prime_Efail = bdd_exist(
            Efail & env_proc_state_id & safety_state_id,
            env_proc_state_vars & safety_state_vars)

        Efail |= bdd_exist(
            #private env transition includes public actions -- to be quantified out 
            #private_safety_trans & bdd_exist(private_env_proc_trans, public_actions_vars) & prime_Efail,
            safety_trans & private_env_proc_trans & prime_Efail,
            private_actions_vars  & public_actions_vars & prime_env_proc_state_vars & prime_safety_state_vars
        )
        cond_print(VERBOSE_HIGH, "Efail-diff: " + bdd_str(Efail & bdd_not(Efail_prev)))

    #print(bdd_str(private_safety_trans))
    #print(bdd_str(private_env_proc_trans))
    #print(bdd_str(bdd_exist(private_env_proc_trans, public_actions_vars)))
    #print(bdd_str(private_safety_trans & private_env_proc_trans & prime_Efail))
    #print("prime env states\n\t:" + bdd_str(prime_env_proc_state_vars))
    #print("quantified out prime env states\n\t:" + bdd_str(bdd_exist(prime_env_proc_state_vars, public_actions_vars)))
    
    cond_print(VERBOSE_HIGH, "Efail-final: " + bdd_str(Efail))

    cond_print(VERBOSE_HIGH, "Negation of Efail:\n\t:" + bdd_str(bdd_not(Efail)))

    cond_print(VERBOSE_HIGH, "Negation of Efail with one-hot:\n\t:" + bdd_str(bdd_not(Efail) & env_proc_state_bvec_inv  & safety_state_bvec_inv))
    
    #########################
    ## 1. Efail complete
    #########################

    #############################################
    #2. Esink(e, a, L) begins
    #Esink(e, a , L) holds if one of the two occurs:
    #(a) a is not present in set L
    #(b) There is no sequence of private transitons in E from state 'e' from which action 'a' is enabled.
    #############################################
     
    #Initializing Esink:
    Esink = bddfalse

    #Adding condition (a) first
    # Not made one-hot, since set-theoretic relation
    Esink |= bdd_not(enabled_public_action)
    cond_print(VERBOSE_HIGH, "Part(a) of Esink:\n\t"+bdd_str(Esink))
    
    #Adding condition for (b)
    #First construct a predicate for the closure of private transitions in the environment. Predicate is called enabled_state_public_action
    #Fixed point computation
    cond_print(VERBOSE_HIGH, "----> Least FixPoint enabled_state_public_action ----------------")
    
    #Base case
    # public env. transition includes private actions -- should be quantified out
    enabled_state_public_action = bdd_exist(public_env_proc_trans, prime_env_proc_state_vars &  private_actions_vars)
    cond_print(VERBOSE_HIGH, "enabled_public_state_action-init: " + bdd_str(enabled_state_public_action))
    prev_enabled_state_public_action = bddfalse
    while(enabled_state_public_action != prev_enabled_state_public_action):
        prev_enabled_state_public_action = enabled_state_public_action

        #rename varibles
        prime_enabled_state_public_action = bdd_exist(
            enabled_state_public_action &
            env_proc_state_id,
            env_proc_state_vars
            )

        # private env transition includes public actions from transition, which is other than public actions in prime_enabled_..
        # So, public actions in private env. transition must be removed before conjuction with prime_enabled_...
        # finally, private actions should be removed
        enabled_state_public_action |= bdd_exist(
            bdd_exist(private_env_proc_trans, public_actions_vars) & prime_enabled_state_public_action,
            prime_env_proc_state_vars & private_actions_vars
            )

        cond_print(VERBOSE_HIGH, "enabled_state_public_action-diff: " + bdd_str(enabled_state_public_action & bdd_not(prev_enabled_state_public_action)))
         
    
    cond_print(VERBOSE_HIGH, "enabled_state_public_action:\n\t" + bdd_str(enabled_state_public_action))

    # esink_b is made one-hot.
    # not necessary for later parts of the code.
    # Made one-hot here to ensure that esink is exactly what we expect it to be. -- for clarity of intermediate steps.
    esink_b = bdd_exist(bdd_not(enabled_state_public_action) & env_proc_state_bvec_inv & public_actions_bvec_inv, private_actions_vars)
    
    cond_print(VERBOSE_HIGH, "Part(b) of Esink:\n\t"+bdd_str(esink_b))

    Esink |= esink_b
    cond_print(VERBOSE_HIGH, "Esink:\n\t " + bdd_str(Esink))

    cond_print(VERBOSE_HIGH, "Negation of Esink:\n\t " + bdd_str(bdd_not(Esink)))

    cond_print(VERBOSE_HIGH, "Negation of Esink with one-hot:\n\t " + bdd_str(bdd_not(Esink) & env_proc_state_bvec_inv & public_actions_bvec_inv_temp))

    
    #########################
    ## 2. Esink complete
    #########################

    #########################
    ##3. Eprivate begins
    
    # #Eprivate((q; r; e); g; (q'; r'; e')) -- There is an execution of 0 or more private transitions only from (q,r,e) to (q',e',r'), g is true iff at least one intermediate state q is accepting in A_L.
    ####  - 'g' is a green marker
    
    ## (Base case) If q = q'; r = r'; e = e' then Z((q; r; e); g; (q'; r'; e')) holds, and g is true iff q is green,
    ## (Induction) If Z((q; r; e); g0; (q0; r0; e0)) and J((q0; r0; e0); b; (q'; r'; e')), then
    ## Z((q; r; e); g; (q'; r'; e')) holds, with g being true if g0 is true or q' is green.
    #########################

    #Define green variable
    green_var = bdd_ithvar(env_aut.register_ap("_green_"))
    mid0_green_var = bdd_ithvar(env_aut.register_ap("_mid0_green_"))
    mid0_green_id = bdd_biimp(green_var, mid0_green_var)
    mid1_green_var = bdd_ithvar(env_aut.register_ap("_mid1_green_"))
    mid1_green_id = bdd_biimp(green_var, mid1_green_var)

    cond_print(VERBOSE_HIGH, "----> Least FixPoint Eprivate ----------------")

    #Base case
    
    Eprivate = (
        # no change to the state
        safety_state_id & liveness_state_id & env_proc_state_id &
        # green iff accepting 
        bdd_biimp(green_var, liveness_acc)
    )

    cond_print(VERBOSE_HIGH, "\nEprivate-init\n\t: " + bdd_str(Eprivate))
    
    # Inducation step
    Eprivate_prev = bddfalse
    while (Eprivate != Eprivate_prev):
        Eprivate_prev = Eprivate
        
        # make predicate: Z((q; r; e); g0; (q0; r0; e0)) from Z(regular to prime) 
        mid0_Z = bdd_exist(
            Eprivate &
            mid0_green_id &
            mid0_prime_env_proc_state_id &
            mid0_prime_safety_state_id &
            mid0_prime_liveness_state_id,
            green_var & prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars
        )
        
        # predicate: J((q0; r0; e0); b; (q'; r'; e')) from private_joint_transitions from regular to prime
        # private joint transition also has public actions -- to quantify out these
        mid0_private_joint_transition = bdd_exist(
            private_joint_transition &
            mid0_env_proc_state_id &
            mid0_safety_state_id &
            mid0_liveness_state_id,
            env_proc_state_vars & safety_state_vars & liveness_state_vars & public_actions_vars
        )
        #print("Mid0_Private_joint_tarnsition\n\t"+bdd_str(mid0_private_joint_transition))
        
        Eprivate |= bdd_exist(
            mid0_Z &
            mid0_private_joint_transition &
            bdd_biimp(green_var, mid0_green_var | prime_liveness_acc),
            #SB Edit
            #mid0_green_var & mid0_env_proc_state_vars & mid0_safety_state_vars & mid0_liveness_state_vars & private_actions_vars
            mid0_green_var & mid0_env_proc_state_vars & mid0_safety_state_vars & mid0_liveness_state_vars & private_actions_vars
        )
        cond_print(VERBOSE_HIGH, "\nEprivate-diff\n\t:" + bdd_str(Eprivate & bdd_not(Eprivate_prev)))

    cond_print(VERBOSE_HIGH, "Eprivate-final: " + bdd_str(Eprivate))


    #########################
    ## 2. Eprivate complete
    #########################
    
    #############################################
    ## Preparing compound transition for non-trivial transition in (q,r,e)-(a,L,g) automaton
    ## compound_transition((q,r,e),(a,L,g),(q',r',e')) iff
    ## exist (q0,r0,e0, g0) and (q1,r1,e1, g1) and public action s s.t.
    ###### Eprivate((q,r,e), g0, (q0,r0,e0)) & --- bullet1
    ###### public joint action from (q0,r0,e0) on a to (q1,r1,e1) & ---- bullet2
    ###### Eprivate((q0,r0,e0), g1, (q1,r1,e1)) & ------- bullet3
    ###### g = g0 or g1
    #############################################

    
    #bullet1 -- Eprivate from regular to 0-states
    bullet1 = bdd_exist(
        Eprivate &
        mid0_green_id &
        mid0_prime_env_proc_state_id &
        mid0_prime_safety_state_id &
        mid0_prime_liveness_state_id,
        green_var & prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars
    )

    #bullet2 -- public joint transition between between 0-state to 1-state
    # public joint transition includes private actions, must be quantified out
    bullet2 = bdd_exist(
        public_joint_transition &
        mid0_env_proc_state_id &
        mid0_safety_state_id &
        mid0_liveness_state_id &
        mid1_prime_env_proc_state_id &
        mid1_prime_safety_state_id &
        mid1_prime_liveness_state_id,
        env_proc_state_vars & safety_state_vars & liveness_state_vars &
        prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars & private_actions_vars 
    )

    #bullet3 -- Eprivate from 1-states to prime-states
    bullet3 = bdd_exist(
        Eprivate &
        mid1_green_id &
        mid1_env_proc_state_id &
        mid1_safety_state_id &
        mid1_liveness_state_id,
        green_var & env_proc_state_vars & safety_state_vars & liveness_state_vars
    )

    #print("Bullet3 - 1-state to prime-state:\n\t"+bdd_str(bullet3))
    
    bullet4 = bdd_biimp(green_var, mid0_green_var | mid1_green_var)  

    compound_transition = bdd_exist(bullet1 & bullet2 & bullet3 & bullet4,
                                    mid0_green_var & mid0_env_proc_state_vars & mid0_safety_state_vars & mid0_liveness_state_vars &
                                    mid1_green_var & mid1_env_proc_state_vars & mid1_safety_state_vars & mid1_liveness_state_vars)
    
    cond_print(VERBOSE_HIGH, "\n Compound transitions :\n\t" + bdd_str(compound_transition))
    
    cond_print(VERBOSE_LOW, "===>Completed building utility predicates and fixpoints")



    #########################
    ## 2. Compound transition complete
    #########################

    #########################
    ## Building noSynch
    #########################
    #########################
    ## (a) enabled_state_set : set L is enabled in state e if no enabled public action from e is contained in L
    ## (b) Generalized EPrivate (q,r,e,L)
    #########################

    ##########################
    ## (a) enabled_state_set begins
    ##Predicate enabled_state_set(e, L) := public_actions(e) \intersect L = empty
    ##enabled_state_set is not in one-hot since it is  a set theoretic predicate.
    
    ## states given in prime form, since that is what we use in the GenEPrivate construction
    ##########################
    
    enabled_state_set = bddtrue
    for state_name in env_state_names:
        src = prime_env_proc_state[state_name]
        #using prime states since only those are used  in Generalized EPrivate
        remove_sets = bddtrue
        for action_name in cspVisitorImpl.global_states[state_name]:
            if (action_name in public_actions):
                remove_sets &= bdd_not(actions_set[action_name])
        #print("Remove sets for state " + bdd_str(src) + " is " + bdd_str(remove_sets))
        #print("new clause is " + bdd_str(bdd_imp(src, remove_sets)))
        enabled_state_set &= bdd_imp(src, remove_sets)
        #print("enabled sets so far is " + bdd_str(enabled_state_set))

    cond_print(VERBOSE_HIGH, "Enabled state set is:\n\t" + (bdd_str(enabled_state_set)))

    
    ##############################
    ## (a) enabled_state_set ends
    ##############################

    #########################
    ##3. GenEprivate begins
    
    ## GenEprivate((q; r; e); g; L'; (q'; r'; e')) -- There is an execution of 0 or more private transitions only from (q,r,e) to (q',e',r'), g is true iff at least one intermediate state q is accepting in A_L and L does not interset with enabled actions from any state on the path
    ####  - 'g' is a green marker
    #### - 'L' is a set of public actions
    
    ## (Base case) If q = q'; r = r'; e = e' then ZG((q; r; e); g; L'; (q'; r'; e')) holds, g is true iff q is green, and L \intersect enabled_public_actions(e') = \emptyset 
    ## (Induction) If ZG((q; r; e); g0; L; (q0; r0; e0)) and J((q0; r0; e0); b; L, (q'; r'; e')), L' \intersect enabled_public_actions(e') = \emptyset , then
    ## ZG((q; r; e); g; L'; (q'; r'; e')) holds, with g being true if g0 is true or q' is green.
    ## NOTE:: L is the same in the indction step. *** this is taken care of implicity in the code 
    #########################

    
    cond_print(VERBOSE_HIGH, "----> Least FixPoint GenEprivate ----------------")

    #Base case
    
    GenEprivate = (
        # no change to the state
        safety_state_id & liveness_state_id & env_proc_state_id &
        # enabled_public_action(prime state) \interesct L = \emptyest
        enabled_state_set &
        # green iff accepting 
        bdd_biimp(green_var, liveness_acc)
    )

    cond_print(VERBOSE_HIGH, "\nGenEprivate-init\n\t: " + bdd_str(GenEprivate))
    
    # Induction step
    GenEprivate_prev = bddfalse
    while (GenEprivate != GenEprivate_prev):
        GenEprivate_prev = GenEprivate
        
        # make predicate: Z((q; r; e); g0; L;  (q0; r0; e0)) from Z(regular to prime) 
        mid0_Z_Gen = bdd_exist(
            #prime env state in GenEPrivate converted to 0-states, L is not changed. L is in non-prime form.  
            GenEprivate &
            mid0_green_id &
            mid0_prime_env_proc_state_id &
            mid0_prime_safety_state_id &
            mid0_prime_liveness_state_id,
            green_var & prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars
        )

        
        # predicate: J((q0; r0; e0); b; (q'; r'; e')) from private_joint_transitions from regular to prime
        # private joint transition also has public actions -- to quantify out these
        # enabled_state_set is applied to prime env states only (env. states are prime, L is not prime) 
        mid0_private_joint_transition_Gen = bdd_exist(
            private_joint_transition &
            mid0_env_proc_state_id &
            mid0_safety_state_id &
            mid0_liveness_state_id &
            #state are prime, L is not prime in enabled_state_set. This is the same L in mid0_Z
            enabled_state_set,
            env_proc_state_vars & safety_state_vars & liveness_state_vars & public_actions_vars
        )

        #print("Mid0_Private_joint_tarnsition\n\t"+bdd_str(mid0_private_joint_transition_Gen))
        
        GenEprivate |= bdd_exist(
            mid0_Z_Gen &
            mid0_private_joint_transition_Gen &
            bdd_biimp(green_var, mid0_green_var | prime_liveness_acc),
            mid0_green_var & mid0_env_proc_state_vars & mid0_safety_state_vars & mid0_liveness_state_vars & private_actions_vars
        )

        #cond_print(VERBOSE_HIGH, "\nGenEprivate\n\t:" + bdd_str(GenEprivate))
        
        cond_print(VERBOSE_HIGH, "\nGenEprivate-diff\n\t:" + bdd_str(GenEprivate & bdd_not(GenEprivate_prev)))

    cond_print(VERBOSE_HIGH, "GenEprivate-final: " + bdd_str(GenEprivate))


    #############################################
    ### 
    ### noSynch(q,r,e,L) if
    ### (a) exists q0, r0, e0,  g, q1, r1, e1, g1, private_action b s.t.
    ###       EPrivate(q,r,e,g, q0,r0,e0) and
    ###       private_joint_transition (q0,r0,e0, b, q1,r1,e1) and
    ###       GenEPrivate(q1,r1,e1,g1,L,q0,r0,e0) and
    ###       g1
    ###
    #############################################

    #noSynch1 -- Eprivate from regular to 0-states without green var
    noSynch1 = bdd_exist(
        Eprivate &
        mid0_prime_env_proc_state_id &
        mid0_prime_safety_state_id &
        mid0_prime_liveness_state_id,
        prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars &
        green_var
    )

    # predicate: J((q0; r0; e0); b; (q1; r1; e1)) from private_joint_transitions from regular to prime
    # private joint transition also has public actions -- to quantify out these
    noSynch_private_joint_transition = bdd_exist(
        private_joint_transition &
        mid0_env_proc_state_id &
        mid0_safety_state_id &
        mid0_liveness_state_id &
        mid1_prime_env_proc_state_id &
        mid1_prime_safety_state_id &
        mid1_prime_liveness_state_id,
        env_proc_state_vars & safety_state_vars & liveness_state_vars & 
        prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars &
        public_actions_vars
    )
     
        
      
    #noSynch2 -- GenEprivate from 1 to 0
    noSynch2 = bdd_exist(
        GenEprivate &
        mid1_green_id &
        mid1_env_proc_state_id &
        mid1_safety_state_id &
        mid1_liveness_state_id &
        mid0_prime_env_proc_state_id &
        mid0_prime_safety_state_id &
        mid0_prime_liveness_state_id,
        green_var &
        env_proc_state_vars & safety_state_vars & liveness_state_vars &
        prime_env_proc_state_vars & prime_safety_state_vars & prime_liveness_state_vars
    )

    noSynch = bdd_exist(
        noSynch1 & noSynch_private_joint_transition & noSynch2 & mid1_green_var,
        mid1_green_var &
        mid0_env_proc_state_vars & mid0_safety_state_vars & mid0_liveness_state_vars &
        mid1_env_proc_state_vars & mid1_safety_state_vars & mid1_liveness_state_vars &
        private_actions_vars
        )

    cond_print(VERBOSE_HIGH, "\n noSynch :\n\t" + bdd_str(noSynch))


    
    
    #############################################
    ## noSynch ends. 
    #############################################

 
    
    ###########################################################################
    ## Building (q,r,e), (a,L,g) automaton
    ## Actions encodes the transitions in the system (a,L,g), where:
    ## - 'a' is a selected public action
    ## - 'L' is a set of enabled public actions
    ## - 'g' is a green marker
    ##
    ## NEXT: currently XOR selected public action 'a' --> reduce to bitvec log(N) bits representation
    ## * For 'L' we need to be able to work with a set of actions, we cannot use
    ##   log(actions) bits and each has its own BDD representation.
    ###########################################################################
    
    cond_print(VERBOSE_LOW, "==> Building transitions (a,L,g)")
    
    
    ###########################################################################
    ## Creating the extra needed variables for the sink and fail states
    ###########################################################################
    #final_aut = spot.make_twa_graph(bdict)
    aux_aut = spot.make_twa_graph(bdict)
    ##
    aux_state = {}
    prime_aux_state = {}
    aux_state[0] = bdd_ithvar(aux_aut.register_ap("_fail_state"))
    prime_aux_state[0] = bdd_ithvar(aux_aut.register_ap("_pri_fail_state"))
    aux_state[1] = bdd_ithvar(aux_aut.register_ap("_sink_state"))
    prime_aux_state[1] = bdd_ithvar(aux_aut.register_ap("_pri_sink_state"))

    fail_state = aux_state[0]
    prime_fail_state = prime_aux_state[0]
    sink_state = aux_state[1]
    prime_sink_state = prime_aux_state[1]
    ## vars (for quantification)
    aux_state_vars = build_vars(aux_state)
    prime_aux_state_vars = build_vars(prime_aux_state)

    aux_state_id = bdd_biimp(fail_state, prime_fail_state) & bdd_biimp(sink_state, prime_sink_state)
    
    ###########################################################################
    ## Final automaton -- 
    ## Building initial/transition/accepting of the final automaton 
    ###########################################################################


    #########################################################
    ## Building automaton for the (q,r,e)-(a,L,g) automaton.
    #########################################################

    #############################################
    ## State space of the automaton. (Legal state)
    #(a) (q,r,e), or
    #(b) fail or sink
    #############################################

    noqre = bddtrue
    prime_noqre = bddtrue
    for state_name in env_state_names:
        src = env_proc_state[state_name]
        noqre &= bdd_not(src)
        src = prime_env_proc_state[state_name]
        prime_noqre &= bdd_not(src)
    for state_name in safety_state:
        src = safety_state[state_name]
        noqre &= bdd_not(src)
        src = prime_safety_state[state_name]
        prime_noqre &= bdd_not(src)
    for state_name in liveness_state:
        src = liveness_state[state_name]
        noqre &= bdd_not(src)
        src = prime_liveness_state[state_name]
        prime_noqre &= bdd_not(src)
        
    ## Create (q,r,e) states -- called legalstates
    
    legalstate = safety_state_bvec_inv & liveness_state_bvec_inv &  env_proc_state_bvec_inv & bdd_not(fail_state)  & bdd_not(sink_state)
    
    #Repeat for prime versions
    prime_legalstate = prime_safety_state_bvec_inv & prime_liveness_state_bvec_inv & prime_env_proc_state_bvec_inv & bdd_not(prime_fail_state)  & bdd_not(prime_sink_state)
    
    
    cond_print(VERBOSE_HIGH, "(q,r,e) states:\n\t" + bdd_str(legalstate))
    cond_print(VERBOSE_HIGH, "prime (q,r,e) states:\n\t" + bdd_str(prime_legalstate))    

    #############################################
    ## Transitions of the automaton. 
    #############################################

    #########################################
    ## IMPORTANT NOTE #######################
    ## This automaton should not contain private actions in the transition function.
    ## We use public_actions_bvec_inv_temp to ensure one-hot encoding on public actions only (and not include private actions)
    #########################################

    #####Transition Type1
    ##If source is either sink or fail,  self loop

    transition_sink_loop = sink_state & bdd_not(fail_state) & noqre  & prime_sink_state & bdd_not(prime_fail_state) & prime_noqre 
    transition_fail_loop = fail_state & bdd_not(sink_state) & noqre  & prime_fail_state & bdd_not(prime_sink_state) & prime_noqre
    
    cond_print(VERBOSE_MID, "Cond 1, when source is either sink or fail:\n\t Sink: " + bdd_str( transition_sink_loop) + "\n\t Fail: "+ bdd_str( transition_fail_loop))

    ###### When source is not sink or fail.
    
    #####Transition Type2
    ##If source state is not legal, goto sink state
     
    #transition_source_not_legal = bdd_not(legalstate) & bdd_not(sink_state) & bdd_not(fail_state) & prime_sink_state & bdd_not(prime_fail_state) & prime_noqre
    #cond_print(VERBOSE_MID, "Cond 2, when source state is not sink or fail and is not legal:\n\t" + bdd_str(transition_source_not_legal))

    #####Transition Type3
    ##If src is legal,  but public action is not one-hot, goto sink
    #transition_illegalaction = legalstate & bdd_not(public_actions_bvec_inv_temp) & prime_sink_state & bdd_not(prime_fail_state)
    
    #transition_illegalaction = legalstate & bdd_not(sink_state) & bdd_not(fail_state) & bdd_not(public_actions_bvec_inv_temp) & prime_sink_state & bdd_not(prime_fail_state) & prime_noqre
    
    #transition_illegalaction = legalstate & bdd_not(public_actions_bvec_inv_temp) & prime_sink_state & bdd_not(prime_fail_state) & prime_noqre
    #cond_print(VERBOSE_MID, "Cond 3, when source is legal but input action is not:\n\t " + bdd_str(transition_illegalaction))



    
    #print(bdd_str(bdd_not(legalstate) & bdd_not(sink_state) & bdd_not(fail_state)))

    #####Transition Type4
    ##If src is legal  public_action is one-hot, but current state is neither sink nor fail, follow transitions from automaton construction
    
    ### Transition Type4A
    ### Transitions that go to Fail

    ###Transition Type4A.1
    
    ##If EFail holds, goto Fail
    #transition_efail = legalstate & bdd_not(sink_state) & bdd_not(fail_state) ## legal q,r,e, state
    transition_efail = legalstate  ## legal q,r,e, state
    transition_efail &= public_actions_bvec_inv_temp ## one-hot aciton
    transition_efail &= Efail # Efail holds
    transition_efail &= prime_fail_state & bdd_not(prime_sink_state) & prime_noqre# goto fail

    #print("testing bdd size")
    #print(bdd_str(transition_efail))
    #print("5: " + bdd_str(astate & transition_efail))

    cond_print(VERBOSE_MID, "Cond 4A.1, when EFail holds:\n\t " + bdd_str(transition_efail))

    ###Transition Type4A.2
    
    ##if noSynch holds, goto Fail
    #transition_noSynch = legalstate & bdd_not(sink_state) & bdd_not(fail_state) ## legal q,r,e, state
    transition_noSynch = legalstate ## legal q,r,e, state
    transition_noSynch &= public_actions_bvec_inv_temp ## one-hot aciton
    transition_noSynch &= noSynch #noSynch holds
    transition_noSynch &= prime_fail_state & bdd_not(prime_sink_state) & prime_noqre # goto fail

    cond_print(VERBOSE_MID, "Cond 4A.2, when noSynch holds:\n\t " + bdd_str(transition_noSynch))

    
    ### Transition Type4B
    ### Transitions that go to Sink
    
    ##If EFail does not hold and noSynch does not hold but ESink holds, goto Sink
    transition_esink = legalstate & bdd_not(sink_state) & bdd_not(fail_state) ## legal q,r,e state
    transition_esink &= public_actions_bvec_inv_temp # one-hot action
    transition_esink &= bdd_not(Efail) # Efail false
    transition_esink &= bdd_not(noSynch) # noSynch is false
    transition_esink &= Esink # esink holds
    transition_esink &= prime_sink_state & bdd_not(prime_fail_state) & prime_noqre # goto Sink
    
    cond_print(VERBOSE_MID, "Cond 4B, when Esink holds:\n\t " + bdd_str(transition_esink))


    ### Transition Type4C
    ### Transitions that go to (q,r,e)
    
    ##If EFail, noSynch and Esink do not hold, follow bullet transitions
    #transition_joint = legalstate & bdd_not(sink_state) & bdd_not(fail_state) #src q,r,e state is legal
    #transition_joint &= prime_legalstate & bdd_not(prime_sink_state) & bdd_not(prime_fail_state) #dest q,r,e state is legal

    transition_joint = legalstate  #src q,r,e state is legal
    transition_joint &= prime_legalstate  #dest q,r,e state is legal
    transition_joint &= compound_transition # makes connections with states 
    transition_joint &= bdd_not(Efail) & bdd_not(Esink) & bdd_not(noSynch) # #esink, efail and noSynch  are false
    transition_joint &= public_actions_bvec_inv_temp # one-hot
    
    cond_print(VERBOSE_MID, "Cond 4C, final compound transition:\n\t " + bdd_str(transition_joint))
    

    ###Final transition of (q,r,e)-(a,L,g) automaton
    #final_transitions = transition_source_not_legal | transition_illegalaction | transition_sink_loop | transition_fail_loop | transition_efail | transition_noSynch | transition_esink | transition_joint


    #REMOVED legal source state
    #final_transitions =  transition_illegalaction | transition_sink_loop | transition_fail_loop | transition_efail | transition_noSynch | transition_esink | transition_joint

    ## TESTING
    #REMOVED legal aphabet as well 
    final_transitions =   transition_sink_loop | transition_fail_loop | transition_efail | transition_noSynch | transition_esink | transition_joint

    cond_print(VERBOSE_HIGH, "Final BDD Nodes: " + str(bdd_nodecount(final_transitions)))

    #exit()
    #########################################################
    ## Completed Building automaton for the (q,r,e)-(a,L,g) automaton.
    #########################################################
    
    #############################################
    ## Building the final specification automaton from the transition relation
    ## Building automaton inside spot
    #############################################


    ### Creating the final Buchi automaton for BoSy

    final_aut = spot.make_twa_graph(bdict)
    final_aut.set_buchi()
    # Pretend accepting condition is state-based. 
    final_aut.prop_state_acc(True)
    
    ################################################
    ### Creating state space of final_aut
    ###### (a).  Adding the sink and fail states 
    ###### (b).  Adding the (q,r,e) states later
    ################################################

    
    final_aut_state_bdds = {}
    #final_aut_state_numbers = {}
    accepting_indices = {} 
    state_tuple_number_id = {}

    accept = "accept"
    nonaccept = "nonaccept"
    
    ################################################
    ###### (a).  Adding the sink and fail states 
    ################################################
    
    ### fail state gets no. 0
    ### fail state is an accepting state

    fail_idx = final_aut.new_state()
    final_aut_state_bdds[fail_idx] = fail_state & bdd_not(sink_state) & noqre
    accepting_indices[fail_idx] = True
    
    ### sink state gets no. 1.
    ### sink state is not an accepting state

    sink_idx = final_aut.new_state()
    final_aut_state_bdds[sink_idx] = sink_state & bdd_not(fail_state) & noqre
    accepting_indices[sink_idx] = False

    ################################################
    ###### (a).  Done - Adding the sink and fail states
    ###### (b).  Adding (q,r,e) states - begin
    ################################################

    def make_state_id(safe,live,env):
        return "_".join([str(safe), str(live), str(env)])

    
    for safety_idx in sorted(safety_state.keys()):
        for liveness_idx in sorted(liveness_state.keys()):
            for env_proc_idx in sorted(env_proc_state.keys()):

                state_tuple_string = make_state_id(safety_idx, liveness_idx, env_proc_idx)
                state_tuple_number_id[state_tuple_string] = {}

                #print(state_tuple_number_id)

                
                # state_bdd is : 
                state_prop = (safety_state[safety_idx] & safety_state_bvec_inv &
                              liveness_state[liveness_idx] & liveness_state_bvec_inv &
                              env_proc_state[env_proc_idx] & env_proc_state_bvec_inv &
                              bdd_not(fail_state) &
                              bdd_not(sink_state))



                ############### green form
                ############### is an accepting state
                ############### Numbers are even beginning from 2
                
                green_new_state_idx = final_aut.new_state()
                state_tuple_number_id[state_tuple_string][accept] = green_new_state_idx
                final_aut_state_bdds[green_new_state_idx] =  state_prop
                accepting_indices[green_new_state_idx] = True
            
                
                ############### non-green form
                ############### is a non-accepting state
                ############### Numbers are odd beginning from 3

                non_green_new_state_idx = final_aut.new_state()
                state_tuple_number_id[state_tuple_string][nonaccept] = non_green_new_state_idx      
                final_aut_state_bdds[non_green_new_state_idx] =  state_prop
                accepting_indices[non_green_new_state_idx] = False

                
                ################ is the state the initial state?
                ################ we require there is a unique initial state
                
                if ( (safety_idx == safety_spec_aut.get_init_state_number()) &
                     (liveness_idx == liveness_spec_aut.get_init_state_number()) &
                     (env_proc_idx == cspVisitorImpl.initial[0]) ):


                    #Note: can be changed to either state as accepting. Accepting init state may be better. 
                    for edge in liveness_spec_aut.out(liveness_idx):
                        if (edge.acc.count() != 0):
                            #init_state = green_new_state_idx
                            init_state = state_tuple_number_id[state_tuple_string][accept]
                        else:
                            #init_state = non_green_new_state_idx
                            init_state = state_tuple_number_id[state_tuple_string][nonaccept]
                            
                    final_aut.set_init_state(init_state)

    ################################################
    ###### (a).  Adding (q,r,e) states - end
    ###### (b)   Building transiitons
    ################################################


    num_states = final_aut.num_states()
    cond_print(VERBOSE_HIGH, "\n\nNumber of states is " + str(num_states)+"\n\n")
    cond_print(VERBOSE_HIGH, "Initial state is " + str(init_state) + "\n\n")

    #actions_set_vars = build_vars(actions_set)
    
    for i in range(num_states):

        ## is src state an accepting state?
        
        if accepting_indices[i]:
            src_is_accepting = True
        else:
            src_is_accepting = False

        ## BDD of src state
        
        src_state = final_aut_state_bdds[i]
        cond_print(VERBOSE_HIGH, "state " + str(i) + "  " + bdd_str(src_state))
        
        
        transitions_from_src = bdd_exist(final_transitions & src_state,
                                         safety_state_vars  & liveness_state_vars  & env_proc_state_vars & aux_state_vars)
        cond_print(VERBOSE_HIGH, "Transitions from source  are: \n\t" + bdd_str(transitions_from_src) + "\n" )

        
        ### Obtain transitions that go to fail (fail state is indexed by fail_idx in final_aut)
        
        dest_state = prime_fail_state & bdd_not(prime_sink_state) & prime_noqre
        src_to_dest = bdd_exist(transitions_from_src & dest_state,
                                prime_safety_state_vars  & prime_liveness_state_vars  & prime_env_proc_state_vars & prime_aux_state_vars)

        if (src_to_dest != bddfalse):
            cond_print(VERBOSE_HIGH, "\t" + "transitions to " + bdd_str(dest_state) + " \n\t\t" + bdd_str(src_to_dest) + "\n" )
        
            ### Add transition to final_aut
            if src_is_accepting:
                final_aut.new_edge(i, fail_idx, src_to_dest, [0])
            else:
                final_aut.new_edge(i, fail_idx, src_to_dest)
            

        ### Obtain transitions that go to sink (sink state is indexed by sink_idx in final_aut)

        dest_state = bdd_not(prime_fail_state) & prime_sink_state & prime_noqre
        src_to_dest = bdd_exist(transitions_from_src & dest_state,
                                prime_safety_state_vars  & prime_liveness_state_vars  & prime_env_proc_state_vars & prime_aux_state_vars)

        if (src_to_dest != bddfalse):
            cond_print(VERBOSE_HIGH, "\t" + "transitions to " + bdd_str(dest_state) + " \n\t\t" + bdd_str(src_to_dest) + "\n" )

            ### Add transition to final_aut
            if src_is_accepting:
                final_aut.new_edge(i, sink_idx, src_to_dest, [0])
            else:
                final_aut.new_edge(i, sink_idx, src_to_dest)
            
        
        ### Obtain remaining q,r,e states
        
        for safety_idx in sorted(safety_state.keys()):
            for liveness_idx in sorted(liveness_state.keys()):
                for env_proc_idx in sorted(env_proc_state.keys()):

                    dest_state = prime_safety_state[safety_idx] & prime_liveness_state[liveness_idx] & prime_env_proc_state[env_proc_idx] & bdd_not(prime_sink_state) & bdd_not(prime_fail_state)
                    src_to_dest = bdd_exist(transitions_from_src & dest_state,
                                prime_safety_state_vars  & prime_liveness_state_vars  & prime_env_proc_state_vars & prime_aux_state_vars)

                    dest_state_string  = make_state_id(safety_idx, liveness_idx, env_proc_idx)

                    ## when green on transition is true
                    ## then destination is an accepting state
                    
                    src_to_dest_accepting_trans = bdd_exist(green_var & src_to_dest,
                                                            green_var)

                    if (src_to_dest_accepting_trans != bddfalse):
                        dest_state_accept_num = state_tuple_number_id[dest_state_string][accept]
                        cond_print(VERBOSE_HIGH, "\t" + "transitions to accepting " + bdd_str(dest_state) + " and state number " + str(dest_state_accept_num) + " \n\t\t" + bdd_str(src_to_dest_accepting_trans)  + "\n" )
                   
                        if src_is_accepting:
                            final_aut.new_edge(i, dest_state_accept_num, src_to_dest_accepting_trans, [0])
                        else:
                            final_aut.new_edge(i, dest_state_accept_num, src_to_dest_accepting_trans)


                    ## when green on transition is false
                    ## then destination is a nonaccepting state
                    
                    src_to_dest_nonaccepting_trans = bdd_exist(bdd_not(green_var) & src_to_dest,
                                                               green_var)

                    if (src_to_dest_nonaccepting_trans != bddfalse):
                        dest_state_nonaccept_num = state_tuple_number_id[dest_state_string][nonaccept]
                        cond_print(VERBOSE_HIGH, "\t" + "transitions to nonaccepting " + bdd_str(dest_state) + " and state number " + str(dest_state_nonaccept_num) + " \n\t\t" + bdd_str(src_to_dest_nonaccepting_trans)  + "\n" )
                        if src_is_accepting:
                            final_aut.new_edge(i, dest_state_nonaccept_num, src_to_dest_nonaccepting_trans, [0])
                        else:
                            final_aut.new_edge(i, dest_state_nonaccept_num, src_to_dest_nonaccepting_trans)

                    

    ####################################
    ##  Transitions entered
    ##  final_aut completed
    ####################################
    
                
    # Adding optimization to reduce the size of the automata
    # Documentation at https://spot.lrde.epita.fr/tut30.html

    cond_print(VERBOSE_HIGH, "Number of states in spec aut is " + str(final_aut.num_states()))

    optimize_spin_file(final_aut, spin_file_temp, spin_file)
    
    write_bosy_output(final_aut, spin_file, bosy_file)
   

def main(args):
    if (False):
        print("-e is: " + str(args.env_file))
        print("-s is: " + str(args.safety_spec))
        print("-l is: " + str(args.liveness_spec))
        print("-o is: " + str(args.base_file_path))
        print("-v is: " + str(args.verbosity))
    
    env_file = args.env_file
    safety_spec = normalize(args.safety_spec)
    liveness_spec = normalize(args.liveness_spec)
    bosy_file = open(args.base_file_path + ".bosy", "w+")
    spin_file = open(args.base_file_path + ".spin", "w+")
    spin_file_temp = open(args.base_file_path + ".temp.spin", "w+")
    verbosity = args.verbosity
    
    ##
    set_verbosity(verbosity)
    ## parsing csp
    load_csp_file(env_file)
    ## building transitions 
    build_bosy_instance(safety_spec, liveness_spec, bosy_file, spin_file, spin_file_temp)
    
    cond_print(VERBOSE_NONE, ">> Done! <<\n")


##################################################################################################
##################################################################################################
##################################################################################################

bdict = spot.make_bdd_dict()
bosy_input_prefix = "x_"
bosy_output_prefix = "y_"
    
#################################################
# inputs: safety spec, liveness spec, csp file, output file, verbosity
parser = argparse.ArgumentParser(description='Asynchronous Synthesis.')
parser.add_argument('-e', metavar='<file>', dest="env_file",
                    type=argparse.FileType('rt'), default='-', required=False, 
                    help="input csp file describing the environment process (default: sys.stdin)")
parser.add_argument('-s', metavar='<ltl>', dest="safety_spec",
                    action="store", default='G(false)', required=False,
                    help="safety specification (default: 'G(false)')")
parser.add_argument('-l', metavar='<ltl>', dest="liveness_spec",
                    action="store", required=True,
                    help="liveness specification")
parser.add_argument('-o', metavar='<file-prefix>', dest="base_file_path", 
                    # type=argparse.FileType('wt'),
                    action="store", required=True, 
                    help="file prefix (including path) to output .bosy file, and .spin file of the generated automata")
parser.add_argument("-v", metavar='<level>', dest="verbosity",
                    type=int, choices=range(0, 4), default=0, required=False,  
                    help="verbose level, ranges from 0 to 3 (default 0)")
parser.add_argument("-qbf", default=False, required=False, action="store_true", 
                    help="setting this forces implicit (QBF-based) solving")
parser.add_argument("-t", metavar='<timeout>', dest="timeout",
                    type=int, default=4000, required=False,  
                    help="specifies timeout (in seconds) for call to BoSy (default 100)")


if __name__ == '__main__':
    # read from prompt

    print(sys.argv)
    read_args = parser.parse_args(sys.argv[1:])

        
    
    main(read_args)

    #run_bosy('../examples/' + read_args.base_file_path + '.bosy', timeout=100)
    #print(read_args.base_file_path)
    run_bosy(read_args.base_file_path + '.bosy', read_args.qbf, read_args.timeout)
       

    print("DONE!!")
    










 
