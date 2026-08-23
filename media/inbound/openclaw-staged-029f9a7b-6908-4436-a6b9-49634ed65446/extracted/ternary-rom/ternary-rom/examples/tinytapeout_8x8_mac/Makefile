TERNARY_ROM_ROOT := ../..
BUILD_DIR     := ./build
SRC_DIR       := ./src
VLOG_FILES    := $(SRC_DIR)/ternary_mac_8x8.v $(SRC_DIR)/ternary_mac_8x8_tb.v
TOP_MODULE    := ternary_mac_8x8_tb

.PHONY: all generate sim synth clean

all: generate

generate:
	@echo "=== Generating design files with ternary-rom ==="
	python3 generate.py

sim: generate
	@echo "=== Running Verilog simulation (iverilog) ==="
	iverilog -o $(BUILD_DIR)/sim.vvp $(VLOG_FILES)
	vvp $(BUILD_DIR)/sim.vvp

synth: generate
	@echo "=== Running synthesis (yosys) ==="
	yosys -p "read_verilog $(SRC_DIR)/ternary_mac_8x8.v; synth -top ternary_mac_8x8; stat" \
		-o $(BUILD_DIR)/synth.v

clean:
	rm -rf $(BUILD_DIR)
	@echo "Build directory removed."
