`include "defs.v"

module tb_pipeline;
    reg clk, rst;

    wire [`WORD_WIDTH-1:0] debug_pc;
    wire [31:0] debug_reg0, debug_reg1, debug_reg2, debug_reg3;
    wire [31:0] debug_reg4, debug_reg5, debug_reg6, debug_reg7;
    wire [31:0] debug_reg8, debug_reg9, debug_reg10, debug_reg11;
    wire [31:0] debug_reg12, debug_reg13, debug_reg14, debug_reg15;
    wire [31:0] debug_reg28, debug_reg29, debug_reg30, debug_reg31;

    pipeline_top uut (.clk(clk), .rst(rst),
        .debug_pc(debug_pc),
        .debug_reg0(debug_reg0), .debug_reg1(debug_reg1),
        .debug_reg2(debug_reg2), .debug_reg3(debug_reg3),
        .debug_reg4(debug_reg4), .debug_reg5(debug_reg5),
        .debug_reg6(debug_reg6), .debug_reg7(debug_reg7),
        .debug_reg8(debug_reg8), .debug_reg9(debug_reg9),
        .debug_reg10(debug_reg10), .debug_reg11(debug_reg11),
        .debug_reg12(debug_reg12), .debug_reg13(debug_reg13),
        .debug_reg14(debug_reg14), .debug_reg15(debug_reg15),
        .debug_reg28(debug_reg28), .debug_reg29(debug_reg29),
        .debug_reg30(debug_reg30), .debug_reg31(debug_reg31));

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    integer cycle;
    initial begin
        rst = 1;
        #15;
        rst = 0;
        cycle = 0;
        #10;
        forever begin
            @(posedge clk);
            #1;
            cycle = cycle + 1;
            $display("cycle=%d PC=%h stall=%b if_flush=%b branch_taken=%b",
                     cycle, uut.pc_current, uut.stall, uut.if_flush, uut.branch_taken);
            if (cycle >= 100) begin
                $display("=== Pipeline Final Register State ===");
                $display("x0  = %d (%h)", uut.debug_reg0,  uut.debug_reg0);
                $display("x1  = %d (%h)", uut.debug_reg1,  uut.debug_reg1);
                $display("x2  = %d (%h)", uut.debug_reg2,  uut.debug_reg2);
                $display("x3  = %d (%h)", uut.debug_reg3,  uut.debug_reg3);
                $display("x4  = %d (%h)", uut.debug_reg4,  uut.debug_reg4);
                $display("x5  = %d (%h)", uut.debug_reg5,  uut.debug_reg5);
                $display("x6  = %d (%h)", uut.debug_reg6,  uut.debug_reg6);
                $display("x7  = %d (%h)", uut.debug_reg7,  uut.debug_reg7);
                $display("x8  = %d (%h)", uut.debug_reg8,  uut.debug_reg8);
                $display("x9  = %d (%h)", uut.debug_reg9,  uut.debug_reg9);
                $display("x10 = %d (%h)", uut.debug_reg10, uut.debug_reg10);
                $display("x11 = %d (%h)", uut.debug_reg11, uut.debug_reg11);
                $display("x12 = %d (%h)", uut.debug_reg12, uut.debug_reg12);
                $display("x13 = %d (%h)", uut.debug_reg13, uut.debug_reg13);
                $display("x14 = %d (%h)", uut.debug_reg14, uut.debug_reg14);
                $display("x15 = %d (%h)", uut.debug_reg15, uut.debug_reg15);
                $display("x28 = %d (%h)", uut.debug_reg28, uut.debug_reg28);
                $display("x29 = %d (%h)", uut.debug_reg29, uut.debug_reg29);
                $display("x30 = %d (%h)", uut.debug_reg30, uut.debug_reg30);
                $display("x31 = %d (%h)", uut.debug_reg31, uut.debug_reg31);
                $finish;
            end
        end
    end
endmodule
