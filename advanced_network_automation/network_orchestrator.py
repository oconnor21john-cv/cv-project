#!/usr/bin/env python3
"""
Advanced Network Orchestrator
Master controller for complete network automation workflow
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from inventory.network_inventory import NetworkInventory, create_task2_inventory
from config_generator import ConfigurationGenerator
from network_deployer import NetworkDeployer, SimulatedDeployer
from validation.network_validator import NetworkValidator, SimulatedValidator

class NetworkOrchestrator:
    """Master orchestrator for network automation workflow"""
    
    def __init__(self, work_dir: str = ".", simulation_mode: bool = True):
        self.work_dir = Path(work_dir)
        self.simulation_mode = simulation_mode
        
        # Initialize components
        self.inventory = None
        self.config_generator = ConfigurationGenerator(
            template_dir=self.work_dir / "templates",
            output_dir=self.work_dir / "configs"
        )
        
        if simulation_mode:
            self.deployer = SimulatedDeployer(log_dir=str(self.work_dir / "logs"))
            self.validator = SimulatedValidator(log_dir=str(self.work_dir / "logs"))
        else:
            self.deployer = NetworkDeployer(log_dir=str(self.work_dir / "logs"))
            self.validator = NetworkValidator(log_dir=str(self.work_dir / "logs"))
            
        # Workflow results
        self.workflow_results = {
            "start_time": None,
            "end_time": None,
            "phases": {},
            "overall_success": False
        }
        
    def load_inventory(self, inventory_file: Optional[str] = None) -> bool:
        """Load network inventory"""
        print("📋 Loading network inventory...")
        
        try:
            if inventory_file and Path(inventory_file).exists():
                if inventory_file.endswith('.json'):
                    self.inventory = NetworkInventory.from_json(inventory_file)
                elif inventory_file.endswith('.yaml') or inventory_file.endswith('.yml'):
                    self.inventory = NetworkInventory.from_yaml(inventory_file)
                else:
                    raise ValueError("Unsupported inventory file format")
                print(f"   ✅ Loaded inventory from {inventory_file}")
            else:
                # Create default Task 2 inventory
                self.inventory = create_task2_inventory()
                print("   ✅ Created default Task 2 inventory")
                
            # Validate inventory
            errors = self.inventory.validate_inventory()
            if errors:
                print("   ⚠️  Inventory validation warnings:")
                for error in errors:
                    print(f"      - {error}")
            else:
                print("   ✅ Inventory validation passed")
                
            # Save inventory for reference
            self.inventory.to_json(str(self.work_dir / "configs" / "network_inventory.json"))
            self.inventory.to_yaml(str(self.work_dir / "configs" / "network_inventory.yaml"))
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to load inventory: {str(e)}")
            return False
            
    def generate_configurations(self) -> bool:
        """Generate device configurations"""
        print("🔧 Generating device configurations...")
        
        try:
            if not self.inventory:
                raise ValueError("No inventory loaded")
                
            # Generate configurations
            configs = self.config_generator.generate_all_configs(self.inventory)
            
            # Generate PC configurations
            self.config_generator.generate_pc_configs(self.inventory)
            
            # Create deployment summary
            self.config_generator.create_deployment_summary(self.inventory, configs)
            
            self.workflow_results["phases"]["config_generation"] = {
                "success": True,
                "configs_generated": len(configs),
                "message": f"Generated {len(configs)} device configurations"
            }
            
            print(f"   ✅ Generated {len(configs)} device configurations")
            return True
            
        except Exception as e:
            self.workflow_results["phases"]["config_generation"] = {
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ Configuration generation failed: {str(e)}")
            return False
            
    def deploy_configurations(self, max_workers: int = 3, backup_first: bool = True) -> bool:
        """Deploy configurations to devices"""
        print("🚀 Deploying configurations to devices...")
        
        try:
            if not self.inventory:
                raise ValueError("No inventory loaded")
                
            # Load generated configurations
            config_dir = self.work_dir / "configs"
            devices_configs = {}
            
            for device in self.inventory.devices.values():
                if device.device_type in ["router", "switch"]:
                    config_file = config_dir / f"{device.hostname}_config.txt"
                    if config_file.exists():
                        with open(config_file, 'r') as f:
                            config = f.read()
                        devices_configs[device] = config
                    else:
                        print(f"   ⚠️  Configuration file not found for {device.hostname}")
                        
            if not devices_configs:
                raise ValueError("No configurations found to deploy")
                
            # Deploy configurations
            deployment_results = self.deployer.deploy_to_multiple_devices(
                devices_configs, max_workers=max_workers, backup_first=backup_first
            )
            
            # Generate deployment report
            self.deployer.generate_deployment_report(deployment_results)
            
            successful_deployments = sum(1 for result in deployment_results.values() if result["success"])
            total_deployments = len(deployment_results)
            
            self.workflow_results["phases"]["deployment"] = {
                "success": successful_deployments == total_deployments,
                "successful_deployments": successful_deployments,
                "total_deployments": total_deployments,
                "success_rate": (successful_deployments / total_deployments * 100) if total_deployments > 0 else 0,
                "results": deployment_results
            }
            
            if successful_deployments == total_deployments:
                print(f"   ✅ All {total_deployments} deployments successful")
                return True
            else:
                print(f"   ⚠️  {successful_deployments}/{total_deployments} deployments successful")
                return False
                
        except Exception as e:
            self.workflow_results["phases"]["deployment"] = {
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ Deployment failed: {str(e)}")
            return False
            
    def validate_network(self) -> bool:
        """Validate network deployment"""
        print("🔍 Validating network deployment...")
        
        try:
            if not self.inventory:
                raise ValueError("No inventory loaded")
                
            # Run comprehensive validation
            validation_results = self.validator.run_comprehensive_validation(self.inventory)
            
            # Generate validation report
            self.validator.generate_validation_report(validation_results)
            
            overall_score = validation_results.get("overall_score", 0)
            
            self.workflow_results["phases"]["validation"] = {
                "success": overall_score >= 80,  # 80% threshold for success
                "overall_score": overall_score,
                "results": validation_results
            }
            
            if overall_score >= 90:
                print(f"   ✅ Validation passed with excellent score: {overall_score:.1f}%")
                return True
            elif overall_score >= 80:
                print(f"   ✅ Validation passed with good score: {overall_score:.1f}%")
                return True
            elif overall_score >= 60:
                print(f"   ⚠️  Validation passed with acceptable score: {overall_score:.1f}%")
                return True
            else:
                print(f"   ❌ Validation failed with low score: {overall_score:.1f}%")
                return False
                
        except Exception as e:
            self.workflow_results["phases"]["validation"] = {
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ Validation failed: {str(e)}")
            return False
            
    def run_full_workflow(self, inventory_file: Optional[str] = None,
                         deploy: bool = True, validate: bool = True,
                         max_workers: int = 3, backup_first: bool = True) -> bool:
        """Run the complete network automation workflow"""
        print("🌐 Starting Advanced Network Automation Workflow")
        print("=" * 60)
        
        self.workflow_results["start_time"] = datetime.now()
        
        # Phase 1: Load Inventory
        print("\n📋 PHASE 1: INVENTORY MANAGEMENT")
        if not self.load_inventory(inventory_file):
            return False
            
        # Phase 2: Generate Configurations
        print("\n🔧 PHASE 2: CONFIGURATION GENERATION")
        if not self.generate_configurations():
            return False
            
        # Phase 3: Deploy Configurations (optional)
        if deploy:
            print("\n🚀 PHASE 3: CONFIGURATION DEPLOYMENT")
            deployment_success = self.deploy_configurations(max_workers, backup_first)
            if not deployment_success and not self.simulation_mode:
                print("   ⚠️  Deployment issues detected. Continuing with validation...")
        else:
            print("\n⏭️  PHASE 3: DEPLOYMENT SKIPPED")
            self.workflow_results["phases"]["deployment"] = {"success": True, "skipped": True}
            
        # Phase 4: Validate Network (optional)
        if validate:
            print("\n🔍 PHASE 4: NETWORK VALIDATION")
            validation_success = self.validate_network()
        else:
            print("\n⏭️  PHASE 4: VALIDATION SKIPPED")
            self.workflow_results["phases"]["validation"] = {"success": True, "skipped": True}
            validation_success = True
            
        # Complete workflow
        self.workflow_results["end_time"] = datetime.now()
        
        # Determine overall success
        all_phases_successful = all(
            phase.get("success", False) for phase in self.workflow_results["phases"].values()
        )
        
        self.workflow_results["overall_success"] = all_phases_successful
        
        # Generate final report
        self.generate_workflow_report()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 WORKFLOW SUMMARY")
        print("=" * 60)
        
        duration = self.workflow_results["end_time"] - self.workflow_results["start_time"]
        
        if all_phases_successful:
            print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        else:
            print("⚠️  WORKFLOW COMPLETED WITH ISSUES")
            
        print(f"⏱️  Total Duration: {duration}")
        print(f"📊 Phases Completed: {len(self.workflow_results['phases'])}")
        
        for phase_name, phase_result in self.workflow_results["phases"].items():
            status = "✅" if phase_result.get("success", False) else "❌"
            if phase_result.get("skipped", False):
                status = "⏭️ "
            print(f"   {status} {phase_name.replace('_', ' ').title()}")
            
        print(f"\n📁 Output Files: {self.work_dir / 'configs'}")
        print(f"📁 Log Files: {self.work_dir / 'logs'}")
        
        return all_phases_successful
        
    def generate_workflow_report(self) -> str:
        """Generate comprehensive workflow report"""
        report = f"""# Network Automation Workflow Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Workflow Summary
