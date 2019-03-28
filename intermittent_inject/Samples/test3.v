// Verilog
// t3
// Ninputs 11
// Noutputs 2
// NtotalGates 18
// NAND2 5

module t1 (N1,N2,N3,N4,N5,N6,N7, N8, N9, N10, N11, N13, N14);

input N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11;

output N13,N14;

wire N12,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29;

nand NAND2_1 (N16, N1, N2);
nor NOR2_2 (N19, N3, N16);
nand NAND2_13 (N21, N4, N5);
nor NOR2_16 (N23, N6, N7);
nand NAND2_18 (N26, N7, N9);
nor NOR2_19 (N25, N3, N8);
nand NAND2_3 (N18, N19, N17);
nor NOR2_10 (N17, N16, N21);
nor NOR2_14 (N22, N21, N25);
nand NAND2_12 (N20, N19, N22);
nor NOR2_11 (N12, N18, N20);
nor NOR2_24 (N27, N10, N11);
nand NAND2_17 (N24, N23, N27);
nor NOR2_15 (N13, N12, N24);
nand NAND2_20 (N28, N25, N26);
nand NAND2_21 (N29, N22, N28);
nand NAND2_23 (N15, N26, N27);
nand NAND2_22 (N14, N29, N15);



endmodule