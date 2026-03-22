`include "defs.v"

module alu (
    input  [`WORD_WIDTH-1:0] a,
    input  [`WORD_WIDTH-1:0] b,
    input  [`ALU_OP_WIDTH-1:0] alu_op,
    output reg [`WORD_WIDTH-1:0] result
);
    always @(*) begin
        case (alu_op)
            `ALU_OP_ADD:  result = a + b;
            `ALU_OP_SUB:  result = a - b;
            `ALU_OP_SLL:  result = a << b[4:0];
            `ALU_OP_SLT:  result = ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
            `ALU_OP_SLTU: result = (a < b) ? 32'd1 : 32'd0;
            `ALU_OP_XOR:  result = a ^ b;
            `ALU_OP_SRL:  result = a >> b[4:0];
            `ALU_OP_SRA:  result = $signed(a) >>> b[4:0];
            `ALU_OP_OR:   result = a | b;
            `ALU_OP_AND:  result = a & b;
            default:      result = 32'd0;
        endcase
    end
endmodule