- **Start Time:** {self.workflow_results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **End Time:** {self.workflow_results['end_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **Duration:** {str(self.workflow_results['end_time'] - self.workflow_results['start_time'])}
- **Overall Success:** {'✅ YES' if self.workflow_results['overall_success'] else '❌ NO'}
- **Simulation Mode:** {'✅ YES' if self.simulation_mode else '❌ NO'}

## Phase Results
"""
        
        for phase_name, phase_result in self.workflow_results["phases"].items():
            status = "✅ SUCCESS" if phase_result.get("success", False) else "❌ FAILED"
            if phase_result.get("skipped", False):
                status = "⏭️  SKIPPED"
                
            report += f"### {phase_name.replace('_', ' ').title()}\n"
            report += f"- **Status:** {status}\n"
            
            if "message" in phase_result:
                report += f"- **Message:** {phase_result['message']}\n"
            if "error" in phase_result:
                report += f"- **Error:** {phase_result['error']}\n"
            if "configs_generated" in phase_result:
                report += f"- **Configurations Generated:** {phase_result['configs_generated']}\n"
            if "successful_deployments" in phase_result:
                report += f"- **Successful Deployments:** {phase_result['successful_deployments']}/{phase_result['total_deployments']}\n"
                report += f"- **Success Rate:** {phase_result['success_rate']:.1f}%\n"
            if "overall_score" in phase_result:
                report += f"- **Validation Score:** {phase_result['overall_score']:.1f}%\n"
                
            report += "\n"
            
        if self.inventory:
            report += f"""## Network Inventory Summary
- **Total Devices:** {len(self.inventory.devices)}
- **Routers:** {len(self.inventory.get_routers())}
- **Switches:** {len(self.inventory.get_switches())}
- **PCs:** {len(self.inventory.get_pcs())}
- **VLANs:** {len(self.inventory.vlans)}
- **Physical Connections:** {len(self.inventory.connections)}

"""
        
        report += f"""## Files Generated
- Configuration files: `configs/`
- Inventory files: `configs/network_inventory.json`, `configs/network_inventory.yaml`
- Deployment logs: `logs/`
- Validation reports: `logs/`

## Next Steps
"""
        
        if self.workflow_results["overall_success"]:
            report += """- ✅ Workflow completed successfully
- Monitor network performance
- Schedule regular validation runs
- Update documentation as needed
"""
        else:
            report += """- ❌ Review failed phases and resolve issues
- Check error logs for detailed information
- Re-run workflow after fixes
- Consider manual intervention if needed
"""
        
        report += f"""
---
*Report generated by Advanced Network Orchestrator*
*Simulation Mode: {'Enabled' if self.simulation_mode else 'Disabled'}*
"""
        
        # Save report
        report_filename = self.work_dir / "logs" / f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_filename.parent.mkdir(exist_ok=True)
        with open(report_filename, 'w') as f:
            f.write(report)
            
        # Save workflow results as JSON
        json_filename = self.work_dir / "logs" / f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w') as f:
            # Convert datetime objects to strings for JSON serialization
            results_copy = self.workflow_results.copy()
            results_copy["start_time"] = results_copy["start_time"].isoformat()
            results_copy["end_time"] = results_copy["end_time"].isoformat()
            json.dump(results_copy, f, indent=2)
            
        return report

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Advanced Network Automation Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full workflow in simulation mode
  python network_orchestrator.py --simulate
  
  # Run with custom inventory file
  python network_orchestrator.py --inventory my_network.yaml
  
  # Generate configs only (no deployment/validation)
  python network_orchestrator.py --no-deploy --no-validate
  
  # Real deployment mode (requires actual devices)
  python network_orchestrator.py --no-simulate --deploy
        """
    )
    
    parser.add_argument(
        "--inventory", "-i",
        help="Path to network inventory file (JSON or YAML)"
    )
    
    parser.add_argument(
        "--work-dir", "-w",
        default=".",
        help="Working directory for output files (default: current directory)"
    )
    
    parser.add_argument(
        "--simulate", "-s",
        action="store_true",
        default=True,
        help="Run in simulation mode (default: True)"
    )
    
    parser.add_argument(
        "--no-simulate",
        action="store_false",
        dest="simulate",
        help="Disable simulation mode (use real devices)"
    )
    
    parser.add_argument(
        "--deploy", "-d",
        action="store_true",
        default=True,
        help="Deploy configurations to devices (default: True)"
    )
    
    parser.add_argument(
        "--no-deploy",
        action="store_false",
        dest="deploy",
        help="Skip configuration deployment"
    )
    
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        default=True,
        help="Validate network after deployment (default: True)"
    )
    
    parser.add_argument(
        "--no-validate",
        action="store_false",
        dest="validate",
        help="Skip network validation"
    )
    
    parser.add_argument(
        "--max-workers",
        type=int,
        default=3,
        help="Maximum number of parallel deployment workers (default: 3)"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_false",
        dest="backup_first",
        help="Skip configuration backup before deployment"
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = NetworkOrchestrator(
        work_dir=args.work_dir,
        simulation_mode=args.simulate
    )
    
    # Run workflow
    success = orchestrator.run_full_workflow(
        inventory_file=args.inventory,
        deploy=args.deploy,
        validate=args.validate,
        max_workers=args.max_workers,
        backup_first=args.backup_first
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

