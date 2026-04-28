
# Enhanced Task 2 Network - Packet Tracer Setup Instructions
Generated on 2025-10-24 15:32:15

## IMPORTANT: ISP Devices Excluded
This configuration excludes the following devices as requested:
- Local ISP R1, R2, R3, R4
- ISP S1, S2, S3, S4 (3650 models in middle)
- ISP Remote devices
- 4331 ISP Remote (ping 9.9.9.9)

## Step 1: Add Devices to Workspace

### Routers (13 total):
- 1 x Cisco 4331 Router (R2) - **Requires interface modules**
- 12 x Cisco 2901 Routers (R1, R3-R8, R11-R16)

### Switches (16 total):
- 16 x Cisco 2960 Switches (SW1-SW8, SW11-SW16)

### Servers (13 total):
- 13 x Generic Servers (S1-S8, S11-S16, excluding ISP servers)

## Step 2: R2 (4331) Interface Module Setup
**CRITICAL**: R2 needs additional interfaces to connect to 4 routers

1. Power off R2
2. Add interface module: **EHWIC-4ESG** (4-port Gigabit Ethernet)
3. Power on R2
4. Verify interfaces: G0/0/0, G0/0/1, G0/1/0, G0/1/1, G0/1/2, G0/1/3

## Step 3: Physical Connections

### Upper Section Router-to-Router Links:
- R1 G0/0 <-> R2 G0/0/0
- R2 G0/0/1 <-> R3 G0/0  
- R2 G0/1/0 <-> R4 G0/0
- R2 G0/1/1 <-> R5 G0/0
- R3 G0/1 <-> R6 G0/0
- R6 G0/1 <-> R7 G0/0
- R7 G0/1 <-> R8 G0/0

### Lower Section Router-to-Router Links:
- R11 G0/0 <-> R12 G0/0
- R12 G0/1 <-> R13 G0/0
- R13 G0/1 <-> R14 G0/0
- R14 G0/1 <-> R15 G0/0
- R15 G0/1 <-> R16 G0/0

### Router-to-Switch Links:
- R1 G0/1 <-> SW1 G0/1
- R2 G0/1/2 <-> SW2 G0/1
- R3 G0/2 <-> SW3 G0/1
- R4 G0/1 <-> SW4 G0/1
- R5 G0/1 <-> SW5 G0/1
- R6 G0/2 <-> SW6 G0/1
- R7 G0/2 <-> SW7 G0/1
- R8 G0/1 <-> SW8 G0/1
- R11 G0/1 <-> SW11 G0/1
- R12 G0/2 <-> SW12 G0/1
- R13 G0/2 <-> SW13 G0/1
- R14 G0/2 <-> SW14 G0/1
- R15 G0/2 <-> SW15 G0/1
- R16 G0/1 <-> SW16 G0/1

### Switch-to-Server Links:
- Each switch F0/1 <-> Corresponding server (S1-S8, S11-S16)

## Step 4: Configure Devices
Copy configurations from generated files to device CLI:

### Routers:
- R1_config.txt -> R1 CLI
- R2_config.txt -> R2 CLI (4331 with modules)
- R3_config.txt -> R3 CLI
- ... (continue for all routers)

### Switches:
- SW1_config.txt -> SW1 CLI
- SW2_config.txt -> SW2 CLI
- ... (continue for all switches)

### Servers:
Configure IP addresses from Server_configs.txt

## Step 5: Network Areas
- **Area 0**: Upper section (R1-R8) - Main backbone
- **Area 1**: Lower section (R11-R16) - Branch networks

## Step 6: DHCP Configuration
Each router provides DHCP for its local VLAN:
- R1: 192.168.1.0/24 (VLAN 1)
- R2: 192.168.2.0/24 (VLAN 2)
- ... (continue for all VLANs)

## Step 7: Verification Commands

### On Routers:
- show ip route ospf
- show ip ospf neighbor
- show ip dhcp binding
- show ip interface brief

### On Switches:
- show vlan brief
- show interface trunk
- show spanning-tree

### On Servers:
- ipconfig
- ping [gateway]
- ping [remote_server]

## Step 8: Testing Scenarios
1. **DHCP Testing**: Connect PCs to access ports, verify DHCP assignment
2. **Inter-VLAN Routing**: Test communication between different VLANs
3. **OSPF Convergence**: Shut down links, verify route recalculation
4. **Area Communication**: Test Area 0 <-> Area 1 communication

## Expected Results
- All OSPF neighbors in FULL state
- DHCP clients receive IP addresses automatically
- Inter-VLAN communication works
- Network has redundant paths
- **Note**: No internet connectivity (ISP devices excluded)

## Troubleshooting Tips
1. **R2 Interface Issues**: Ensure EHWIC-4ESG module is properly installed
2. **OSPF Problems**: Check area assignments and network statements
3. **DHCP Issues**: Verify ip helper-address on VLAN interfaces
4. **VLAN Problems**: Check trunk configurations and VLAN assignments

## Network Topology Summary
- **13 Routers**: 1x 4331, 12x 2901
- **16 Switches**: All 2960 models
- **13 Servers**: Excluding ISP servers as requested
- **2 OSPF Areas**: Area 0 (upper), Area 1 (lower)
- **16 VLANs**: Each with DHCP service
