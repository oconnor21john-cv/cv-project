#!/usr/bin/env python3
"""
Advanced Network Validation System
Validates network deployment and connectivity
"""

import os
import time
import json
import logging
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from netmiko import ConnectHandler
    NETMIKO_AVAILABLE = True
except ImportError:
    NETMIKO_AVAILABLE = False

from ..inventory.network_inventory import NetworkInventory, NetworkDevice

class NetworkValidator:
    """Advanced network validation and testing"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Validation results
        self.validation_results = {
            "connectivity_tests": {},
            "ospf_tests": {},
            "vlan_tests": {},
            "routing_tests": {},
            "interface_tests": {},
            "overall_score": 0
        }
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_filename = self.log_dir / f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def ping_test(self, source_ip: str, target_ip: str, count: int = 4) -> Tuple[bool, Dict]:
        """Perform ping test between two IPs"""
        try:
            # Use system ping command
            if os.name == 'nt':  # Windows
                cmd = ['ping', '-n', str(count), target_ip]
            else:  # Unix/Linux
                cmd = ['ping', '-c', str(count), target_ip]
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            
            # Parse ping statistics
            output = result.stdout
            stats = {
                "packets_sent": count,
                "packets_received": 0,
                "packet_loss": 100,
                "avg_rtt": 0
            }
            
            if success:
                # Basic parsing for packet loss
                if "0% packet loss" in output or "0% loss" in output:
                    stats["packets_received"] = count
                    stats["packet_loss"] = 0
                    
            return success, stats
            
        except Exception as e:
            self.logger.error(f"Ping test failed: {str(e)}")
            return False, {"error": str(e)}
            
    def validate_device_connectivity(self, device: NetworkDevice) -> Dict[str, Any]:
        """Validate basic device connectivity"""
        result = {
            "device": device.hostname,
            "reachable": False,
            "response_time": 0,
            "interfaces_up": 0,
            "total_interfaces": len(device.interfaces),
            "details": {}
        }
        
        try:
            if not NETMIKO_AVAILABLE:
                # Fallback to ping test
                start_time = time.time()
                ping_success, ping_stats = self.ping_test("localhost", device.mgmt_ip)
                result["response_time"] = time.time() - start_time
                result["reachable"] = ping_success
                result["details"]["ping_stats"] = ping_stats
                return result
                
            # Use Netmiko for detailed validation
            connection_params = {
                "device_type": "cisco_ios",
                "host": device.mgmt_ip,
                "username": device.credentials.get("username", "admin"),
                "password": device.credentials.get("password", "cisco"),
                "secret": device.credentials.get("secret", "cisco"),
                "timeout": 15
            }
            
            start_time = time.time()
            with ConnectHandler(**connection_params) as conn:
                result["response_time"] = time.time() - start_time
                result["reachable"] = True
                
                # Check interface status
                interface_output = conn.send_command("show ip interface brief")
                result["details"]["interface_output"] = interface_output
                
                # Count up interfaces
                lines = interface_output.split('\n')
                for line in lines:
                    if 'up' in line.lower() and 'up' in line.lower().split()[-1]:
                        result["interfaces_up"] += 1
                        
        except Exception as e:
            result["details"]["error"] = str(e)
            self.logger.error(f"Connectivity validation failed for {device.hostname}: {str(e)}")
            
        return result
        
    def validate_ospf_neighbors(self, device: NetworkDevice) -> Dict[str, Any]:
        """Validate OSPF neighbor relationships"""
        result = {
            "device": device.hostname,
            "ospf_enabled": False,
            "neighbors_expected": 0,
            "neighbors_found": 0,
            "neighbors_full": 0,
            "neighbor_details": [],
            "routing_table_entries": 0
        }
        
        if device.device_type != "router":
            return result
            
        try:
            if not NETMIKO_AVAILABLE:
                result["error"] = "Netmiko not available for OSPF validation"
                return result
                
            connection_params = {
                "device_type": "cisco_ios",
                "host": device.mgmt_ip,
                "username": device.credentials.get("username", "admin"),
                "password": device.credentials.get("password", "cisco"),
                "secret": device.credentials.get("secret", "cisco"),
                "timeout": 15
            }
            
            with ConnectHandler(**connection_params) as conn:
                # Check OSPF neighbors
                ospf_output = conn.send_command("show ip ospf neighbor")
                result["ospf_enabled"] = "Neighbor ID" in ospf_output
                
                if result["ospf_enabled"]:
                    lines = ospf_output.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('Neighbor'):
                            parts = line.split()
                            if len(parts) >= 6:
                                neighbor_info = {
                                    "neighbor_id": parts[0],
                                    "priority": parts[1],
                                    "state": parts[2],
                                    "dead_time": parts[3],
                                    "address": parts[4],
                                    "interface": parts[5]
                                }
                                result["neighbor_details"].append(neighbor_info)
                                result["neighbors_found"] += 1
                                
                                if neighbor_info["state"] == "FULL":
                                    result["neighbors_full"] += 1
                                    
                # Check routing table
                route_output = conn.send_command("show ip route")
                result["routing_table_entries"] = route_output.count('O ')  # OSPF routes
                
                # Expected neighbors for Task 2 topology
                neighbor_expectations = {
                    "R1": 2,  # R2, R3
                    "R2": 2,  # R1, R4
                    "R3": 2,  # R1, R4
                    "R4": 2   # R2, R3
                }
                result["neighbors_expected"] = neighbor_expectations.get(device.hostname, 0)
                
        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"OSPF validation failed for {device.hostname}: {str(e)}")
            
        return result
        
    def validate_vlan_configuration(self, device: NetworkDevice) -> Dict[str, Any]:
        """Validate VLAN configuration on switches"""
        result = {
            "device": device.hostname,
            "vlans_configured": 0,
            "vlans_expected": 5,  # 10, 20, 30, 40, 99
            "vlan_details": [],
            "trunk_ports": 0,
            "access_ports": 0
        }
        
        if device.device_type != "switch":
            return result
            
        try:
            if not NETMIKO_AVAILABLE:
                result["error"] = "Netmiko not available for VLAN validation"
                return result
                
            connection_params = {
                "device_type": "cisco_ios",
                "host": device.mgmt_ip,
                "username": device.credentials.get("username", "admin"),
                "password": device.credentials.get("password", "cisco"),
                "secret": device.credentials.get("secret", "cisco"),
                "timeout": 15
            }
            
            with ConnectHandler(**connection_params) as conn:
                # Check VLAN configuration
                vlan_output = conn.send_command("show vlan brief")
                lines = vlan_output.split('\n')
                
                for line in lines:
                    if line.strip() and line[0].isdigit():
                        parts = line.split()
                        if len(parts) >= 3:
                            vlan_info = {
                                "vlan_id": parts[0],
                                "name": parts[1],
                                "status": parts[2],
                                "ports": parts[3:] if len(parts) > 3 else []
                            }
                            result["vlan_details"].append(vlan_info)
                            result["vlans_configured"] += 1
                            
                # Check trunk configuration
                trunk_output = conn.send_command("show interface trunk")
                result["trunk_ports"] = trunk_output.count('trunking')
                
                # Count access ports (approximate)
                interface_output = conn.send_command("show interface status")
                result["access_ports"] = interface_output.count('connected') - result["trunk_ports"]
                
        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"VLAN validation failed for {device.hostname}: {str(e)}")
            
        return result
        
    def validate_inter_vlan_routing(self, inventory: NetworkInventory) -> Dict[str, Any]:
        """Validate inter-VLAN routing functionality"""
        result = {
            "test_name": "Inter-VLAN Routing",
            "tests_performed": 0,
            "tests_passed": 0,
            "test_details": []
        }
        
        # Define test cases for inter-VLAN connectivity
        test_cases = [
            {"source": "192.168.10.100", "target": "192.168.20.100", "description": "Sales to Marketing"},
            {"source": "192.168.10.100", "target": "192.168.30.100", "description": "Sales to IT"},
            {"source": "192.168.20.100", "target": "192.168.40.100", "description": "Marketing to Finance"},
            {"source": "192.168.30.100", "target": "192.168.40.100", "description": "IT to Finance"}
        ]
        
        for test_case in test_cases:
            result["tests_performed"] += 1
            
            # Perform ping test
            success, stats = self.ping_test(test_case["source"], test_case["target"])
            
            test_detail = {
                "description": test_case["description"],
                "source": test_case["source"],
                "target": test_case["target"],
                "success": success,
                "stats": stats
            }
            
            result["test_details"].append(test_detail)
            
            if success:
                result["tests_passed"] += 1
                
        return result
        
    def validate_network_topology(self, inventory: NetworkInventory) -> Dict[str, Any]:
        """Validate overall network topology"""
        result = {
            "topology_name": "Task 2 Network",
            "expected_devices": 12,  # 4 routers + 4 switches + 4 PCs (we're testing 4 PCs)
            "reachable_devices": 0,
            "device_summary": {},
            "connectivity_matrix": {}
        }
        
        # Test connectivity to all devices
        for device in inventory.devices.values():
            if device.device_type in ["router", "switch"]:  # Skip PCs for now
                connectivity_result = self.validate_device_connectivity(device)
                result["device_summary"][device.hostname] = connectivity_result
                
                if connectivity_result["reachable"]:
                    result["reachable_devices"] += 1
                    
        return result
        
    def run_comprehensive_validation(self, inventory: NetworkInventory) -> Dict[str, Any]:
        """Run comprehensive network validation"""
        self.logger.info("Starting comprehensive network validation...")
        
        validation_start = datetime.now()
        
        # 1. Device connectivity validation
        print("🔍 Validating device connectivity...")
        connectivity_results = {}
        for device in inventory.devices.values():
            if device.device_type in ["router", "switch"]:
                result = self.validate_device_connectivity(device)
                connectivity_results[device.hostname] = result
                status = "✅" if result["reachable"] else "❌"
                print(f"   {status} {device.hostname}: {'Reachable' if result['reachable'] else 'Unreachable'}")
                
        self.validation_results["connectivity_tests"] = connectivity_results
        
        # 2. OSPF validation
        print("🔍 Validating OSPF configuration...")
        ospf_results = {}
        for device in inventory.get_routers():
            result = self.validate_ospf_neighbors(device)
            ospf_results[device.hostname] = result
            status = "✅" if result["neighbors_full"] == result["neighbors_expected"] else "❌"
            print(f"   {status} {device.hostname}: {result['neighbors_full']}/{result['neighbors_expected']} neighbors")
            
        self.validation_results["ospf_tests"] = ospf_results
        
        # 3. VLAN validation
        print("🔍 Validating VLAN configuration...")
        vlan_results = {}
        for device in inventory.get_switches():
            result = self.validate_vlan_configuration(device)
            vlan_results[device.hostname] = result
            status = "✅" if result["vlans_configured"] >= result["vlans_expected"] else "❌"
            print(f"   {status} {device.hostname}: {result['vlans_configured']}/{result['vlans_expected']} VLANs")
            
        self.validation_results["vlan_tests"] = vlan_results
        
        # 4. Inter-VLAN routing validation
        print("🔍 Validating inter-VLAN routing...")
        routing_result = self.validate_inter_vlan_routing(inventory)
        self.validation_results["routing_tests"] = routing_result
        status = "✅" if routing_result["tests_passed"] == routing_result["tests_performed"] else "❌"
        print(f"   {status} Inter-VLAN routing: {routing_result['tests_passed']}/{routing_result['tests_performed']} tests passed")
        
        # 5. Overall topology validation
        print("🔍 Validating network topology...")
        topology_result = self.validate_network_topology(inventory)
        self.validation_results["topology_tests"] = topology_result
        
        # Calculate overall score
        total_tests = 0
        passed_tests = 0
        
        # Count connectivity tests
        for result in connectivity_results.values():
            total_tests += 1
            if result["reachable"]:
                passed_tests += 1
                
        # Count OSPF tests
        for result in ospf_results.values():
            total_tests += 1
            if result["neighbors_full"] == result["neighbors_expected"]:
                passed_tests += 1
                
        # Count VLAN tests
        for result in vlan_results.values():
            total_tests += 1
            if result["vlans_configured"] >= result["vlans_expected"]:
                passed_tests += 1
                
        # Count routing tests
        total_tests += routing_result["tests_performed"]
        passed_tests += routing_result["tests_passed"]
        
        self.validation_results["overall_score"] = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        validation_end = datetime.now()
        self.validation_results["validation_duration"] = str(validation_end - validation_start)
        self.validation_results["validation_timestamp"] = validation_end.isoformat()
        
        print(f"\n🎯 Validation complete! Overall score: {self.validation_results['overall_score']:.1f}%")
        
        return self.validation_results
        
    def generate_validation_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive validation report"""
        report = f"""# Network Validation Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Overall Score:** {results.get('overall_score', 0):.1f}%
- **Validation Duration:** {results.get('validation_duration', 'Unknown')}
- **Network Status:** {'✅ HEALTHY' if results.get('overall_score', 0) >= 90 else '⚠️ NEEDS ATTENTION' if results.get('overall_score', 0) >= 70 else '❌ CRITICAL ISSUES'}

## Device Connectivity Results
"""
        
        connectivity_tests = results.get("connectivity_tests", {})
        for device, result in connectivity_tests.items():
            status = "✅ PASS" if result["reachable"] else "❌ FAIL"
            report += f"- **{device}:** {status} (Response time: {result['response_time']:.2f}s)\n"
            
        report += f"""
## OSPF Neighbor Validation
"""
        
        ospf_tests = results.get("ospf_tests", {})
        for device, result in ospf_tests.items():
            status = "✅ PASS" if result["neighbors_full"] == result["neighbors_expected"] else "❌ FAIL"
            report += f"- **{device}:** {status} ({result['neighbors_full']}/{result['neighbors_expected']} neighbors in FULL state)\n"
            
        report += f"""
## VLAN Configuration Validation
"""
        
        vlan_tests = results.get("vlan_tests", {})
        for device, result in vlan_tests.items():
            status = "✅ PASS" if result["vlans_configured"] >= result["vlans_expected"] else "❌ FAIL"
            report += f"- **{device}:** {status} ({result['vlans_configured']}/{result['vlans_expected']} VLANs configured)\n"
            
        report += f"""
## Inter-VLAN Routing Tests
"""
        
        routing_tests = results.get("routing_tests", {})
        if routing_tests:
            for test in routing_tests.get("test_details", []):
                status = "✅ PASS" if test["success"] else "❌ FAIL"
                report += f"- **{test['description']}:** {status} ({test['source']} → {test['target']})\n"
                
        report += f"""
## Recommendations
"""
        
        if results.get('overall_score', 0) >= 90:
            report += "- ✅ Network is operating optimally\n- Continue regular monitoring and maintenance\n"
        elif results.get('overall_score', 0) >= 70:
            report += "- ⚠️ Some issues detected that require attention\n- Review failed tests and resolve issues\n- Re-run validation after fixes\n"
        else:
            report += "- ❌ Critical issues detected\n- Immediate attention required\n- Review all failed tests\n- Consider rollback if necessary\n"
            
        report += f"""
## Next Steps
1. Address any failed validation tests
2. Verify physical connectivity for unreachable devices
3. Check OSPF configuration for neighbor issues
4. Validate VLAN assignments and trunk configurations
5. Test end-to-end connectivity manually if needed
6. Schedule regular validation runs

---
*Report generated by Advanced Network Validation System*
"""
        
        # Save report
        report_filename = self.log_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_filename, 'w') as f:
            f.write(report)
            
        # Save results as JSON
        json_filename = self.log_dir / f"validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w') as f:
            json.dump(results, f, indent=2)
            
        return report

