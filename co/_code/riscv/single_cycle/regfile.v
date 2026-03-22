`include "defs.v"

module regfile (
    input  clk,
    input  rst,
    input  [`REG_ADDR_WIDTH-1:0] rs1_addr,
    input  [`REG_ADDR_WIDTH-1:0] rs2_addr,
    input  [`REG_ADDR_WIDTH-1:0] rd_addr,
    input  [`WORD_WIDTH-1:0] rd_data,
    input  rd_write_en,
    output [`WORD_WIDTH-1:0] rs1_data,
    output [`WORD_WIDTH-1:0] rs2_data
);
    reg [`WORD_WIDTH-1:0] regs [0:31];

    integer i;
    always @(posedge clk) begin
        if (rst) begin
            for (i = 0; i < 32; i = i + 1)
                regs[i] <= 32'd0;
        end else begin
            if (rd_write_en && rd_addr != 5'd0) begin
                regs[rd_addr] <= rd_data;
            end
        end
    end

    assign rs1_data = (rs1_addr == 5'd0) ? 32'd0 : regs[rs1_addr];
    assign rs2_data = (rs2_addr == 5'd0) ? 32'd0 : regs[rs2_addr];
endmodule
