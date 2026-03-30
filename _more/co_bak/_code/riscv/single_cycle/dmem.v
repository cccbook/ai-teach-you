`include "defs.v"

module dmem (
    input  clk,
    input  [`WORD_WIDTH-1:0] addr,
    input  [`WORD_WIDTH-1:0] write_data,
    input  mem_read,
    input  mem_write,
    output [`WORD_WIDTH-1:0] read_data
);
    reg [`WORD_WIDTH-1:0] mem [0:255];

    integer i;
    initial begin
        for (i = 0; i < 256; i = i + 1)
            mem[i] = 32'd0;
    end

    wire [`MEM_ADDR_WIDTH-1:0] word_addr = addr[`MEM_ADDR_WIDTH-1:0];

    always @(posedge clk) begin
        if (mem_write) begin
            mem[word_addr] <= write_data;
        end
    end

    assign read_data = mem_read ? mem[word_addr] : 32'd0;
endmodule
