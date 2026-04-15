# Networking Fundamentals Handbook

This file is a concept-first networking guide for placement prep.
It explains what each building block is, why it exists, and where you use it.

## 1. Big Picture

Networking is the system that lets devices exchange data.
If software is the logic, networking is the road system that moves requests and responses.

Real-world flow:

1. User opens an app or browser.
2. App finds server address (usually via DNS).
3. Data is split into packets and sent across networks.
4. Routers forward packets toward destination.
5. Server processes request and sends response.

## 2. What Is a Server?

A server is a computer (or software process) that provides a service to other computers.

Examples:

- Web server serves websites.
- Database server stores and returns data.
- Mail server sends and receives email.
- File server stores shared files.

Key idea:

- A server is defined by its role, not by hardware size.
- Your laptop can be a server if it serves requests.

## 3. What Is a Client?

A client is a device or app that requests services from a server.

Examples:

- Browser requesting a web page.
- Mobile app calling a backend API.
- Desktop app querying database through API.

Client-server model:

- Client asks.
- Server answers.

## 4. What Is a Network?

A network is a group of connected devices that can communicate.

Common types:

- LAN (Local Area Network): home, office, campus.
- WAN (Wide Area Network): connects distant locations.
- Internet: global network of networks.

## 5. Data Units You Should Know

- Frame: Layer 2 data unit (inside local network).
- Packet: Layer 3 data unit (IP routing between networks).
- Segment/Datagram: Layer 4 data unit (TCP/UDP transport).

Interview point:

- People say "packet" for everything in casual discussion, but layer-specific terms matter in interviews.

## 6. IP Address: Device Identity

IP address is the logical address of a device in a network.

Two common versions:

- IPv4: 32-bit (example format: 192.168.1.10)
- IPv6: 128-bit (much larger address space)

Public vs private IP:

- Public IP is reachable on internet.
- Private IP is used inside private networks.

## 7. MAC Address: Local Hardware Identity

MAC address is a link-layer hardware identifier for a network interface.

Simple distinction:

- IP = logical address for routing between networks.
- MAC = local address for delivery on the current link.

## 8. DNS: Name to IP Translation

DNS converts human-readable names to IP addresses.

Example:

- You type example.com.
- DNS returns an IP.
- Browser connects to that IP.

Why DNS matters:

- Humans remember names.
- Networks route by addresses.

## 9. Port: Application Doorway

A port is a numbered endpoint used by a process/service on a machine.

One IP, many services:

- HTTPS on 443
- SSH on 22
- Database on 3306

Think of:

- IP as building address.
- Port as apartment number.

## 10. Protocol: Communication Rules

A protocol is an agreed set of rules for data exchange.

Core protocols:

- IP: addressing and routing
- TCP: reliable transport
- UDP: fast, connectionless transport
- HTTP/HTTPS: web communication
- DNS: name resolution

## 11. TCP vs UDP

TCP:

- Connection-oriented
- Reliable and ordered delivery
- Retransmissions, acknowledgements, flow control

UDP:

- Connectionless
- No delivery guarantees
- Lower overhead and lower latency

Typical use:

- TCP: web pages, APIs, transactions
- UDP: live calls, gaming, DNS queries

## 12. Router, Switch, and Firewall

Switch:

- Connects devices within same LAN.
- Forwards frames using MAC addresses.

Router:

- Connects different networks/subnets.
- Forwards packets using IP routes.

Firewall:

- Filters traffic using security rules.
- Can allow or deny by IP, port, protocol, direction.

## 13. Subnet and Segmentation

A subnet is a smaller logical network inside a larger network.

Why use subnets:

- Security isolation
- Better management
- Reduced broadcast scope

Typical architecture:

- Public subnet for internet-facing services.
- Private subnet for app and database tiers.

## 14. NAT: Private to Public Translation

NAT lets private IP systems access the internet via public IP addresses.

Common result:

- Many private hosts share one public IP for outbound traffic.

Why it exists:

- IPv4 address conservation
- Extra isolation from direct inbound internet traffic

## 15. DHCP: Automatic Network Configuration

DHCP automatically assigns:

- IP address
- Subnet mask
- Default gateway
- DNS servers

Without DHCP:

- Every device must be manually configured.

## 16. Load Balancer

A load balancer distributes incoming traffic across multiple backend servers.

Benefits:

- Higher availability
- Better scalability
- Maintenance without total downtime

Common types:

- Layer 4 load balancer: routes by IP/port.
- Layer 7 load balancer: routes by host/path/HTTP data.

## 17. Proxy and Reverse Proxy

Forward proxy:

- Acts on behalf of clients.
- Used for access control, filtering, anonymity.

