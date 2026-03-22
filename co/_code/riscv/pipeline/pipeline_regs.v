`ifndef PIPELINE_DEFS_V
`define PIPELINE_DEFS_V

`include "defs.v"

module if_id (
    input  clk, rst, flush, stall,
    input  [`WORD_WIDTH-1:0] pc_plus4_in,
    input  [`WORD_WIDTH-1:0] instr_in,
    output reg [`WORD_WIDTH-1:0] pc_plus4_out,
    output reg [`WORD_WIDTH-1:0] instr_out
);
    always @(posedge clk) begin
        if (rst || flush) begin
            pc_plus4_out <= 32'd0;
            instr_out    <= 32'h00000013;
        end else if (!stall) begin
            pc_plus4_out <= pc_plus4_in;
            instr_out    <= instr_in;
        end
    end
endmodule

module id_ex (
    input  clk, rst, flush,
    input  [`WORD_WIDTH-1:0] pc_plus4_in,
    input  [`WORD_WIDTH-1:0] rs1_data_in, rs2_data_in,
    input  [`WORD_WIDTH-1:0] imm_in,
    input  [`REG_ADDR_WIDTH-1:0] rd_in,
    input  branch_in, mem_read_in, mem_to_reg_in,
    input  [`ALU_OP_WIDTH-1:0] alu_op_in,
    input  mem_write_in, alu_src_in, reg_write_in,
    input  [`FUNCT3_WIDTH-1:0] funct3_in,
    output reg [`WORD_WIDTH-1:0] pc_plus4_out,
    output reg [`WORD_WIDTH-1:0] rs1_data_out, rs2_data_out,
    output reg [`WORD_WIDTH-1:0] imm_out,
    output reg [`REG_ADDR_WIDTH-1:0] rd_out,
    output reg branch_out, mem_read_out, mem_to_reg_out,
    output reg [`ALU_OP_WIDTH-1:0] alu_op_out,
    output reg mem_write_out, alu_src_out, reg_write_out,
    output reg [`FUNCT3_WIDTH-1:0] funct3_out
);
    always @(posedge clk) begin
        if (rst || flush) begin
            pc_plus4_out  <= 32'd0;
            rs1_data_out  <= 32'd0;
            rs2_data_out  <= 32'd0;
            imm_out       <= 32'd0;
            rd_out        <= 5'd0;
            branch_out    <= 0;
            mem_read_out  <= 0;
            mem_to_reg_out<= 0;
            alu_op_out    <= 4'd0;
            mem_write_out <= 0;
            alu_src_out   <= 0;
            reg_write_out <= 0;
            funct3_out    <= 3'd0;
        end else begin
            pc_plus4_out  <= pc_plus4_in;
            rs1_data_out  <= rs1_data_in;
            rs2_data_out  <= rs2_data_in;
            imm_out       <= imm_in;
            rd_out        <= rd_in;
            branch_out    <= branch_in;
            mem_read_out  <= mem_read_in;
            mem_to_reg_out<= mem_to_reg_in;
            alu_op_out    <= alu_op_in;
            mem_write_out <= mem_write_in;
            alu_src_out   <= alu_src_in;
            reg_write_out <= reg_write_in;
            funct3_out    <= funct3_in;
        end
    end
endmodule

module ex_mem (
    input  clk, rst,
    input  [`WORD_WIDTH-1:0] alu_result_in,
    input  [`WORD_WIDTH-1:0] write_data_in,
    input  [`REG_ADDR_WIDTH-1:0] rd_in,
    input  branch_in, mem_read_in, mem_to_reg_in,
    input  mem_write_in, reg_write_in,
    output reg [`WORD_WIDTH-1:0] alu_result_out,
    output reg [`WORD_WIDTH-1:0] write_data_out,
    output reg [`REG_ADDR_WIDTH-1:0] rd_out,
    output reg branch_out, mem_read_out, mem_to_reg_out,
    output reg mem_write_out, reg_write_out
);
    always @(posedge clk) begin
        if (rst) begin
            alu_result_out  <= 32'd0;
            write_data_out  <= 32'd0;
            rd_out          <= 5'd0;
            branch_out      <= 0;
            mem_read_out    <= 0;
            mem_to_reg_out  <= 0;
            mem_write_out   <= 0;
            reg_write_out   <= 0;
        end else begin
            alu_result_out  <= alu_result_in;
            write_data_out  <= write_data_in;
            rd_out          <= rd_in;
            branch_out      <= branch_in;
            mem_read_out    <= mem_read_in;
            mem_to_reg_out  <= mem_to_reg_in;
            mem_write_out   <= mem_write_in;
            reg_write_out   <= reg_write_in;
        end
    end
endmodule

module mem_wb (
    input  clk, rst,
    input  [`WORD_WIDTH-1:0] alu_result_in,
    input  [`WORD_WIDTH-1:0] mem_data_in,
    input  [`REG_ADDR_WIDTH-1:0] rd_in,
    input  mem_to_reg_in, reg_write_in,
    output reg [`WORD_WIDTH-1:0] alu_result_out,
    output reg [`WORD_WIDTH-1:0] mem_data_out,
    output reg [`REG_ADDR_WIDTH-1:0] rd_out,
    output reg mem_to_reg_out, reg_write_out
);
    always @(posedge clk) begin
        if (rst) begin
            alu_result_out  <= 32'd0;
            mem_data_out    <= 32'd0;
            rd_out          <= 5'd0;
            mem_to_reg_out  <= 0;
            reg_write_out   <= 0;
        end else begin
            alu_result_out  <= alu_result_in;
            mem_data_out    <= mem_data_in;
            rd_out          <= rd_in;
            mem_to_reg_out  <= mem_to_reg_in;
            reg_write_out   <= reg_write_in;
        end
    end
endmodule

`endif
