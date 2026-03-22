`include "defs.v"

module top (
    input  clk,
    input  rst
);
    wire branch, mem_read, mem_to_reg, mem_write, alu_src, reg_write;
    wire [1:0] alu_src_b_sel;
    wire [`ALU_OP_WIDTH-1:0] alu_op;
    wire pc_src;
    wire [`WORD_WIDTH-1:0] pc_current, alu_result, mem_read_data;
    wire [`FUNCT3_WIDTH-1:0] funct3_out;

    datapath dp (.clk(clk), .rst(rst),
        .branch(branch), .mem_read(mem_read), .mem_to_reg(mem_to_reg),
        .alu_op(alu_op), .mem_write(mem_write), .alu_src(alu_src),
        .reg_write(reg_write), .alu_src_b_sel(alu_src_b_sel),
        .funct3_in(dp.instr[14:12]), .funct3_out(funct3_out),
        .opcode(dp.instr[6:0]), .pc_src(pc_src),
        .pc_current(pc_current), .alu_result(alu_result),
        .mem_read_data(mem_read_data));

    control ctrl (.opcode(dp.instr[6:0]), .funct3(dp.instr[14:12]),
        .funct7(dp.instr[31:25]), .branch(branch), .mem_read(mem_read),
        .mem_to_reg(mem_to_reg), .alu_op(alu_op),
        .mem_write(mem_write), .alu_src(alu_src),
        .reg_write(reg_write), .alu_src_b_sel(alu_src_b_sel));
endmodule
