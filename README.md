# LSTM-RNN-Checker

This repo is the source code for the VTS'21 paper "LSTM-based Analysis of Temporally- and Spatially-Correlated Signatures for Intermittent Fault Detection".

Link: http://ieeexplore.ieee.org/document/9107600/references

## intermittent_inject

This is the intermittent fault injection toolkit. It supports ITC'99 circuit benchmark, OR1200 processor, and Leon3 processor.

## parser

This is the parser for OR1200 and Leon3 processor, which can parse VERILOG code to BENCH code.

## standard

This is the standard detection model set, which includes SVM, RNN, (1/2-layer) LSTM, BiLSTM.

## visualization

This is the visualization tool for LSTM model. However, it depends on some modifications in Keras library, which are not included in this repo.
