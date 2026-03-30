`include "defs.v"

module pipeline_datapath (
    input  clk, rst
);
    wire [`WORD_WIDTH-1:0] pc_current, pc_plus4, pc_next;
    wire [`WORD_WIDTH-1:0] instr_if;

    wire [`WORD_WIDTH-1:0] pc_plus4_id, instr_id;
    wire [`REG_ADDR_WIDTH-1:0] rs1_id, rs2_id, rd_id;
    wire [`WORD_WIDTH-1:0] rs1_data_id, rs2_data_id;
    wire [`WORD_WIDTH-1:0] imm_id;

    wire [`WORD_WIDTH-1:0] pc_plus4_ex, rs1_data_ex, rs2_data_ex, imm_ex;
    wire [`REG_ADDR_WIDTH-1:0] rd_ex;
    wire branch_ex, mem_read_ex, mem_to_reg_ex;
    wire [`ALU_OP_WIDTH-1:0] alu_op_ex;
    wire mem_write_ex, alu_src_ex, reg_write_ex;
    wire [`FUNCT3_WIDTH-1:0] funct3_ex;

    wire [`WORD_WIDTH-1:0] pc_plus4_mem, alu_result_ex;
    wire [`WORD_WIDTH-1:0] write_data_ex;
    wire [`REG_ADDR_WIDTH-1:0] rd_mem;
    wire branch_mem, mem_read_mem, mem_to_reg_mem;
    wire mem_write_mem, reg_write_mem;

    wire [`WORD_WIDTH-1:0] alu_result_mem, mem_data_mem;
    wire [`REG_ADDR_WIDTH-1:0] rd_wb;
    wire mem_to_reg_wb, reg_write_wb;

    wire [`WORD_WIDTH-1:0] write_back_data;

    wire stall, if_flush, id_flush, ex_flush;
    wire [1:0] forward_a_sel, forward_b_sel;
    wire [`WORD_WIDTH-1:0] rs1_data_id_f, rs2_data_id_f;

    wire branch_taken;
    wire [`WORD_WIDTH-1:0] alu_result_ex_d, write_data_ex_d;

    wire [`WORD_WIDTH-1:0] alu_a, alu_b;

    assign rs1_id = instr_id[19:15];
    assign rs2_id = instr_id[24:20];
    assign rd_id  = instr_id[11:7];

    always @(posedge clk) begin
        if (rst) pc_current <= 32'd0;
        else     pc_current <= pc_next;
    end

    assign pc_plus4     = pc_current + 32'd4;
    assign instr_if     = imem_if.mem[pc_current[`MEM_ADDR_WIDTH+1:2]];

    hazard_detection hf (
        .rs1_id(rs1_id), .rs2_id(rs2_id),
        .rd_ex(rd_ex), .mem_read_ex(mem_read_ex),
        .rd_mem(rd_mem), .reg_write_mem(reg_write_mem),
        .rd_wb(rd_wb), .reg_write_wb(reg_write_wb),
        .stall(stall), .forward_a(), .forward_b(),
        .forward_a_sel(forward_a_sel), .forward_b_sel(forward_b_sel)
    );

    assign if_flush  = branch_taken || stall;
    assign id_flush  = stall;
    assign ex_flush  = 0;

    assign pc_next   = branch_taken ? (pc_plus4_ex + imm_ex) : pc_plus4;

    assign rs1_data_id_f = (forward_a_sel == 2'd1) ? alu_result_ex :
                           (forward_a_sel == 2'd2) ? alu_result_mem :
                           (forward_a_sel == 2'd3) ? write_back_data : rs1_data_id;
    assign rs2_data_id_f = (forward_b_sel == 2'd1) ? alu_result_ex :
                           (forward_b_sel == 2'd2) ? alu_result_mem :
                           (forward_b_sel == 2'd3) ? write_back_data : rs2_data_id;

    branch_taken_gen btg (
        .branch(branch_ex), .funct3(funct3_ex),
        .rs1_data(rs1_data_ex), .rs2_data(rs2_data_ex),
        .taken(branch_taken)
    );

    assign alu_a = rs1_data_ex;
    assign alu_b = (alu_src_ex) ? imm_ex : write_data_ex;

    if_id  if_id_reg (.clk(clk), .rst(rst),
        .flush(if_flush), .stall(stall),
        .pc_plus4_in(pc_plus4), .instr_in(instr_if),
        .pc_plus4_out(pc_plus4_id), .instr_out(instr_id));

    id_ex  id_ex_reg (.clk(clk), .rst(rst), .flush(ex_flush),
        .pc_plus4_in(pc_plus4_id), .rs1_data_in(rs1_data_id_f),
        .rs2_data_in(rs2_data_id_f), .imm_in(imm_id),
        .rd_in(rd_id), .branch_in(branch), .mem_read_in(mem_read),
        .mem_to_reg_in(mem_to_reg), .alu_op_in(alu_op),
        .mem_write_in(mem_write), .alu_src_in(alu_src),
        .reg_write_in(reg_write), .funct3_in(instr_id[14:12]),
        .pc_plus4_out(pc_plus4_ex), .rs1_data_out(rs1_data_ex),
        .rs2_data_out(rs2_data_ex), .imm_out(imm_ex), .rd_out(rd_ex),
        .branch_out(branch_ex), .mem_read_out(mem_read_ex),
        .mem_to_reg_out(mem_to_reg_ex), .alu_op_out(alu_op_ex),
        .mem_write_out(mem_write_ex), .alu_src_out(alu_src_ex),
        .reg_write_out(reg_write_ex), .funct3_out(funct3_out));

    ex_mem ex_mem_reg (.clk(clk), .rst(rst),
        .alu_result_in(alu_result_ex), .write_data_in(write_data_ex),
        .rd_in(rd_ex), .branch_in(branch_ex),
        .mem_read_in(mem_read_ex), .mem_to_reg_in(mem_to_reg_ex),
        .mem_write_in(mem_write_ex), .reg_write_in(reg_write_ex),
        .alu_result_out(alu_result_mem), .write_data_out(write_data_mem),
        .rd_out(rd_mem), .branch_out(branch_mem),
        .mem_read_out(mem_read_mem), .mem_to_reg_out(mem_to_reg_mem),
        .mem_write_out(mem_write_mem), .reg_write_out(reg_write_mem));

    mem_wb  mem_wb_reg (.clk(clk), .rst(rst),
        .alu_result_in(alu_result_mem), .mem_data_in(mem_data_mem),
        .rd_in(rd_mem), .mem_to_reg_in(mem_to_reg_mem),
        .reg_write_in(reg_write_mem),
        .alu_result_out(alu_result_wb), .mem_data_out(mem_data_wb),
        .rd_out(rd_wb), .mem_to_reg_out(mem_to_reg_wb),
        .reg_write_out(reg_write_wb));

    assign write_back_data = mem_to_reg_wb ? mem_data_wb : alu_result_wb;

    regfile rf (.clk(clk), .rst(rst),
        .rs1_addr(rs1_id), .rs2_addr(rs2_id),
        .rd_addr(rd_wb), .rd_data(write_back_data),
        .rd_write_en(reg_write_wb),
        .rs1_data(rs1_data_id), .rs2_data(rs2_data_id));

    pipeline_control ctrl (.instr(instr_id),
        .stall(stall), .branch(branch), .mem_read(mem_read),
        .mem_to_reg(mem_to_reg), .alu_op(alu_op),
        .mem_write(mem_write), .alu_src(alu_src),
        .reg_write(reg_write), .alu_src_b_sel(alu_src_b_sel));

    imm_gen ig (.instr(instr_id), .imm(imm_id));

    alu alu_ex (.a(alu_a), .b(alu_b), .alu_op(alu_op_ex),
                .result(alu_result_ex));

    dmem dm (.clk(clk), .addr(alu_result_mem[`MEM_ADDR_WIDTH+1:2]),
        .write_data(write_data_mem), .mem_read(mem_read_mem),
        .mem_write(mem_write_mem), .read_data(mem_data_mem));

endmodule

module branch_taken_gen (
    input  branch,
    input  [`FUNCT3_WIDTH-1:0] funct3,
    input  [`WORD_WIDTH-1:0] rs1_data, rs2_data,
    output reg taken
);
    wire zero = (rs1_data == rs2_data);
    always @(*) begin
        if (!branch) taken = 0;
        else begin
            case (funct3)
                3'b000: taken = zero;
                3'b001: taken = !zero;
                3'b100: taken = ($signed(rs1_data) < $signed(rs2_data));
                3'b101: taken = ($signed(rs1_data) >= $signed(rs2_data));
                3'b110: taken = (rs1_data < rs2_data);
                3'b111: taken = (rs1_data >= rs2_data);
                default: taken = 0;
            endcase
        end
    end
endmodule
