
# Enhanced Task 2 Network - Device Summary
Generated on 2025-10-24 15:32:15

## Devices Included:
- **Routers**: 14 (1x 4331, 12x 2901)
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
- Redundant paths (where applicable)

## Special Requirements:
- R2 (4331) requires EHWIC-4ESG module for 4 connections
- No internet connectivity (ISP excluded)
- Area 0: Upper section, Area 1: Lower section