class SimulatedValidator(NetworkValidator):
    """Simulated validator for testing without real devices"""
    
    def __init__(self, log_dir: str = "logs"):
        super().__init__(log_dir)
        self.logger.info("Using simulated validation mode")
        
    def validate_device_connectivity(self, device: NetworkDevice) -> Dict[str, Any]:
        """Simulate device connectivity validation"""
        time.sleep(0.5)  # Simulate test time
        
        return {
            "device": device.hostname,
            "reachable": True,
            "response_time": 0.5,
            "interfaces_up": len(device.interfaces),
            "total_interfaces": len(device.interfaces),
            "details": {"simulated": True}
        }
        
    def validate_ospf_neighbors(self, device: NetworkDevice) -> Dict[str, Any]:
        """Simulate OSPF validation"""
        time.sleep(1)  # Simulate test time
        
        neighbor_expectations = {
            "R1": 2, "R2": 2, "R3": 2, "R4": 2
        }
        
        expected = neighbor_expectations.get(device.hostname, 0)
        
        return {
            "device": device.hostname,
            "ospf_enabled": True,
            "neighbors_expected": expected,
            "neighbors_found": expected,
            "neighbors_full": expected,
            "neighbor_details": [{"simulated": True}] * expected,
            "routing_table_entries": 8
        }
        
    def validate_vlan_configuration(self, device: NetworkDevice) -> Dict[str, Any]:
        """Simulate VLAN validation"""
        time.sleep(0.8)  # Simulate test time
        
        return {
            "device": device.hostname,
            "vlans_configured": 5,
            "vlans_expected": 5,
            "vlan_details": [{"simulated": True}] * 5,
            "trunk_ports": 1,
            "access_ports": 4
        }
        
    def ping_test(self, source_ip: str, target_ip: str, count: int = 4) -> Tuple[bool, Dict]:
        """Simulate ping test"""
        time.sleep(0.3)  # Simulate ping time
        
        return True, {
            "packets_sent": count,
            "packets_received": count,
            "packet_loss": 0,
            "avg_rtt": 2.5
        }

def main():
    """Main function for testing validation"""
    from ..inventory.network_inventory import create_task2_inventory
    
    print("🔍 Advanced Network Validation System")
    print("=" * 50)
    
    # Create inventory
    print("📋 Loading network inventory...")
    inventory = create_task2_inventory()
    
    # Create validator (simulated for testing)
    print("🔍 Initializing validation engine...")
    validator = SimulatedValidator()
    
    # Run comprehensive validation
    print("🚀 Running comprehensive validation...")
    results = validator.run_comprehensive_validation(inventory)
    
    # Generate report
    print("📊 Generating validation report...")
    report = validator.generate_validation_report(results)
    
    print(f"\n🎉 Validation complete!")
    print(f"📊 Overall Score: {results['overall_score']:.1f}%")
    print(f"📁 Reports: {validator.log_dir}")
    
if __name__ == "__main__":
    main()

