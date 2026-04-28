
# Enhanced Task 2 Network v2 - Device Summary
Generated on 2025-10-25 16:18:47

## Devices Included:
- **Routers**: 14 (1x 4331, 13x 2901)
- **Switches**: 14 (All 2960)
- **Servers**: 13 (Excluding ISP servers)

## Devices Excluded (as requested):
- Local ISP R1, R2, R3, R4
- ISP S1, S2, S3, S4 (3650 models)
- ISP Remote devices
- 4331 ISP Remote (ping 9.9.9.9)

## Key Features:
- OSPF routing with 2 areas
- DHCP services on all routers
- VLAN segmentation
- Port security on switches
- Management VLANs
- **Proper WAN/LAN link distinctions**

## WAN vs LAN Links:
- **WAN Links**: R2-R5 (Serial interfaces, PPP encapsulation, clock rate)
- **LAN Links**: All other connections (Ethernet interfaces)

## Special Requirements:
- R2 (4331) requires EHWIC-4ESG module for multiple connections
- R2-R5 WAN link requires Serial DCE cable
- No internet connectivity (ISP excluded)
- Area 0: Upper section, Area 1: Lower section

## Interface Summary:
### R2 (4331) Interfaces:
- G0/0/0: LAN to R1
- G0/0/1: LAN to R3  
- G0/1/0: LAN to R4
- S0/0/0: **WAN to R5** (DCE side with clock rate)
- G0/1/1: LAN to SW2

### R5 (2901) Interfaces:
- S0/0/0: **WAN to R2** (DTE side)
- G0/0: LAN to SW5
