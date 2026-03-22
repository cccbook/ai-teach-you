`include "defs.v"

module pipeline_top (
    input  clk,
    input  rst,
    output [`WORD_WIDTH-1:0] debug_pc,
    output [31:0] debug_reg0, debug_reg1, debug_reg2, debug_reg3,
    output [31:0] debug_reg4, debug_reg5, debug_reg6, debug_reg7,
    output [31:0] debug_reg8, debug_reg9, debug_reg10, debug_reg11,
    output [31:0] debug_reg12, debug_reg13, debug_reg14, debug_reg15,
    output [31:0] debug_reg28, debug_reg29, debug_reg30, debug_reg31
);

    wire stall, if_flush, id_flush;
    wire [1:0] forward_a_sel, forward_b_sel;

    reg  [`WORD_WIDTH-1:0] pc_current;
    wire [`WORD_WIDTH-1:0] pc_plus4_if, pc_next, pc_target;

    wire [`WORD_WIDTH-1:0] instr_if;

    wire [`WORD_WIDTH-1:0] pc_plus4_id, instr_id;
    wire [`REG_ADDR_WIDTH-1:0] rs1_addr_id, rs2_addr_id, rd_id;
    wire [`WORD_WIDTH-1:0] rs1_data_id, rs2_data_id;
    wire [`WORD_WIDTH-1:0] imm_id;
    wire branch_id, mem_read_id, mem_to_reg_id;
    wire [`ALU_OP_WIDTH-1:0] alu_op_id;
    wire mem_write_id, alu_src_id, reg_write_id;
    wire [`FUNCT3_WIDTH-1:0] funct3_id;

    wire [`WORD_WIDTH-1:0] pc_plus4_ex, rs1_data_ex, rs2_data_ex, imm_ex;
    wire [`REG_ADDR_WIDTH-1:0] rd_ex;
    wire branch_ex, mem_read_ex, mem_to_reg_ex;
    wire [`ALU_OP_WIDTH-1:0] alu_op_ex;
    wire mem_write_ex, alu_src_ex, reg_write_ex;
    wire [`FUNCT3_WIDTH-1:0] funct3_ex;

    wire [`WORD_WIDTH-1:0] alu_a, alu_b, alu_result_ex;

    wire [`WORD_WIDTH-1:0] alu_result_mem, write_data_mem;
    wire [`REG_ADDR_WIDTH-1:0] rd_mem;
    wire mem_read_mem, mem_to_reg_mem, mem_write_mem, reg_write_mem;
    wire [`WORD_WIDTH-1:0] mem_data_mem;

    wire [`WORD_WIDTH-1:0] alu_result_wb, mem_data_wb;
    wire [`REG_ADDR_WIDTH-1:0] rd_wb;
    wire mem_to_reg_wb, reg_write_wb;
    wire [`WORD_WIDTH-1:0] write_back_data;

    wire [`WORD_WIDTH-1:0] rs1_data_ex_f, rs2_data_ex_f;
    wire branch_taken;
    wire pc_src;

    assign debug_pc = pc_current;
    assign debug_reg0  = rf.regs[0];
    assign debug_reg1  = rf.regs[1];
    assign debug_reg2  = rf.regs[2];
    assign debug_reg3  = rf.regs[3];
    assign debug_reg4  = rf.regs[4];
    assign debug_reg5  = rf.regs[5];
    assign debug_reg6  = rf.regs[6];
    assign debug_reg7  = rf.regs[7];
    assign debug_reg8  = rf.regs[8];
    assign debug_reg9  = rf.regs[9];
    assign debug_reg10 = rf.regs[10];
    assign debug_reg11 = rf.regs[11];
    assign debug_reg12 = rf.regs[12];
    assign debug_reg13 = rf.regs[13];
    assign debug_reg14 = rf.regs[14];
    assign debug_reg15 = rf.regs[15];
    assign debug_reg28 = rf.regs[28];
    assign debug_reg29 = rf.regs[29];
    assign debug_reg30 = rf.regs[30];
    assign debug_reg31 = rf.regs[31];

    assign rs1_addr_id = instr_id[19:15];
    assign rs2_addr_id = instr_id[24:20];
    assign rd_id        = instr_id[11:7];
    assign funct3_id    = instr_id[14:12];

    assign pc_target = alu_result_ex;
    assign pc_src    = branch_taken;
    assign pc_next   = pc_src ? pc_target : pc_plus4_if;

    always @(posedge clk) begin
        if (rst) pc_current <= 32'd0;
        else     pc_current <= pc_next;
    end
    assign pc_plus4_if = pc_current + 32'd4;

    imem imem_inst (.addr(pc_current[`MEM_ADDR_WIDTH+1:2]), .instr(instr_if));

    regfile rf (.clk(clk), .rst(rst),
        .rs1_addr(rs1_addr_id), .rs2_addr(rs2_addr_id),
        .rd_addr(rd_wb), .rd_data(write_back_data),
        .rd_write_en(reg_write_wb),
        .rs1_data(rs1_data_id), .rs2_data(rs2_data_id));

    imm_gen ig (.instr(instr_id), .imm(imm_id));

    pipeline_control ctrl (.instr(instr_id),
        .stall(stall),
        .branch(branch_id), .mem_read(mem_read_id),
        .mem_to_reg(mem_to_reg_id), .alu_op(alu_op_id),
        .mem_write(mem_write_id), .alu_src(alu_src_id),
        .reg_write(reg_write_id), .alu_src_b_sel());

    assign rs1_data_ex_f = (forward_a_sel == 2'd1) ? alu_result_ex  :
                           (forward_a_sel == 2'd2) ? alu_result_mem :
                           (forward_a_sel == 2'd3) ? write_back_data : rs1_data_id;

    assign rs2_data_ex_f = (forward_b_sel == 2'd1) ? alu_result_ex  :
                           (forward_b_sel == 2'd2) ? alu_result_mem :
                           (forward_b_sel == 2'd3) ? write_back_data : rs2_data_id;

    assign alu_a = rs1_data_ex_f;
    assign alu_b = alu_src_ex ? imm_ex : rs2_data_ex_f;

    alu alu_inst (.a(alu_a), .b(alu_b), .alu_op(alu_op_ex),
                  .result(alu_result_ex));

    branch_check bc (.branch(branch_ex), .funct3(funct3_ex),
        .rs1_data(rs1_data_ex_f), .rs2_data(rs2_data_ex_f),
        .taken(branch_taken));

    dmem dmem_inst (.clk(clk), .addr(alu_result_mem[`MEM_ADDR_WIDTH+1:2]),
        .write_data(write_data_mem), .mem_read(mem_read_mem),
        .mem_write(mem_write_mem), .read_data(mem_data_mem));

    assign write_back_data = mem_to_reg_wb ? mem_data_wb : alu_result_wb;

    assign if_flush = branch_taken;
    assign id_flush = stall;

    hazard_detection hf (
        .rs1_id(rs1_addr_id), .rs2_id(rs2_addr_id),
        .rd_ex(rd_ex), .mem_read_ex(mem_read_ex),
        .rd_mem(rd_mem), .reg_write_mem(reg_write_mem),
        .rd_wb(rd_wb), .reg_write_wb(reg_write_wb),
        .stall(stall),
        .forward_a_sel(forward_a_sel), .forward_b_sel(forward_b_sel)
    );

    if_id if_id_reg (.clk(clk), .rst(rst),
        .flush(if_flush), .stall(stall),
        .pc_plus4_in(pc_plus4_if), .instr_in(instr_if),
        .pc_plus4_out(pc_plus4_id), .instr_out(instr_id));

    id_ex id_ex_reg (.clk(clk), .rst(rst), .flush(id_flush),
        .pc_plus4_in(pc_plus4_id),
        .rs1_data_in(rs1_data_id), .rs2_data_in(rs2_data_id),
        .imm_in(imm_id), .rd_in(rd_id),
        .branch_in(branch_id), .mem_read_in(mem_read_id),
        .mem_to_reg_in(mem_to_reg_id), .alu_op_in(alu_op_id),
        .mem_write_in(mem_write_id), .alu_src_in(alu_src_id),
        .reg_write_in(reg_write_id), .funct3_in(funct3_id),
        .pc_plus4_out(pc_plus4_ex),
        .rs1_data_out(rs1_data_ex), .rs2_data_out(rs2_data_ex),
        .imm_out(imm_ex), .rd_out(rd_ex),
        .branch_out(branch_ex), .mem_read_out(mem_read_ex),
        .mem_to_reg_out(mem_to_reg_ex), .alu_op_out(alu_op_ex),
        .mem_write_out(mem_write_ex), .alu_src_out(alu_src_ex),
        .reg_write_out(reg_write_ex), .funct3_out(funct3_ex));

    ex_mem ex_mem_reg (.clk(clk), .rst(rst),
        .alu_result_in(alu_result_ex), .write_data_in(rs2_data_ex_f),
        .rd_in(rd_ex),
        .branch_in(1'b0), .mem_read_in(1'b0),
        .mem_to_reg_in(mem_to_reg_ex), .mem_write_in(mem_write_ex),
        .reg_write_in(reg_write_ex),
        .alu_result_out(alu_result_mem), .write_data_out(write_data_mem),
        .rd_out(rd_mem),
        .branch_out(), .mem_read_out(mem_read_mem),
        .mem_to_reg_out(mem_to_reg_mem), .mem_write_out(mem_write_mem),
        .reg_write_out(reg_write_mem));

    mem_wb mem_wb_reg (.clk(clk), .rst(rst),
        .alu_result_in(alu_result_mem), .mem_data_in(mem_data_mem),
        .rd_in(rd_mem), .mem_to_reg_in(mem_to_reg_mem),
        .reg_write_in(reg_write_mem),
        .alu_result_out(alu_result_wb), .mem_data_out(mem_data_wb),
        .rd_out(rd_wb), .mem_to_reg_out(mem_to_reg_wb),
        .reg_write_out(reg_write_wb));
endmodule

module branch_check (
    input  branch,
    input  [`FUNCT3_WIDTH-1:0] funct3,
    input  [`WORD_WIDTH-1:0] rs1_data, rs2_data,
    output reg taken
);
    wire eq = (rs1_data == rs2_data);
    always @(*) begin
        if (!branch) taken = 0;
        else case (funct3)
            3'b000: taken = eq;
            3'b001: taken = !eq;
            3'b100: taken = ($signed(rs1_data) < $signed(rs2_data));
            3'b101: taken = ($signed(rs1_data) >= $signed(rs2_data));
            3'b110: taken = (rs1_data < rs2_data);
            3'b111: taken = (rs1_data >= rs2_data);
            default: taken = 0;
        endcase
    end
endmodule

module imem (input [`MEM_ADDR_WIDTH-1:0] addr, output [`WORD_WIDTH-1:0] instr);
    reg [`WORD_WIDTH-1:0] mem [0:255];
    initial begin
        $readmemh("/Users/Shared/ccc/mybook/ai-teach-you/co/_code/riscv/pipeline/program.txt", mem);
    end
    assign instr = mem[addr];
endmodule

module dmem (
    input  clk,
    input  [`WORD_WIDTH-1:0] addr,
    input  [`WORD_WIDTH-1:0] write_data,
    input  mem_read, mem_write,
    output [`WORD_WIDTH-1:0] read_data
);
    reg [`WORD_WIDTH-1:0] mem [0:255];
    integer i;
    initial for (i=0;i<256;i=i+1) mem[i]=32'd0;
    wire [`MEM_ADDR_WIDTH-1:0] word_addr = addr[`MEM_ADDR_WIDTH-1:0];
    always @(posedge clk) if (mem_write) mem[word_addr] <= write_data;
    assign read_data = mem_read ? mem[word_addr] : 32'd0;
endmodule
