`include "defs.v"

module tb_top;
    reg clk, rst;

    top uut (.clk(clk), .rst(rst));

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
            $display("cycle=%d PC=%h instr=%h reg_write=%b alu_op=%d",
                     cycle, uut.dp.pc_current, uut.dp.instr, uut.reg_write, uut.alu_op);
            if (cycle >= 100) begin
                $display("=== Final Register State ===");
                $display("x1  = %d (%h)", uut.dp.rf.regs[1],  uut.dp.rf.regs[1]);
                $display("x2  = %d (%h)", uut.dp.rf.regs[2],  uut.dp.rf.regs[2]);
                $display("x3  = %d (%h)", uut.dp.rf.regs[3],  uut.dp.rf.regs[3]);
                $display("x4  = %d (%h)", uut.dp.rf.regs[4],  uut.dp.rf.regs[4]);
                $display("x5  = %d (%h)", uut.dp.rf.regs[5],  uut.dp.rf.regs[5]);
                $display("x6  = %d (%h)", uut.dp.rf.regs[6],  uut.dp.rf.regs[6]);
                $display("x7  = %d (%h)", uut.dp.rf.regs[7],  uut.dp.rf.regs[7]);
                $display("x8  = %d (%h)", uut.dp.rf.regs[8],  uut.dp.rf.regs[8]);
                $display("x9  = %d (%h)", uut.dp.rf.regs[9],  uut.dp.rf.regs[9]);
                $display("x10 = %d (%h)", uut.dp.rf.regs[10], uut.dp.rf.regs[10]);
                $display("x11 = %d (%h)", uut.dp.rf.regs[11], uut.dp.rf.regs[11]);
                $display("x12 = %d (%h)", uut.dp.rf.regs[12], uut.dp.rf.regs[12]);
                $display("x13 = %d (%h)", uut.dp.rf.regs[13], uut.dp.rf.regs[13]);
                $display("x14 = %d (%h)", uut.dp.rf.regs[14], uut.dp.rf.regs[14]);
                $display("x15 = %d (%h)", uut.dp.rf.regs[15], uut.dp.rf.regs[15]);
                $display("x16 = %d (%h)", uut.dp.rf.regs[16], uut.dp.rf.regs[16]);
                $display("x17 = %d (%h)", uut.dp.rf.regs[17], uut.dp.rf.regs[17]);
                $display("x18 = %d (%h)", uut.dp.rf.regs[18], uut.dp.rf.regs[18]);
                $display("x19 = %d (%h)", uut.dp.rf.regs[19], uut.dp.rf.regs[19]);
                $display("x20 = %d (%h)", uut.dp.rf.regs[20], uut.dp.rf.regs[20]);
                $display("x21 = %d (%h)", uut.dp.rf.regs[21], uut.dp.rf.regs[21]);
                $display("x22 = %d (%h)", uut.dp.rf.regs[22], uut.dp.rf.regs[22]);
                $display("x23 = %d (%h)", uut.dp.rf.regs[23], uut.dp.rf.regs[23]);
                $display("x24 = %d (%h)", uut.dp.rf.regs[24], uut.dp.rf.regs[24]);
                $display("x25 = %d (%h)", uut.dp.rf.regs[25], uut.dp.rf.regs[25]);
                $display("x26 = %d (%h)", uut.dp.rf.regs[26], uut.dp.rf.regs[26]);
                $display("x27 = %d (%h)", uut.dp.rf.regs[27], uut.dp.rf.regs[27]);
                $display("x28 = %d (%h)", uut.dp.rf.regs[28], uut.dp.rf.regs[28]);
                $display("x29 = %d (%h)", uut.dp.rf.regs[29], uut.dp.rf.regs[29]);
                $display("x30 = %d (%h)", uut.dp.rf.regs[30], uut.dp.rf.regs[30]);
                $display("x31 = %d (%h)", uut.dp.rf.regs[31], uut.dp.rf.regs[31]);
                $finish;
            end
        end
    end
endmodule
