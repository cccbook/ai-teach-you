.PHONY: all run clean

all:
	iverilog -o tb_top.vvp -s tb_top \
		tb_top.v top.v datapath.v control.v alu.v \
		regfile.v imem.v dmem.v imm_gen.v defs.v

run: all
	vvp tb_top.vvp

clean:
	rm -f tb_top.vvp *.vvp
