module HB1xp67_ASAP7_75t_SL (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	endmodule

module FAx1_ASAP7_75t_SL (CON, SN, A, B, CI);
	output CON, SN;
	input A, B, CI;

	// Function
	wire A__bar, B__bar, CI__bar;
	wire int_fwire_0, int_fwire_1, int_fwire_2;
	wire int_fwire_3, int_fwire_4, int_fwire_5;
	wire int_fwire_6;

	not (CI__bar, CI);
	not (B__bar, B);
	and (int_fwire_0, B__bar, CI__bar);
	not (A__bar, A);
	and (int_fwire_1, A__bar, CI__bar);
	and (int_fwire_2, A__bar, B__bar);
	or (CON, int_fwire_2, int_fwire_1, int_fwire_0);
	and (int_fwire_3, A__bar, B__bar, CI__bar);
	and (int_fwire_4, A__bar, B, CI);
	and (int_fwire_5, A, B__bar, CI);
	and (int_fwire_6, A, B, CI__bar);
	or (SN, int_fwire_6, int_fwire_5, int_fwire_4, int_fwire_3);
	endmodule

module HAxp5_ASAP7_75t_SL (CON, SN, A, B);
	output CON, SN;
	input A, B;

	// Function
	wire A__bar, B__bar, int_fwire_0;
	wire int_fwire_1;

	not (B__bar, B);
	not (A__bar, A);
	or (CON, A__bar, B__bar);
	and (int_fwire_0, A__bar, B__bar);
	and (int_fwire_1, A, B);
	or (SN, int_fwire_1, int_fwire_0);
endmodule
