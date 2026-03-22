`ifndef DEFS_V
`define DEFS_V

`define WORD_WIDTH 32
`define REG_ADDR_WIDTH 5
`define ALU_OP_WIDTH 4
`define MEM_ADDR_WIDTH 8

`define OPCODE_WIDTH 7
`define FUNCT3_WIDTH 3
`define FUNCT7_WIDTH 7

`define OPCODE_LUI     7'b0110111
`define OPCODE_AUIPC   7'b0010111
`define OPCODE_JAL     7'b1101111
`define OPCODE_JALR    7'b1100111
`define OPCODE_BRANCH  7'b1100011
`define OPCODE_LOAD    7'b0000011
`define OPCODE_STORE   7'b0100011
`define OPCODE_OP_IMM  7'b0010011
`define OPCODE_OP      7'b0110011

`define F3_ADD_SUB 3'b000
`define F3_SLL     3'b001
`define F3_SLT     3'b010
`define F3_SLTU    3'b011
`define F3_XOR     3'b100
`define F3_SRL_SRA 3'b101
`define F3_OR      3'b110
`define F3_AND     3'b111

`define F7_ADD  7'b0000000
`define F7_SUB  7'b0100000
`define F7_SLL  7'b0000000
`define F7_SRL  7'b0000000
`define F7_SRA  7'b0100000

`define ALU_OP_ADD  4'd0
`define ALU_OP_SUB  4'd1
`define ALU_OP_SLL  4'd2
`define ALU_OP_SLT  4'd3
`define ALU_OP_SLTU 4'd4
`define ALU_OP_XOR  4'd5
`define ALU_OP_SRL  4'd6
`define ALU_OP_SRA  4'd7
`define ALU_OP_OR   4'd8
`define ALU_OP_AND  4'd9

`endif
