
# Enhanced Task 2 Network v2 - Packet Tracer Setup Instructions
Generated on 2025-10-25 16:18:47

## IMPORTANT: WAN vs LAN Links
This configuration properly distinguishes between:
- **LAN Links** (straight lines): Use Ethernet interfaces and Copper Straight-Through cables
- **WAN Links** (red zigzag lines): Use Serial interfaces and Serial DCE cables

## ISP Devices Excluded
This configuration excludes the following devices as requested:
- Local ISP R1, R2, R3, R4
- ISP S1, S2, S3, S4 (3650 models in middle)
- ISP Remote devices
- 4331 ISP Remote (ping 9.9.9.9)

## Step 1: Add Devices to Workspace

### Routers (14 total):
- 1 x Cisco 4331 Router (R2) - **Requires interface modules**
- 13 x Cisco 2901 Routers (R1, R3-R8, R11-R16)

### Switches (14 total):
- 14 x Cisco 2960 Switches (SW1-SW8, SW11-SW16)

### Servers (13 total):
- 13 x Generic Servers (S1-S8, S11-S16, excluding ISP servers)

## Step 2: R2 (4331) Interface Module Setup
**CRITICAL**: R2 needs additional interfaces

1. Power off R2
2. Add interface module: **EHWIC-4ESG** (4-port Gigabit Ethernet)
3. Power on R2
4. Verify interfaces: G0/0/0, G0/0/1, G0/1/0, G0/1/1, S0/0/0

## Step 3: Physical Connections

### **LAN Links** (Copper Straight-Through Cables):

#### Upper Section Router-to-Router Links:
- R1 G0/0 <-> R2 G0/0/0
- R2 G0/0/1 <-> R3 G0/0  
- R2 G0/1/0 <-> R4 G0/0
- R3 G0/1 <-> R6 G0/0
- R6 G0/1 <-> R7 G0/0
- R7 G0/1 <-> R8 G0/0

#### Lower Section Router-to-Router Links:
- R11 G0/0 <-> R12 G0/0
- R12 G0/1 <-> R13 G0/0
- R13 G0/1 <-> R14 G0/0
- R14 G0/1 <-> R15 G0/0
- R15 G0/1 <-> R16 G0/0

### **WAN Links** (Serial DCE Cables):

#### Critical WAN Connection:
- **R2 S0/0/0 <-> R5 S0/0/0** (RED ZIGZAG LINE)
  - Use **Serial DCE cable**
  - R2 side = **DCE** (provides clock rate)
  - R5 side = **DTE**

### Router-to-Switch Links (Ethernet):
- R1 G0/1 <-> SW1 G0/1
- R2 G0/1/1 <-> SW2 G0/1
- R3 G0/2 <-> SW3 G0/1
- R4 G0/1 <-> SW4 G0/1
- R5 G0/0 <-> SW5 G0/1
- R6 G0/2 <-> SW6 G0/1
- R7 G0/2 <-> SW7 G0/1
- R8 G0/1 <-> SW8 G0/1
- R11 G0/1 <-> SW11 G0/1
- R12 G0/2 <-> SW12 G0/1
- R13 G0/2 <-> SW13 G0/1
- R14 G0/2 <-> SW14 G0/1
- R15 G0/2 <-> SW15 G0/1
- R16 G0/1 <-> SW16 G0/1

### Switch-to-Server Links (Ethernet):
- Each switch F0/1 <-> Corresponding server (S1-S8, S11-S16)

## Step 4: Configure Devices
Copy configurations from generated files to device CLI:

### Routers:
- R1_config.txt -> R1 CLI
- R2_config.txt -> R2 CLI (4331 with modules + Serial interface)
- R3_config.txt -> R3 CLI
- R5_config.txt -> R5 CLI (includes Serial interface)
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

## Step 7: WAN Link Verification
**Critical**: Verify the R2-R5 WAN link:

### On R2:
- show interface serial0/0/0
- show controllers serial0/0/0 (should show DCE)

### On R5:
- show interface serial0/0/0
- show controllers serial0/0/0 (should show DTE)

### Test WAN connectivity:
- ping 10.2.25.2 (from R2 to R5)
- ping 10.2.25.1 (from R5 to R2)

## Step 8: Verification Commands

### On Routers:
- show ip route ospf
- show ip ospf neighbor
- show ip dhcp binding
- show ip interface brief
- show interface serial0/0/0 (for WAN links)

### On Switches:
- show vlan brief
- show interface trunk
- show spanning-tree

### On Servers:
- ipconfig
- ping [gateway]
- ping [remote_server]

## Step 9: Testing Scenarios
1. **DHCP Testing**: Connect PCs to access ports, verify DHCP assignment
2. **Inter-VLAN Routing**: Test communication between different VLANs
3. **OSPF Convergence**: Shut down links, verify route recalculation
4. **WAN Link Testing**: Test R2-R5 WAN connectivity specifically
5. **Area Communication**: Test Area 0 <-> Area 1 communication

## Expected Results
- All OSPF neighbors in FULL state
- DHCP clients receive IP addresses automatically
- Inter-VLAN communication works
- **WAN link R2-R5 shows "up/up" status**
- Network has redundant paths
- **Note**: No internet connectivity (ISP devices excluded)

## Troubleshooting Tips
1. **R2 Interface Issues**: Ensure EHWIC-4ESG module is properly installed
2. **WAN Link Problems**: 
   - Verify Serial DCE cable is used
   - Check clock rate on DCE side (R2)
   - Verify encapsulation ppp on both ends
3. **OSPF Problems**: Check area assignments and network statements
4. **DHCP Issues**: Verify ip helper-address on VLAN interfaces
5. **VLAN Problems**: Check trunk configurations and VLAN assignments

## Key Differences from v1:
- **R2-R5 connection**: Now properly configured as Serial/WAN link
- **Cable types**: Distinguishes between Ethernet and Serial cables
- **Interface types**: Uses Serial0/0/0 for WAN, GigabitEthernet for LAN
- **Clock rate**: Properly configured on DCE side (R2)
- **Encapsulation**: PPP encapsulation on WAN links

## Network Topology Summary
- **14 Routers**: 1x 4331, 13x 2901
- **14 Switches**: All 2960 models
- **13 Servers**: Excluding ISP servers as requested
- **2 OSPF Areas**: Area 0 (upper), Area 1 (lower)
- **16 VLANs**: Each with DHCP service
- **1 WAN Link**: R2-R5 (Serial connection)
- **Multiple LAN Links**: All other connections (Ethernet)
