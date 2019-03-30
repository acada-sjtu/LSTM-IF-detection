import sys
import h5py
import numpy as np
from draw_fig import draw_binary
from draw_fig import draw_hidden_states
from draw_fig import draw_bi_hidden_states

CYCLE = 50

file_path = sys.argv[1]
if file_path.split('/')[1].split('_')[0]=='bi':
	bi_h_states_flag = 1
else:
	bi_h_states_flag = 0

file_h_states_J = h5py.File(file_path, 'r')


# # ---------- flipped for inputerror ----------
# print('processing flipped...')
# flipped_raw = np.loadtxt('flipped_b10_e', dtype='int64')
# # permanent fault
# flipped = flipped_raw.copy()
# # intermittent fault
# flipped_raw = flipped_raw.reshape((-1, CYCLE, flipped_raw.shape[1]))
# print(flipped_raw.shape)
# flipped = np.zeros((flipped_raw.shape[0], flipped_raw.shape[1]-1, flipped_raw.shape[2]), dtype='int64')
# for i in range(flipped.shape[0]):
#     flipped[i] = np.delete(flipped_raw[i], 0, axis=0)


# hidden states J
print(file_h_states_J.keys())  # input, affected, hidden_states
input_array = file_h_states_J['input']
affected_array = file_h_states_J['affected']
if bi_h_states_flag==1:
	hidden_states_array = file_h_states_J['bi_hidden_states']
else:
	hidden_states_array = file_h_states_J['hidden_states']

rightORwrong_array = file_h_states_J['rightORwrong']

# # hidden states J free
# print(file_h_states_J.keys())  # input, hidden_states
# input_array = file_h_states_J_free['input']
# hidden_states_array = file_h_states_J_free['hidden_states']
# rightORwrong_array = file_h_states_J['rightORwrong']


start_i = 0
i = 0
for (i_key, a_key, h_key, rw_key) in \
        zip(input_array.keys(), affected_array.keys(), hidden_states_array.keys(), rightORwrong_array.keys()):
    if i < start_i:
        i += 1
        continue
    print('Sample: ', i)
    # Input
    # print(input_array[i_key].name)
    # print(input_array[i_key][()])
    draw_binary('input_%d' % i, input_array[i_key][()].T, save=1)
    # Flipped
    # Affected
    # print(affected_array[a_key].name)
    # print(affected_array[a_key][()])
    draw_binary('affected_%d' % i, affected_array[a_key][()].T, save=1)
    # Hidden states
    # print(hidden_states_array[h_key].name)
    # print(hidden_states_array[h_key][()])
    if bi_h_states_flag==1:
    	draw_bi_hidden_states('bi_hidden_states_%d' % i, hidden_states_array[h_key][()].T, save=1)
    else:
    	draw_hidden_states('hidden_states_%d' % i, hidden_states_array[h_key][()].T, save=1)
    # Right or Wrong
    # print(rightORwrong_array[rw_key].name)
    print(rightORwrong_array[rw_key][()])
    if rightORwrong_array[rw_key][()] == 1:
        print('right')
    else:
        print('wrong')
    # draw_pixel()
    i += 1
    input()
