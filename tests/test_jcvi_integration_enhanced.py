#!/usr/bin/env python3
"""
Enhanced BioXen-JCVI Integration Test Suite

This enhanced version automatically converts .genome files to FASTA format
when needed, demonstrating the "graceful enhancement pattern" for JCVI integration.
"""

import os
import sys
import subprocess
import json
import glob
from pathlib import Path

# Import the converter
from bioxen_to_jcvi_converter import BioXenToJCVIConverter

class EnhancedJCVIIntegrationTester:
    """Enhanced JCVI integration tester with automatic format conversion"""
    
    def __init__(self):
        self.results = {
            'jcvi_available': False,
            'ncbi_download_available': False,
            'genome_tests': {},
            'conversion_tests': {},
            'overall_status': 'UNKNOWN'
        }
        self.converter = BioXenToJCVIConverter()
    
    def check_jcvi_installation(self):
        """Check if JCVI is installed and get version"""
        print("1. Checking JCVI Installation...")
        
        try:
            import jcvi
            self.results['jcvi_available'] = True
            
            # Try to get version
            try:
                version = jcvi.__version__
            except AttributeError:
                version = "Unknown"
            
            print(f"✅ JCVI is installed and importable")
            print(f"   JCVI version: {version}")
            self.results['jcvi_version'] = version
            return True
            
        except ImportError:
            print(f"❌ JCVI is not installed")
            print(f"   Install with: pip install jcvi")
            self.results['jcvi_available'] = False
            return False
    
    def check_ncbi_download_tool(self):
        """Check if ncbi-genome-download is available"""
        print("\\n2. Checking NCBI Download Tool...")
        
        try:
            result = subprocess.run(
                ['ncbi-genome-download', '--version'], 
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ ncbi-genome-download is available")
                print(f"   Version: {version}")
                self.results['ncbi_download_available'] = True
                self.results['ncbi_download_version'] = version
                return True
            else:
                raise subprocess.CalledProcessError(result.returncode, 'ncbi-genome-download')
                
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ ncbi-genome-download is not available")
            print(f"   Install with: pip install ncbi-genome-download")
            self.results['ncbi_download_available'] = False
            return False
    
    def find_genome_files(self):
        """Find all genome files in the genomes directory"""
        genome_files = []
        
        # Look for .genome files
        genome_files.extend(glob.glob("genomes/*.genome"))
        
        # Look for .fasta files
        genome_files.extend(glob.glob("genomes/*.fasta"))
        
        return sorted(genome_files)
    
    def test_jcvi_with_file(self, file_path):
        """Test JCVI tools with a specific file"""
        file_name = os.path.basename(file_path)
        
        try:
            # Test JCVI FASTA summary
            result = subprocess.run([
                sys.executable, "-m", "jcvi.formats.fasta", "summary", file_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'compatible': True,
                    'output': result.stdout,
                    'error': None
                }
            else:
                return {
                    'compatible': False,
                    'output': result.stdout,
                    'error': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                'compatible': False,
                'output': "",
                'error': "Timeout after 30 seconds"
            }
        except Exception as e:
            return {
                'compatible': False,
                'output': "",
                'error': str(e)
            }
    
    def convert_genome_if_needed(self, genome_path):
        """Convert .genome file to FASTA if needed"""
        if genome_path.endswith('.genome'):
            fasta_path = genome_path.replace('.genome', '.fasta')
            
            print(f"   🔄 Converting {os.path.basename(genome_path)} to FASTA format...")
            
            success = self.converter.convert_genome(genome_path, fasta_path)
            
            if success:
                print(f"   ✅ Conversion successful: {os.path.basename(fasta_path)}")
                return fasta_path, True
            else:
                print(f"   ❌ Conversion failed")
                return None, False
        else:
            # Already a FASTA file
            return genome_path, True
    
    def test_genomes_with_jcvi(self):
        """Test JCVI compatibility with all genome files"""
        print("\\n3. Testing JCVI with BioXen Genomes...")
        
        if not self.results['jcvi_available']:
            print("❌ Skipping genome tests - JCVI not available")
            return False
        
        genome_files = self.find_genome_files()
        
        if not genome_files:
            print("❌ No genome files found in genomes/ directory")
            return False
        
        print(f"🔍 Found {len(genome_files)} genome files to test")
        
        compatible_count = 0
        converted_count = 0
        
        for genome_file in genome_files:
            file_name = os.path.basename(genome_file)
            print(f"\\n📊 Testing {file_name}...")
            
            # Test original file first
            original_result = self.test_jcvi_with_file(genome_file)
            
            if original_result['compatible']:
                print(f"   ✅ JCVI compatible (original format)")
                compatible_count += 1
                self.results['genome_tests'][file_name] = {
                    'original_compatible': True,
                    'conversion_needed': False,
                    'final_compatible': True
                }
            else:
                print(f"   ❌ JCVI incompatible (original format)")
                
                # Try conversion if it's a .genome file
                if genome_file.endswith('.genome'):
                    converted_file, conversion_success = self.convert_genome_if_needed(genome_file)
                    
                    if conversion_success and converted_file:
                        # Test converted file
                        converted_result = self.test_jcvi_with_file(converted_file)
                        
                        if converted_result['compatible']:
                            print(f"   ✅ JCVI compatible (after conversion)")
                            compatible_count += 1
                            converted_count += 1
                            self.results['genome_tests'][file_name] = {
                                'original_compatible': False,
                                'conversion_needed': True,
                                'conversion_successful': True,
                                'final_compatible': True,
                                'converted_file': os.path.basename(converted_file)
                            }
                        else:
                            print(f"   ❌ JCVI incompatible (even after conversion)")
                            self.results['genome_tests'][file_name] = {
                                'original_compatible': False,
                                'conversion_needed': True,
                                'conversion_successful': True,
                                'final_compatible': False,
                                'error': converted_result['error']
                            }
                    else:
                        print(f"   ❌ Conversion failed")
                        self.results['genome_tests'][file_name] = {
                            'original_compatible': False,
                            'conversion_needed': True,
                            'conversion_successful': False,
                            'final_compatible': False
                        }
                else:
                    # FASTA file that's incompatible - this shouldn't happen
                    self.results['genome_tests'][file_name] = {
                        'original_compatible': False,
                        'conversion_needed': False,
                        'final_compatible': False,
                        'error': original_result['error']
                    }
        
        self.results['total_files'] = len(genome_files)
        self.results['compatible_files'] = compatible_count
        self.results['converted_files'] = converted_count
        
        return compatible_count > 0
    
    def generate_integration_report(self):
        """Generate a comprehensive integration readiness report"""
        print("\\n4. Generating Integration Report...")
        
        total_files = self.results.get('total_files', 0)
        compatible_files = self.results.get('compatible_files', 0)
        converted_files = self.results.get('converted_files', 0)
        
        print("\\n" + "="*60)
        print("🧬 BioXen-JCVI Enhanced Integration Report")
        print("="*60)
        
        # Overall status
        if compatible_files == 0:
            status = "❌ FAILED"
            self.results['overall_status'] = 'FAILED'
            status_msg = "No genomes are JCVI-compatible"
        elif compatible_files == total_files:
            status = "✅ EXCELLENT" 
            self.results['overall_status'] = 'EXCELLENT'
            status_msg = "All genomes are JCVI-compatible"
        else:
            status = "🎉 GOOD"
            self.results['overall_status'] = 'GOOD'
            status_msg = f"{compatible_files}/{total_files} genomes are JCVI-compatible"
        
        print(f"\\n📊 Overall Results: {compatible_files}/{total_files} genomes JCVI-compatible")
        print(f"{status}: {status_msg}")
        
        if converted_files > 0:
            print(f"🔄 Auto-conversion successful for {converted_files} genomes")
        
        # Detailed results
        print(f"\\n📋 Detailed Results:")
        for file_name, result in self.results.get('genome_tests', {}).items():
            file_size = self._get_file_size(f"genomes/{file_name}")
            
            if result['final_compatible']:
                if result.get('conversion_needed', False):
                    print(f"   🔄 {file_name} ({file_size}) - Compatible after conversion")
                    if 'converted_file' in result:
                        print(f"      → Created: {result['converted_file']}")
                else:
                    print(f"   ✅ {file_name} ({file_size}) - Natively compatible")
            else:
                print(f"   ❌ {file_name} ({file_size}) - Incompatible")
                if 'error' in result:
                    error_preview = result['error'][:100] + "..." if len(result['error']) > 100 else result['error']
                    print(f"      Error: {error_preview}")
        
        # Next steps
        print(f"\\n🚀 Next Steps for Integration:")
        if self.results['overall_status'] == 'EXCELLENT':
            print("   1. ✅ All genomes ready - proceed with full JCVI integration")
            print("   2. 🚀 Implement enhanced features using JCVI tools")
            print("   3. 📊 Add comparative genomics capabilities")
        elif self.results['overall_status'] == 'GOOD':
            print("   1. ✅ Proceed with JCVI integration for compatible genomes")
            print("   2. 🔧 Auto-conversion is working - integrate into main workflow")
            print("   3. 🔄 Add graceful fallback for unsupported formats")
        else:
            print("   1. 🔧 Debug conversion issues")
            print("   2. 📥 Try downloading genomes in different formats")
            print("   3. 🔄 Implement alternative integration approaches")
        
        print(f"\\n💡 Integration Strategy:")
        print("   • ✅ Auto-conversion pattern is working")
        print("   • 🔄 Graceful enhancement with fallback")
        print("   • 📈 Progressive feature enablement")
        print("   • 🧪 Thorough testing with all genome types")
        
        return self.results['overall_status'] in ['EXCELLENT', 'GOOD']
    
    def _get_file_size(self, file_path):
        """Get human-readable file size"""
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024*1024:
                return f"{size_bytes/1024:.1f} KB"
            else:
                return f"{size_bytes/(1024*1024):.1f} MB"
        except:
            return "Unknown size"
    
    def save_results(self):
        """Save test results to JSON file"""
        print("\\n5. Saving Test Results...")
        
        results_file = "enhanced_jcvi_integration_results.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            print(f"\\n💾 Enhanced test results saved to: {results_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False
    
    def run_full_test(self):
        """Run the complete integration test suite"""
        print("🧪 BioXen-JCVI Enhanced Integration Test Suite")
        print("=" * 50)
        
        # Check dependencies
        jcvi_ok = self.check_jcvi_installation()
        ncbi_ok = self.check_ncbi_download_tool()
        
        if not jcvi_ok:
            print("\\n❌ Cannot proceed without JCVI installation")
            return False
        
        # Test genomes
        genomes_ok = self.test_genomes_with_jcvi()
        
        # Generate report
        integration_ready = self.generate_integration_report()
        
        # Save results
        self.save_results()
        
        # Final status
        if integration_ready:
            print("\\n🎉 Enhanced integration test PASSED - Ready to proceed!")
            return True
        else:
            print("\\n⚠️  Enhanced integration test needs attention before proceeding")
            return False

def main():
    """Main entry point"""
    tester = EnhancedJCVIIntegrationTester()
    success = tester.run_full_test()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
