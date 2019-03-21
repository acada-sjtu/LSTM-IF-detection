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

'''
# ---------- LSTM weights ----------
print file_weights.keys()
model_weights = file_weights['model_weights'] # dense_1, dropout_1, lstm_1
optimizer_weights = file_weights['optimizer_weights'] # Adam, training

# optimizer_weights
print optimizer_weights['training']['Adam']['Variable:0'] # (3, 32)

print optimizer_weights['training']['Adam']['Variable_1:0'] # (8, 32)
print optimizer_weights['training']['Adam']['Variable_2:0'] # (32,)
print optimizer_weights['training']['Adam']['Variable_3:0'] # (8, 1)
print optimizer_weights['training']['Adam']['Variable_4:0'] # (1,)
print optimizer_weights['training']['Adam']['Variable_5:0'] # (3, 32)
print optimizer_weights['training']['Adam']['Variable_6:0'] # (8, 32)
print optimizer_weights['training']['Adam']['Variable_7:0'] # (32,)
print optimizer_weights['training']['Adam']['Variable_8:0'] # (8, 1)
print optimizer_weights['training']['Adam']['Variable_9:0'] # (1,)

# model_weights
dense_1 = model_weights['dense_1']['dense_1'] # bias:0, kernel:0
lstm_1 = model_weights['lstm_1']['lstm_1'] # bias:0, kernel:0, recurrent_kernel:0
lstm_kernel = lstm_1['kernel:0']
lstm_recurrent_kernel = lstm_1['recurrent_kernel:0']
lstm_bias = lstm_1['bias:0']

lstm_kernel_array = lstm_kernel[()].T
lstm_recurrent_kernel_array = lstm_recurrent_kernel[()].T
lstm_bias_array = lstm_bias[()].T
print lstm_kernel
print lstm_recurrent_kernel
print lstm_bias

#f_out = h5py.File('states.hdf5','w')
#f_out.create_dataset('lstm_1_recurrent_kernel', data=grp1['lstm_1']['lstm_1']['recurrent_kernel'])
#f_out.create_dataset('lstm_1_kernel', data=grp1['lstm_1']['lstm_1']['kernel'])
#f_out.create_dataset('lstm_1_bias', data=grp1['lstm_1']['lstm_1']['bias'])
#f_out.close()
'''