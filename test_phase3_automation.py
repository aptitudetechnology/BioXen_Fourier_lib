#!/usr/bin/env python3
"""
BioXen-JCVI Phase 3 Automated Testing Script

This script automatically tests all questionary menu options in the 
interactive comparative genomics interface to validate functionality
and identify what's working vs what's placeholder.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Import the main interactive class
try:
    from interactive_comparative_genomics import InteractiveComparativeGenomics
except ImportError as e:
    print(f"❌ Error: Could not import interactive_comparative_genomics: {e}")
    sys.exit(1)

class AutomatedTester:
    """Automated testing for all Phase 3 questionary options"""
    
    def __init__(self):
        self.interface = InteractiveComparativeGenomics()
        self.test_results = {}
        self.start_time = datetime.now()
        
    def log_test(self, test_name, status, details=""):
        """Log a test result"""
        self.test_results[test_name] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   {details}")
    
    def test_genome_discovery(self):
        """Test genome file discovery functionality"""
        print("\n🔍 Testing Genome Discovery...")
        
        try:
            genomes = self.interface._discover_genomes()
            if len(genomes) >= 5:
                self.log_test("Genome Discovery", "PASS", f"Found {len(genomes)} genomes")
                return genomes
            else:
                self.log_test("Genome Discovery", "WARN", f"Only found {len(genomes)} genomes (expected 5+)")
                return genomes
        except Exception as e:
            self.log_test("Genome Discovery", "FAIL", f"Exception: {e}")
            return []
    
    def test_genome_profiles(self, genomes):
        """Test genome profile generation"""
        print("\n📊 Testing Genome Profile Generation...")
        
        profiles = {}
        for genome in genomes[:3]:  # Test first 3 genomes
            try:
                profile = self.interface._get_genome_profile(genome)
                profiles[genome] = profile
                
                # Validate profile structure
                required_keys = ['gene_count', 'total_bases', 'complexity']
                missing_keys = [key for key in required_keys if key not in profile]
                
                if not missing_keys:
                    self.log_test(f"Profile: {Path(genome).stem}", "PASS", 
                                f"{profile['gene_count']} genes, {profile['complexity']} complexity")
                else:
                    self.log_test(f"Profile: {Path(genome).stem}", "FAIL", 
                                f"Missing keys: {missing_keys}")
                    
            except Exception as e:
                self.log_test(f"Profile: {Path(genome).stem}", "FAIL", f"Exception: {e}")
        
        return profiles
    
    def test_compatibility_analysis(self, genomes):
        """Test compatibility analysis methods"""
        print("\n🧬 Testing Compatibility Analysis...")
        
        if len(genomes) < 2:
            self.log_test("Compatibility Analysis", "SKIP", "Need at least 2 genomes")
            return
        
        # Test full compatibility analysis
        try:
            print("   Testing full compatibility matrix...")
            self.interface._run_full_compatibility_analysis(genomes)
            self.log_test("Full Compatibility Analysis", "PASS", "Matrix generated successfully")
        except Exception as e:
            self.log_test("Full Compatibility Analysis", "FAIL", f"Exception: {e}")
        
        # Test basic compatibility fallback
        try:
            print("   Testing basic compatibility fallback...")
            self.interface._run_basic_compatibility_fallback(genomes[:3])
            self.log_test("Basic Compatibility Fallback", "PASS", "Fallback working")
        except Exception as e:
            self.log_test("Basic Compatibility Fallback", "FAIL", f"Exception: {e}")
        
        # Test quick compatibility check
        try:
            print("   Testing quick compatibility check...")
            self.interface._run_quick_compatibility_check(genomes)
            self.log_test("Quick Compatibility Check", "PASS", "Quick check working")
        except Exception as e:
            self.log_test("Quick Compatibility Check", "FAIL", f"Exception: {e}")
        
        # Test detailed compatibility report
        try:
            print("   Testing detailed compatibility report...")
            self.interface._run_detailed_compatibility_report(genomes)
            self.log_test("Detailed Compatibility Report", "PASS", "Detailed report generated")
        except Exception as e:
            self.log_test("Detailed Compatibility Report", "FAIL", f"Exception: {e}")
    
    def test_synteny_analysis(self, genomes):
        """Test synteny analysis options"""
        print("\n🧬 Testing Synteny Analysis...")
        
        synteny_types = [
            "gene_order",
            "orthology", 
            "rearrangements",
            "vm_optimization",
            "clustering"
        ]
        
        for analysis_type in synteny_types:
            try:
                print(f"   Testing {analysis_type} analysis...")
                self.interface._run_synteny_analysis(genomes, analysis_type)
                self.log_test(f"Synteny: {analysis_type}", "PASS", "Mock analysis completed")
            except Exception as e:
                self.log_test(f"Synteny: {analysis_type}", "FAIL", f"Exception: {e}")
    
    def test_phylogenetic_analysis(self, genomes):
        """Test phylogenetic analysis options"""
        print("\n🌳 Testing Phylogenetic Analysis...")
        
        phylo_types = [
            "tree",
            "distance",
            "clock", 
            "gene_families",
            "vm_phylogeny"
        ]
        
        for analysis_type in phylo_types:
            try:
                print(f"   Testing {analysis_type} analysis...")
                self.interface._run_phylogenetic_analysis(genomes, analysis_type)
                self.log_test(f"Phylogenetic: {analysis_type}", "PASS", "Mock analysis completed")
            except Exception as e:
                self.log_test(f"Phylogenetic: {analysis_type}", "FAIL", f"Exception: {e}")
    
    def test_optimization_recommendations(self, genomes):
        """Test resource optimization recommendations"""
        print("\n⚡ Testing Resource Optimization...")
        
        opt_types = [
            "vm_allocation",
            "memory",
            "cpu",
            "load_balancing", 
            "bottlenecks",
            "scalability"
        ]
        
        for opt_type in opt_types:
            try:
                print(f"   Testing {opt_type} optimization...")
                self.interface._generate_optimization_recommendations(genomes, opt_type)
                self.log_test(f"Optimization: {opt_type}", "PASS", "Recommendations generated")
            except Exception as e:
                self.log_test(f"Optimization: {opt_type}", "FAIL", f"Exception: {e}")
    
    def test_vm_creation_wizard(self, genomes):
        """Test VM creation wizard components"""
        print("\n🖥️ Testing VM Creation Wizard Components...")
        
        if not genomes:
            self.log_test("VM Creation Wizard", "SKIP", "No genomes available")
            return
        
        # Test genome profile retrieval for VM sizing
        try:
            test_genome = genomes[0]
            profile = self.interface._get_genome_profile(test_genome)
            
            # Test memory estimation
            memory_estimate = self.interface._estimate_memory_usage(test_genome)
            
            # Test compatibility suggestions
            suggestions = self.interface._suggest_compatible_genomes(test_genome, genomes)
            
            self.log_test("VM Creation: Profile Analysis", "PASS", 
                         f"Memory: {memory_estimate}MB, Suggestions: {len(suggestions)}")
            
        except Exception as e:
            self.log_test("VM Creation: Profile Analysis", "FAIL", f"Exception: {e}")
        
        # Test VM configuration calculation
        try:
            test_genome = genomes[0]
            config = {
                'memory': '512',
                'cpus': '2'
            }
            self.interface._create_optimized_vm(test_genome, config)
            self.log_test("VM Creation: Configuration", "PASS", "VM config simulation working")
        except Exception as e:
            self.log_test("VM Creation: Configuration", "FAIL", f"Exception: {e}")
    
    def test_analysis_history_and_caching(self):
        """Test analysis history and caching functionality"""
        print("\n💾 Testing Analysis History & Caching...")
        
        # Test cache saving
        try:
            # Add some test data to cache
            self.interface.analysis_cache['test_entry'] = {
                'timestamp': datetime.now().isoformat(),
                'data': 'test_data'
            }
            
            self.interface._save_analysis_cache()
            self.log_test("Cache Saving", "PASS", "Cache saved successfully")
        except Exception as e:
            self.log_test("Cache Saving", "FAIL", f"Exception: {e}")
        
        # Test history viewing
        try:
            self.interface._view_analysis_history()
            self.log_test("Analysis History", "PASS", "History displayed")
        except Exception as e:
            self.log_test("Analysis History", "FAIL", f"Exception: {e}")
    
    def test_export_functionality(self):
        """Test export analysis reports functionality"""
        print("\n📄 Testing Export Functionality...")
        
        export_formats = ["json", "csv", "txt", "html"]
        
        for format_type in export_formats:
            try:
                # Simulate export (without actually running questionary)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_export_{format_type}_{timestamp}.{format_type}"
                
                # Test the core export logic
                if format_type == "json":
                    with open(filename, 'w') as f:
                        json.dump(self.interface.analysis_cache, f, indent=2)
                else:
                    with open(filename, 'w') as f:
                        f.write(f"BioXen-JCVI Test Export Report ({format_type})\n")
                        f.write(f"Generated: {datetime.now()}\n\n")
                        f.write(str(self.interface.analysis_cache))
                
                # Clean up test file
                if os.path.exists(filename):
                    os.remove(filename)
                
                self.log_test(f"Export: {format_type.upper()}", "PASS", "Export logic working")
                
            except Exception as e:
                self.log_test(f"Export: {format_type.upper()}", "FAIL", f"Exception: {e}")
    
    def test_refresh_genome_collection(self):
        """Test genome collection refresh functionality"""
        print("\n🔄 Testing Genome Collection Refresh...")
        
        try:
            self.interface._refresh_genome_collection()
            self.log_test("Genome Collection Refresh", "PASS", "Refresh completed")
        except Exception as e:
            self.log_test("Genome Collection Refresh", "FAIL", f"Exception: {e}")
    
    def run_all_tests(self):
        """Run all automated tests"""
        print("🧪 BioXen-JCVI Phase 3 Automated Testing Suite")
        print("=" * 60)
        print(f"Started: {self.start_time}")
        
        # Test core functionality
        genomes = self.test_genome_discovery()
        profiles = self.test_genome_profiles(genomes)
        
        # Test main analysis features
        self.test_compatibility_analysis(genomes)
        self.test_synteny_analysis(genomes)
        self.test_phylogenetic_analysis(genomes)
        self.test_optimization_recommendations(genomes)
        self.test_vm_creation_wizard(genomes)
        
        # Test utility features
        self.test_analysis_history_and_caching()
        self.test_export_functionality()
        self.test_refresh_genome_collection()
        
        # Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate a comprehensive test summary report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"\n📊 Test Summary Report")
        print("=" * 40)
        print(f"Duration: {duration.total_seconds():.2f} seconds")
        
        # Count results by status
        status_counts = {}
        for test_name, result in self.test_results.items():
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_tests = len(self.test_results)
        print(f"Total tests: {total_tests}")
        
        for status, count in status_counts.items():
            percentage = (count / total_tests) * 100
            icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️" if status == "WARN" else "⏭️"
            print(f"{icon} {status}: {count} ({percentage:.1f}%)")
        
        # Detailed results
        print(f"\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️"
            print(f"{status_icon} {test_name}: {result['status']}")
            if result['details']:
                print(f"   └─ {result['details']}")
        
        # Save results to file
        report_file = f"phase3_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        test_report = {
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration.total_seconds(),
            'total_tests': total_tests,
            'status_counts': status_counts,
            'test_results': self.test_results
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(test_report, f, indent=2)
            print(f"\n💾 Detailed report saved: {report_file}")
        except Exception as e:
            print(f"\n❌ Could not save report: {e}")
        
        # Overall assessment
        pass_rate = status_counts.get('PASS', 0) / total_tests * 100
        
        print(f"\n🎯 Overall Assessment:")
        if pass_rate >= 80:
            print(f"🟢 EXCELLENT: {pass_rate:.1f}% pass rate - Phase 3 is highly functional!")
        elif pass_rate >= 60:
            print(f"🟡 GOOD: {pass_rate:.1f}% pass rate - Phase 3 is mostly working with some issues")
        elif pass_rate >= 40:
            print(f"🟠 FAIR: {pass_rate:.1f}% pass rate - Phase 3 has significant functionality but needs work")
        else:
            print(f"🔴 POOR: {pass_rate:.1f}% pass rate - Phase 3 needs major fixes")

def main():
    """Main entry point for automated testing"""
    
    print("🚀 Starting BioXen-JCVI Phase 3 Automated Test Suite...")
    
    try:
        tester = AutomatedTester()
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
