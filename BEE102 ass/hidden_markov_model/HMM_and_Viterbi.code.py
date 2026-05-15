import sys
import os
import math
import numpy as np

states = {"s": 0, "E": 1, "5": 2, "I" : 3, "e": 4}
id2state = {0: "s", 1: "E", 2: "5", 3: "I", 4: "e"}

state_transition_prob = np.array([
    [0.0, 1.0, 0.0, 0.0, 0.0], 
    [0.0, 0.9, 0.1, 0.0, 0.0], 
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.9, 0.1],
    [0.0, 0.0, 0.0, 0.0, 0.0]
])

emission_nuc_codes = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
emission_probs = np.array([
    [0.00, 0.00, 0.00, 0.00], 
    [0.25, 0.25, 0.25, 0.25],
    [0.05, 0.00, 0.95, 0.00],
    [0.40, 0.10, 0.10, 0.40],
    [0.00, 0.00, 0.00, 0.00]
])

query_sequence = "CTTCATGTGAAAGCAGACGTAAGTCA"
n_states = len(states)
T = len(query_sequence)

viterbi_value_matrix = np.full((n_states, T), -np.inf)
viterbi_trace_matrix = np.zeros((n_states, T), dtype=int)



def calculate_prob_for_a_node(prev_col_probs, curr_state_idx, obs_idx):
    """
    Calculates the max log-probability for a state at time t based on column t-1.
    """
    max_val = -np.inf
    best_prev_state = 0
    
    
    emis_p = emission_probs[curr_state_idx][obs_idx]
    if emis_p == 0:
        return -np.inf, 0
    
    log_emis = math.log(emis_p)

    for prev_state_idx in range(n_states):
        trans_p = state_transition_prob[prev_state_idx][curr_state_idx]
        
        if trans_p > 0 and prev_col_probs[prev_state_idx] != -np.inf:
           
            current_prob = prev_col_probs[prev_state_idx] + math.log(trans_p) + log_emis
            
            if current_prob > max_val:
                max_val = current_prob
                best_prev_state = prev_state_idx
                
    return max_val, best_prev_state


first_obs = emission_nuc_codes[query_sequence[0]]

for s in range(n_states):
    t_start = state_transition_prob[states["s"]][s]
    e_start = emission_probs[s][first_obs]
    
    if t_start > 0 and e_start > 0:
        viterbi_value_matrix[s][0] = math.log(0.25) + math.log(t_start) + math.log(e_start)
    viterbi_trace_matrix[s][0] = 0


for t in range(1, T):
    obs_idx = emission_nuc_codes[query_sequence[t]]
    for s_curr in range(n_states):
        val, prev_idx = calculate_prob_for_a_node(viterbi_value_matrix[:, t-1], s_curr, obs_idx)
        viterbi_value_matrix[s_curr][t] = val
        viterbi_trace_matrix[s_curr][t] = prev_idx


final_probs = []
for s_idx in range(n_states):
    trans_end = state_transition_prob[s_idx][states["e"]]
    if trans_end > 0:
        final_probs.append(viterbi_value_matrix[s_idx][T-1] + math.log(trans_end))
    else:
        final_probs.append(-np.inf)

best_last_state = np.argmax(final_probs)


path_indices = [best_last_state]
for t in range(T - 1, 0, -1):
    best_last_state = viterbi_trace_matrix[best_last_state][t]
    path_indices.append(best_last_state)

path_indices.reverse()
state_path = "".join([id2state[i] for i in path_indices])


print(f"Query Sequence: {query_sequence}")
print(f"Most Probable Path: {state_path}")
print(f"Log Probability: {np.max(final_probs)}")