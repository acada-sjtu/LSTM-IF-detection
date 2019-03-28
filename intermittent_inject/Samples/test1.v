// Verilog
// t1
// Ninputs 11
// Noutputs 4
// NtotalGates 10
// NAND2 6

module t1 (N1,N2,N3,N4,N5,N6,N7, N8, N9, N10, N11, N12, N13, N14, N15);

input N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11;

output N12,N13,N14,N15;

wire N16,N17,N18,N19,N20,N21;

nand NAND2_1 (N16, N1, N2);
nor NOR2_2 (N17, N3, N16);
nand NAND2_3 (N19, N6, N7);
nor NOR2_4 (N20, N8, N9);
nand NAND2_5 (N14, N10, N19);
nor NOR2_6 (N18, N17, N19);
nand NAND2_7 (N12, N16, N18);
nor NOR2_8 (N13, N18, N20);
nand NAND2_10 (N21, N4, N5);
nand NAND2_9 (N15, N21, N11);

endmodule