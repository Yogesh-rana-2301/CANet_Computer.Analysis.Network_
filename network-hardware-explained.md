# Network Hardware Explained

This file turns the full device walkthrough into clear, study-friendly notes.

## 1. Modem

### What it does

- Brings internet service from your ISP into your home network.
- Converts signals between your ISP line and your digital devices.

### Why the name matters

- Modem = modulator + demodulator.
- Demodulation: converts incoming analog line signals into digital data.
- Modulation: converts outgoing digital data into line signals for ISP transport.

### Data flow

1. ISP sends data over cable, DSL line, fiber, satellite, or cellular link.
2. Modem demodulates line signal to digital bits for your network.
3. Your device sends data out.
4. Modem modulates digital data for upstream transport.

### Common modem types

- Cable modem: uses coaxial cable.
- DSL modem: uses telephone lines.
- Fiber modem or ONT: handles fiber-optic internet.
- Satellite modem: uses satellite internet links.
- Cellular or wireless modem: uses mobile network connectivity.

### Key takeaway

- No modem, no internet access from ISP.

## 2. Router

### What it does

- Shares one internet connection across many devices.
- Creates and manages your local area network (LAN).

### Core functions

- Assigns local IP addresses (usually via DHCP service).
- Tracks devices and sends each packet to the right destination.
- Uses routing tables to choose packet paths.
- Uses NAT so many local devices share one public IP.
- Often provides built-in Wi-Fi in home setups.

### Key takeaway

- Modem gets internet in.
- Router distributes internet across your devices.

## 3. Switch

### What it does

- Expands wired connectivity for devices in the same LAN.

### Why it matters

- Routers have limited Ethernet ports.
- A switch adds many more ports (often 5 to 48+).

### How it works

- Learns device MAC addresses per port.
- Stores this mapping in a MAC address table.
- Forwards frames only to the matching destination port.

### Technical note

- Operates at OSI Layer 2 (Data Link layer).
- Does not route between networks and usually does not assign IP addresses.

### Switch vs hub

- Hub broadcasts to all ports (inefficient).
- Switch forwards only where needed (efficient).

## 4. Access Point (WAP)

### What it does

- Provides Wi-Fi access from a wired network connection.

### How it works

1. Connect AP to router or switch through Ethernet.
2. AP broadcasts wireless signal (SSID).
3. Phones, laptops, and tablets join wirelessly.
4. AP bridges wireless traffic into the wired LAN.

### Important distinction

- AP does not perform routing for the network.
- Router still handles routing, NAT, and usually DHCP.

### Where it is useful

- Large homes with dead zones.
- Offices, schools, hotels, and multi-floor buildings.

### AP vs range extender

- Access point: wired uplink, usually better stability and speed.
- Range extender/repeater: wireless uplink, easier setup but often slower.

## 5. Firewall

### What it does

- Acts as the network security gatekeeper.
- Inspects traffic and allows or blocks based on policy rules.

### What it checks

- Source and destination addresses.
- Ports and protocols.
- Connection behavior and suspicious patterns.

### Typical blocked threats

- Unauthorized inbound access attempts.
- Known malicious IPs.
- Port scanning and abnormal traffic patterns.

### Types

- Hardware firewall: protects the whole network perimeter.
- Software firewall: runs on a single endpoint (for example, Windows or macOS firewall).

### Practical note

- Many home routers include basic firewall features.
- Advanced setups use dedicated firewall appliances for deeper control.

## 6. NIC (Network Interface Card)

### What it does

- Physical interface that connects a device to a network.
- Converts device-level digital data into network-transmittable signals and back.

### Identity

- Every NIC has a unique MAC address.
- MAC acts as a hardware identifier on local network segments.

### Types

- Wired NIC: Ethernet port, common in desktops, servers, and docking stations.
- Wireless NIC: Wi-Fi radio interface, built-in or USB/PCIe adapter.

### Speed examples

- Common wired rates: 100 Mbps, 1 Gbps, 2.5 Gbps, 10 Gbps+.

## 7. Bridge and Gateway (Quick Clarification)

### Bridge

- Connects two network segments, commonly at Layer 2.
- Useful for extending or joining LAN segments.

### Gateway

- Connects different networks or protocols.
- In home networking, the router is usually the default gateway to the internet.

## 8. How These Devices Work Together

1. Modem connects your home to ISP service.
2. Router creates LAN and shares internet to many devices.
3. Switch adds more wired ports when needed.
4. Access point extends wireless coverage from the wired LAN.
5. Firewall enforces traffic security rules.
6. NIC in each device performs the physical network interface role.

## 9. Fast Recap

- Modem translates ISP line signals and gives internet entry.
- Router manages traffic between your devices and the internet.
- Switch efficiently connects many wired devices in one LAN.
- Access point provides Wi-Fi from a wired uplink.
- Firewall filters traffic and blocks threats.
- NIC is the hardware interface that lets each device join the network.
