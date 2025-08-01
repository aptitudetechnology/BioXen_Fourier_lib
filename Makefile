# Makefile for BioXen Project

.PHONY: install dev-install test lint format clean demo benchmark

# Default Python interpreter
PYTHON := python3

# Install for production use
install:
	$(PYTHON) -m pip install .

# Install for development
dev-install:
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install -r requirements.txt

# Run tests
test:
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Run linting
lint:
	$(PYTHON) -m flake8 src/ tests/ demo.py
	$(PYTHON) -m mypy src/

# Format code
format:
	$(PYTHON) -m black src/ tests/ demo.py

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run demo
demo:
	$(PYTHON) demo.py

# Run quick demo (no benchmark)
demo-quick:
	echo "Running quick BioXen demo..."
	$(PYTHON) -c "from demo import demo_basic_vm_operations, demo_vm_image_builder, demo_genetic_circuits; demo_basic_vm_operations(); demo_vm_image_builder(); demo_genetic_circuits()"

# Run full benchmark suite
benchmark:
	$(PYTHON) -c "from demo import demo_benchmark_suite; demo_benchmark_suite()"

# Create VM image
create-vm:
	$(PYTHON) -c "from src.genome.syn3a import VMImageBuilder; builder = VMImageBuilder(); image = builder.build_vm_image('example-vm', {}); builder.save_vm_image(image, 'example-vm.json'); print('VM image saved to example-vm.json')"

# Compile hypervisor DNA
compile-dna:
	$(PYTHON) -c "from src.genetics.circuits import BioCompiler; import json; compiler = BioCompiler(); sequences = compiler.compile_hypervisor([{'vm_id': 'vm1'}, {'vm_id': 'vm2'}]); json.dump(sequences, open('hypervisor.json', 'w'), indent=2); print('Hypervisor DNA saved to hypervisor.json')"

# Show project structure
tree:
	tree -I '__pycache__|*.pyc|.git|.pytest_cache|htmlcov|*.egg-info'

# Help
help:
	@echo "BioXen Makefile Commands:"
	@echo "  install      - Install BioXen for production use"
	@echo "  dev-install  - Install BioXen for development"
	@echo "  test         - Run test suite"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  demo         - Run full interactive demo"
	@echo "  demo-quick   - Run quick demo without benchmarks"
	@echo "  benchmark    - Run benchmark suite"
	@echo "  create-vm    - Create example VM image"
	@echo "  compile-dna  - Compile hypervisor DNA sequences"
	@echo "  tree         - Show project structure"
	@echo "  help         - Show this help message"
