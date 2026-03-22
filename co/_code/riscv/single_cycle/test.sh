set -x

iverilog tb_top.v -o tb_top.vvp
vvp tb_top.vvp
