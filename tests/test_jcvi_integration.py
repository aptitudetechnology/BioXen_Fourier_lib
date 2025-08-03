#!/usr/bin/env python3
"""
BioXen-JCVI Integration Test Script
Test JCVI compatibility with BioXen genomes and prepare for integration.
"""

import subprocess
import sys
import json
from pathlib import Path

def check_jcvi_installation():
    """Check if JCVI is properly installed."""
    try:
        result = subprocess.run([
            sys.executable, "-c", "import jcvi; print(f'JCVI version: {jcvi.__version__}')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ JCVI is installed and importable")
            print(f"   {result.stdout.strip()}")
            return True
        else:
            print("❌ JCVI import failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ JCVI import test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing JCVI: {e}")
        return False

def check_ncbi_download_tool():
    """Check if ncbi-genome-download is available."""
    try:
        result = subprocess.run([
            'ncbi-genome-download', '--version'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ ncbi-genome-download is available")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ ncbi-genome-download not found")
            return False
    except FileNotFoundError:
        print("❌ ncbi-genome-download not installed")
        print("   Install with: pip install ncbi-genome-download")
        return False
    except Exception as e:
        print(f"❌ Error checking ncbi-genome-download: {e}")
        return False

def test_jcvi_with_bioxen_genomes():
    """Test JCVI tools with BioXen genome files."""
    
    # Look for genome files in the genomes directory
    genomes_dir = Path("genomes")
    
    if not genomes_dir.exists():
        print("❌ No genomes directory found")
        print("   Run 'python3 download_genomes.py' first to get genomes")
        return {}
    
    genome_files = list(genomes_dir.glob("*.genome")) + list(genomes_dir.glob("*.fasta")) + list(genomes_dir.glob("*.fa"))
    
    if not genome_files:
        print("❌ No genome files found in genomes/ directory")
        print("   Run 'python3 download_genomes.py' first to get genomes")
        return {}
    
    print(f"🔍 Found {len(genome_files)} genome files to test")
    
    results = {}
    
    for genome_file in genome_files:
        print(f"\n📊 Testing {genome_file.name}...")
        
        try:
            # Test JCVI FASTA summary
            result = subprocess.run([
                sys.executable, "-m", "jcvi.formats.fasta", "summary", str(genome_file)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ JCVI FASTA summary successful")
                
                # Parse summary output
                summary_lines = result.stdout.strip().split('\\n')
                summary_data = {}
                for line in summary_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        summary_data[key.strip()] = value.strip()
                
                results[str(genome_file)] = {
                    'jcvi_compatible': True,
                    'summary_output': result.stdout,
                    'summary_data': summary_data,
                    'file_size_bytes': genome_file.stat().st_size,
                    'errors': None
                }
            else:
                print(f"   ❌ JCVI FASTA summary failed: {result.stderr.strip()}")
                results[str(genome_file)] = {
                    'jcvi_compatible': False,
                    'error': result.stderr.strip(),
                    'file_size_bytes': genome_file.stat().st_size
                }
                
        except subprocess.TimeoutExpired:
            print("   ❌ JCVI test timed out (>30 seconds)")
            results[str(genome_file)] = {
                'jcvi_compatible': False,
                'error': 'Timeout after 30 seconds',
                'file_size_bytes': genome_file.stat().st_size
            }
        except Exception as e:
            print(f"   ❌ Error testing with JCVI: {e}")
            results[str(genome_file)] = {
                'jcvi_compatible': False,
                'error': str(e),
                'file_size_bytes': genome_file.stat().st_size
            }
    
    return results

def generate_integration_report(results):
    """Generate a comprehensive integration readiness report."""
    
    print("\\n" + "="*60)
    print("🧬 BioXen-JCVI Integration Readiness Report")
    print("="*60)
    
    compatible_count = sum(1 for r in results.values() if r.get('jcvi_compatible', False))
    total_count = len(results)
    
    print(f"\\n📊 Overall Results: {compatible_count}/{total_count} genomes JCVI-compatible")
    
    if compatible_count == total_count and total_count > 0:
        print("🎉 EXCELLENT: All genomes are JCVI-compatible!")
        print("✅ Ready for full JCVI integration")
    elif compatible_count > 0:
        print("⚠️  PARTIAL: Some genomes are JCVI-compatible")
        print("🔄 Consider format conversion for incompatible genomes")
    else:
        print("❌ POOR: No genomes are JCVI-compatible")
        print("🔧 Need to implement format conversion before integration")
    
    print("\\n📋 Detailed Results:")
    for genome_path, result in results.items():
        genome_name = Path(genome_path).name
        status = "✅" if result.get('jcvi_compatible') else "❌"
        size_kb = result.get('file_size_bytes', 0) / 1024
        
        print(f"   {status} {genome_name} ({size_kb:.1f} KB)")
        
        if not result.get('jcvi_compatible'):
            error = result.get('error', 'Unknown error')
            print(f"      Error: {error}")
        else:
            summary_data = result.get('summary_data', {})
            if summary_data:
                print(f"      Statistics available via JCVI")
    
    print("\\n🚀 Next Steps for Integration:")
    
    if compatible_count == total_count and total_count > 0:
        print("   1. ✅ Proceed with Phase 1: Enhanced Parser Implementation")
        print("   2. ✅ Add JCVI dependency to requirements.txt")
        print("   3. ✅ Implement JCVIEnhancedGenomeParser class")
        print("   4. ✅ Add enhanced statistics to interactive interface")
    elif compatible_count > 0:
        print("   1. 🔧 Implement format conversion for incompatible genomes")
        print("   2. ✅ Proceed with JCVI integration for compatible genomes")
        print("   3. 🔄 Add fallback mechanisms for unsupported formats")
    else:
        print("   1. 🔧 Implement comprehensive format conversion")
        print("   2. 📥 Download genomes in JCVI-compatible formats")
        print("   3. 🔄 Re-run this test after format improvements")
    
    print("\\n💡 Integration Strategy:")
    print("   • Start with graceful enhancement pattern")
    print("   • Maintain backward compatibility")
    print("   • Add JCVI features progressively")
    print("   • Test thoroughly with all genome types")
    
    return {
        'compatible_count': compatible_count,
        'total_count': total_count,
        'ready_for_integration': compatible_count > 0,
        'full_compatibility': compatible_count == total_count and total_count > 0
    }

def save_test_results(results, summary):
    """Save test results to JSON file for future reference."""
    
    report_data = {
        'test_timestamp': str(Path(__file__).stat().st_mtime),
        'bioxen_jcvi_integration_test': {
            'summary': summary,
            'detailed_results': results,
            'recommendations': {
                'ready_for_integration': summary['ready_for_integration'],
                'next_phase': 'enhanced_parser' if summary['full_compatibility'] else 'format_conversion',
                'priority_actions': [
                    'Add JCVI to requirements.txt',
                    'Implement JCVIEnhancedGenomeParser',
                    'Add comparative genomics features'
                ] if summary['ready_for_integration'] else [
                    'Fix genome format compatibility',
                    'Re-test JCVI integration',
                    'Implement format converters'
                ]
            }
        }
    }
    
    report_file = Path("jcvi_integration_test_results.json")
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\\n💾 Test results saved to: {report_file}")

def main():
    """Run the complete BioXen-JCVI integration test suite."""
    
    print("🧪 BioXen-JCVI Integration Test Suite")
    print("=====================================")
    
    # Step 1: Check JCVI installation
    print("\\n1. Checking JCVI Installation...")
    jcvi_available = check_jcvi_installation()
    
    if not jcvi_available:
        print("\\n❌ JCVI not available. Install with:")
        print("   pip install jcvi")
        print("\\nℹ️  Note: JCVI requires Python 3.9-3.12")
        return 1
    
    # Step 2: Check ncbi-genome-download
    print("\\n2. Checking NCBI Download Tool...")
    ncbi_tool_available = check_ncbi_download_tool()
    
    # Step 3: Test JCVI with BioXen genomes
    print("\\n3. Testing JCVI with BioXen Genomes...")
    test_results = test_jcvi_with_bioxen_genomes()
    
    # Step 4: Generate integration report
    print("\\n4. Generating Integration Report...")
    summary = generate_integration_report(test_results)
    
    # Step 5: Save results
    print("\\n5. Saving Test Results...")
    save_test_results(test_results, summary)
    
    # Return appropriate exit code
    if summary['ready_for_integration']:
        print("\\n🎉 Integration test PASSED - Ready to proceed!")
        return 0
    else:
        print("\\n⚠️  Integration test needs attention before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())
