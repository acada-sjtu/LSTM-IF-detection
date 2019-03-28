module t1 (N1,N2,N3,N19);

input N1,N2,N3;

output N19;

N16 = NAND(N1, N2)
N19 = NOR(N16, N3)

endmodule