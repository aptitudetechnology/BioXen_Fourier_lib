# BioXen Testing Guide

## Quick Testing

Run the comprehensive test suite:
```bash
python3 test_bioxen.py
```

Run the simple demonstration:
```bash
python3 simple_demo.py
```

Run everything with the quickstart script:
```bash
chmod +x quickstart.sh
./quickstart.sh
```

## Test Scripts

### `test_bioxen.py`
- Comprehensive test suite covering all major functionality
- Tests module imports, hypervisor operations, genetic circuits, and genome building
- Simulates the 4 development phases from the main README
- No external dependencies required

### `simple_demo.py`
- Interactive demonstration showing key BioXen concepts
- Creates multiple VMs with different priorities
- Shows resource allocation, scheduling, and genetic circuit compilation
- Easy to follow step-by-step walkthrough

### `quickstart.sh`
- Automated script that runs both tests and demo
- Checks Python installation
- Attempts to install pytest if needed
- Fallback to built-in tests if pytest unavailable

## Expected Results

If everything works correctly, you should see:
- ✅ All module imports successful
- ✅ Hypervisor creates and manages VMs
- ✅ Genetic circuits compile to DNA sequences
- ✅ VM images build with Syn3A genomes
- ✅ Multi-VM scheduling works
- ✅ All development phases simulate successfully

## Troubleshooting

**Import errors**: Make sure you're running from the BioXen directory

**Permission errors**: Run `chmod +x quickstart.sh` to make it executable

**Python version**: Requires Python 3.8 or higher

## Manual Testing

You can also test individual components:

```python
# Test hypervisor only
python3 -c "
import sys, os
sys.path.insert(0, 'src')
from hypervisor.core import BioXenHypervisor
h = BioXenHypervisor()
h.create_vm('test', 'syn3a_minimal')
print('Hypervisor works!')
"

# Test genetic circuits only
python3 -c "
import sys, os
sys.path.insert(0, 'src')
from genetics.circuits import BioCompiler
c = BioCompiler()
seqs = c.compile_hypervisor([{'vm_id': 'test'}])
print(f'Generated {len(seqs)} DNA sequences')
"
```
