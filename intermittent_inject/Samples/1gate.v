module t1 (N1,N2,N3,N4,N5,N6,N7,N19,N21,N23);

input N1,N2,N3,N4,N5,N6,N7;

output N19,N21,N23;

N16 = NAND(N1, N2)
N19 = NOR(N16, N3)
N21 = NAND(N4, N5)
N23 = NOR(N6, N7)

endmodule