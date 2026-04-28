#!/usr/bin/env python3
"""
Simple runner for Advanced Network Automation
Easy-to-use interface for the complete automation system
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from network_orchestrator import NetworkOrchestrator

def main():
    """Simple main function to run the automation"""
    print("🌐 Advanced Network Automation System")
    print("🚀 Task 2 Network - Complete Automation")
    print("=" * 60)
    
    print("\n🔧 Configuration:")
    print("   • Mode: Simulation (safe for testing)")
    print("   • Network: Task 2 topology")
    print("   • Features: Full automation workflow")
    print("   • Output: Configurations + Reports")
    
    print("\n⏳ Starting automation workflow...")
    
    # Create orchestrator in simulation mode
    orchestrator = NetworkOrchestrator(
        work_dir=".",
        simulation_mode=True  # Safe simulation mode
    )
    
    # Run the complete workflow
    success = orchestrator.run_full_workflow(
        inventory_file=None,  # Use default Task 2 inventory
        deploy=True,          # Simulate deployment
        validate=True,        # Simulate validation
        max_workers=3,        # Parallel processing
        backup_first=True     # Backup configurations
    )
    
    if success:
        print("\n🎉 Automation completed successfully!")
        print("\n📁 Check these directories:")
        print("   • configs/ - Generated configurations")
        print("   • logs/ - Deployment and validation logs")
        print("\n📋 What you got:")
        print("   • Router configurations (R1-R4)")
        print("   • Switch configurations (SW1-SW4)")
        print("   • PC configuration guide")
        print("   • Network inventory files")
        print("   • Deployment reports")
        print("   • Validation reports")
        print("   • Complete workflow documentation")
        
        print("\n🎯 Ready for Packet Tracer!")
        print("   1. Use the generated .txt config files")
        print("   2. Follow the deployment instructions")
        print("   3. Test with validation commands")
        
    else:
        print("\n❌ Automation encountered issues")
        print("   Check the logs/ directory for details")
        
    return success

if __name__ == "__main__":
    success = main()
    input("\n🎉 Press Enter to close...")
    sys.exit(0 if success else 1)

