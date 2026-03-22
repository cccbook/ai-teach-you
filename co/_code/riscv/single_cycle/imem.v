`include "defs.v"

module imem (
    input  [`MEM_ADDR_WIDTH-1:0] addr,
    output [`WORD_WIDTH-1:0] instr
);
    reg [`WORD_WIDTH-1:0] mem [0:255];

    initial begin
        $readmemh("/Users/Shared/ccc/mybook/ai-teach-you/co/_code/riscv/single_cycle/program.txt", mem);
        $display("imem: loaded program.txt, addr[0]=%h addr[1]=%h addr[2]=%h addr[3]=%h",
                 mem[0], mem[1], mem[2], mem[3]);
    end

    assign instr = mem[addr];
endmodule
