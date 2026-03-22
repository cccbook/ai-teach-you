`include "defs.v"

module control (
    input  [`OPCODE_WIDTH-1:0] opcode,
    input  [`FUNCT3_WIDTH-1:0] funct3,
    input  [`FUNCT7_WIDTH-1:0] funct7,
    output reg branch,
    output reg mem_read,
    output reg mem_to_reg,
    output reg [`ALU_OP_WIDTH-1:0] alu_op,
    output reg mem_write,
    output reg alu_src,
    output reg reg_write,
    output reg [1:0] alu_src_b_sel
);
    always @(*) begin
        branch = 0; mem_read = 0; mem_to_reg = 0;
        alu_op = 4'd0; mem_write = 0; alu_src = 0; reg_write = 0;
        alu_src_b_sel = 2'd0;

        case (opcode)
            `OPCODE_OP: begin
                reg_write = 1;
                alu_src = 0;
                alu_src_b_sel = 2'd0;
                mem_to_reg = 0;
                case ({funct7, funct3})
                    {`F7_ADD,  `F3_ADD_SUB}: alu_op = `ALU_OP_ADD;
                    {`F7_SUB,  `F3_ADD_SUB}: alu_op = `ALU_OP_SUB;
                    {`F7_SLL,  `F3_SLL}:     alu_op = `ALU_OP_SLL;
                    {7'b0000000, `F3_SLT}:   alu_op = `ALU_OP_SLT;
                    {7'b0000000, `F3_SLTU}:  alu_op = `ALU_OP_SLTU;
                    {7'b0000000, `F3_XOR}:   alu_op = `ALU_OP_XOR;
                    {`F7_SRL,  `F3_SRL_SRA}: alu_op = `ALU_OP_SRL;
                    {`F7_SRA,  `F3_SRL_SRA}: alu_op = `ALU_OP_SRA;
                    {7'b0000000, `F3_OR}:    alu_op = `ALU_OP_OR;
                    {7'b0000000, `F3_AND}:   alu_op = `ALU_OP_AND;
                    default:                alu_op = `ALU_OP_ADD;
                endcase
            end

            `OPCODE_OP_IMM: begin
                reg_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd1;
                mem_to_reg = 0;
                case (funct3)
                    3'b000: alu_op = `ALU_OP_ADD;
                    3'b001: alu_op = `ALU_OP_SLL;
                    3'b010: alu_op = `ALU_OP_SLT;
                    3'b011: alu_op = `ALU_OP_SLTU;
                    3'b100: alu_op = `ALU_OP_XOR;
                    3'b101: alu_op = (funct7[5]) ? `ALU_OP_SRA : `ALU_OP_SRL;
                    3'b110: alu_op = `ALU_OP_OR;
                    3'b111: alu_op = `ALU_OP_AND;
                    default: alu_op = `ALU_OP_ADD;
                endcase
            end

            `OPCODE_LUI: begin
                reg_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd2;
                mem_to_reg = 0;
                alu_op = `ALU_OP_OR;
            end

            `OPCODE_AUIPC: begin
                reg_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd2;
                mem_to_reg = 0;
                alu_op = `ALU_OP_ADD;
            end

            `OPCODE_JAL: begin
                reg_write = 1;
                alu_src_b_sel = 2'd0;
                mem_to_reg = 2;
                alu_op = `ALU_OP_ADD;
            end

            `OPCODE_JALR: begin
                reg_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd1;
                mem_to_reg = 2;
                alu_op = `ALU_OP_ADD;
            end

            `OPCODE_BRANCH: begin
                branch = 1;
                alu_src_b_sel = 2'd0;
                case (funct3)
                    3'b000: alu_op = `ALU_OP_SUB;
                    3'b001: alu_op = `ALU_OP_SUB;
                    3'b100: alu_op = `ALU_OP_SLT;
                    3'b101: alu_op = `ALU_OP_SLT;
                    3'b110: alu_op = `ALU_OP_SLTU;
                    3'b111: alu_op = `ALU_OP_SLTU;
                    default: alu_op = `ALU_OP_SUB;
                endcase
            end

            `OPCODE_LOAD: begin
                reg_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd1;
                mem_read = 1;
                mem_to_reg = 1;
                alu_op = `ALU_OP_ADD;
            end

            `OPCODE_STORE: begin
                mem_write = 1;
                alu_src = 1;
                alu_src_b_sel = 2'd1;
                alu_op = `ALU_OP_ADD;
            end

            default: begin
                branch = 0; mem_read = 0; mem_to_reg = 0;
                alu_op = 4'd0; mem_write = 0; alu_src = 0; reg_write = 0;
            end
        endcase
    end
endmodule
