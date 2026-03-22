`include "defs.v"

module datapath (
    input  clk,
    input  rst,
    input  branch,
    input  mem_read,
    input  mem_to_reg,
    input  [`ALU_OP_WIDTH-1:0] alu_op,
    input  mem_write,
    input  alu_src,
    input  reg_write,
    input  [1:0] alu_src_b_sel,
    input  [`FUNCT3_WIDTH-1:0] funct3_in,
    input  [`OPCODE_WIDTH-1:0] opcode,
    output [`FUNCT3_WIDTH-1:0] funct3_out,
    output pc_src,
    output reg [`WORD_WIDTH-1:0] pc_current,
    output [`WORD_WIDTH-1:0] alu_result,
    output [`WORD_WIDTH-1:0] mem_read_data
);
    wire [`WORD_WIDTH-1:0] pc_next, pc_plus4, pc_target;
    wire [`WORD_WIDTH-1:0] instr, rs1_data, rs2_data;
    wire [`WORD_WIDTH-1:0] imm;
    wire [`WORD_WIDTH-1:0] alu_b;
    wire alu_zero;
    wire [`WORD_WIDTH-1:0] write_back_data;
    wire [`WORD_WIDTH-1:0] mem_read_data_w;
    wire [`REG_ADDR_WIDTH-1:0] rs1_addr, rs2_addr, rd_addr;

    assign funct3_out = funct3_in;
    assign rs1_addr = instr[19:15];
    assign rs2_addr = instr[24:20];
    assign rd_addr  = instr[11:7];

    always @(posedge clk) begin
        if (rst)
            pc_current <= 32'd0;
        else
            pc_current <= pc_next;
    end

    assign pc_plus4  = pc_current + 32'd4;
    assign pc_target = pc_current + imm;

    assign pc_src = branch && (
        (funct3_in == 3'b000 && alu_zero) ||
        (funct3_in == 3'b001 && !alu_zero) ||
        (funct3_in == 3'b100 && !alu_zero) ||
        (funct3_in == 3'b101 && alu_zero) ||
        (funct3_in == 3'b110 && !alu_zero) ||
        (funct3_in == 3'b111 && alu_zero)
    );

    assign pc_next = pc_src ? pc_target : pc_plus4;

    imem imem_inst (.addr(pc_current[`MEM_ADDR_WIDTH+1:2]), .instr(instr));

    regfile rf (.clk(clk), .rst(rst),
        .rs1_addr(rs1_addr), .rs2_addr(rs2_addr),
        .rd_addr(rd_addr), .rd_data(write_back_data),
        .rd_write_en(reg_write),
        .rs1_data(rs1_data), .rs2_data(rs2_data));

    imm_gen ig (.instr(instr), .imm(imm));

    assign alu_b = (alu_src_b_sel == 2'd0) ? rs2_data :
                    (alu_src_b_sel == 2'd1) ? imm :
                    {instr[31:12], 12'b0};

    alu alu_inst (.a(rs1_data), .b(alu_b), .alu_op(alu_op),
                  .result(alu_result));
    assign alu_zero = (alu_result == 32'd0);

    dmem dmem_inst (.clk(clk), .addr(alu_result[`MEM_ADDR_WIDTH+1:2]),
        .write_data(rs2_data), .mem_read(mem_read),
        .mem_write(mem_write), .read_data(mem_read_data_w));

    assign mem_read_data = mem_read_data_w;

    assign write_back_data =
        (mem_to_reg == 2'd0) ? alu_result :
        (mem_to_reg == 2'd1) ? mem_read_data_w :
        pc_plus4;
endmodule