Reverse proxy:

- Acts on behalf of servers.
- Used for TLS termination, caching, load balancing, hiding internals.

## 18. CDN (Content Delivery Network)

A CDN stores cached content closer to users at edge locations.

Benefits:

- Lower latency
- Reduced origin server load
- Better global performance

## 19. What Is Virtualization?

Virtualization allows multiple virtual machines (VMs) to run on one physical host.

VM basics:

- Each VM has guest OS.
- Managed by hypervisor.

Why VMs:

- Better hardware utilization
- Isolation between workloads

## 20. What Is a Container?

A container packages app code with runtime dependencies in an isolated unit.

Container vs VM:

- VM virtualizes full machine and OS.
- Container virtualizes at OS level and shares host kernel.

Benefits of containers:

- Fast startup
- Consistent environment
- Efficient resource usage

## 21. What Is Docker?

Docker is a platform/tooling ecosystem for building, shipping, and running containers.

Core Docker terms:

- Image: immutable template for a container.
- Container: running instance of image.
- Registry: image storage (public or private).
- Dockerfile: instructions to build image.

Container networking basics:

- Bridge network on single host.
- Port mapping from host port to container port.

## 22. What Is Kubernetes?

Kubernetes is a container orchestration platform.
It automates deployment, scaling, healing, and service discovery.

Why Kubernetes:

- Manage many containers across many machines.
- Replace failed containers automatically.
- Roll out updates safely.

Core Kubernetes objects:

- Pod: smallest deployable unit (usually one container).
- Deployment: declarative management of pod replicas and updates.
- Service: stable networking endpoint for a set of pods.
- Ingress: HTTP/HTTPS entry and routing rules into cluster.

## 23. Cloud Networking Essentials

In cloud, concepts are same but managed for you.

Common terms:

- VPC/VNet: isolated virtual network.
- Subnets: segmented network ranges.
- Internet Gateway: path between public subnet and internet.
- NAT Gateway: outbound internet access for private subnet.
- Security Group: stateful instance-level firewall.
- NACL: subnet-level traffic filter.

## 24. Network Security Basics

Core principles:

- Least privilege: allow only required traffic.
- Defense in depth: multiple security layers.
- Encrypt in transit: use TLS/HTTPS.
- Patch and harden systems regularly.

Common controls:

- Firewalls
- ACLs
- VPNs
- IDS/IPS
- WAF

## 25. Reliability and Performance Concepts

Latency:

- Time for data to travel from source to destination.

Throughput:

- Actual amount of data transferred per unit time.

Bandwidth:

- Maximum link capacity.

Jitter:

- Variation in delay between packets.

Packet loss:

- Packets that fail to reach destination.

Interview point:

- High bandwidth does not guarantee low latency.

## 26. Observability and Troubleshooting

Typical troubleshooting flow:

1. Is service up?
2. Is DNS resolution working?
3. Is network path reachable?
4. Is required port open?
5. Is firewall/security policy blocking?
6. Is backend healthy and responding?
7. Is latency/loss causing timeouts?

Useful tools to know:

- ping
- traceroute/tracert
- nslookup/dig
- curl
- netstat/ss
- tcpdump/Wireshark

## 27. End-to-End Example (Browser to Backend)

1. User enters a URL in browser.
2. Browser resolves domain with DNS.
3. Browser opens TCP connection to server.
4. If HTTPS, TLS handshake establishes secure session.
5. Browser sends HTTP request.
6. Load balancer routes request to an app server.
7. App server queries database or other services.
8. Response travels back to client.

Where failures can occur:

- DNS failure
- TCP connection timeout
- TLS certificate issue
- Firewall block
- App crash
- Database outage

## 28. Placement Interview Quick Answers

What is a server?

- A system that provides services/resources to clients over a network.

What is a container?

- A lightweight, isolated runtime package containing app code and dependencies, sharing host OS kernel.

What is Kubernetes?

- A platform that automates deployment, scaling, and management of containerized applications.

What is a subnet?

- A logical partition of an IP network used for isolation and routing control.

What is NAT?

- Address translation between private and public IP spaces, commonly for outbound internet access.

What is a load balancer?

- A component that distributes incoming traffic across multiple backend instances.

## 29. 7-Day Study Plan from This File

1. Day 1: Sections 1 to 6.
2. Day 2: Sections 7 to 12.
3. Day 3: Sections 13 to 17.
4. Day 4: Sections 18 to 22.
5. Day 5: Sections 23 to 25.
6. Day 6: Sections 26 and 27 with diagrams.
7. Day 7: Section 28 mock interview practice.

If you can explain each section with one real-world example, you are well prepared for networking interview fundamentals.
