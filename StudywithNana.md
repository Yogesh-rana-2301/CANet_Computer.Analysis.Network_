# Study with Nana - Computer Networking Notes

These notes capture the full learning flow from the video using the TravelBody example (an imaginary travel booking app) that grows from one server to cloud-native Kubernetes.
 

## 1. Single Server Stage: IP and DNS

### Why this matters

At launch, TravelBody has one server. Users need a way to find it on the internet.

### IP Address

- Every device on a network needs an IP address.
- IP is a unique network identifier, like a house address for mail.
- A public IP lets internet users reach the server.

### DNS (Domain Name System)

- Humans remember names (like `travelbody.com`) better than IP numbers.
- DNS translates domain names to IP addresses.
- Analogy: phone contacts (name -> actual number).

### Key takeaway

IP identifies where to send data; DNS makes IP usable for humans.

---

## 2. Multiple Apps on One Server: Ports

### Problem

One server runs multiple applications:

- Website
- Database
- Payment service

All share one IP address. How does traffic reach the correct app?

### Ports

- Ports are logical numbered channels from 1 to 65,535.
- Each app listens on a specific port.

Example mapping:

- HTTP web traffic: port 80
- HTTPS secure web traffic: port 443
- MySQL: port 3306
- Custom payment service: port 9090

Analogy: apartment building.

- Building address = IP
- Apartment number = port

### Key takeaway

IP gets traffic to the machine; port gets traffic to the right process.

---

## 3. Security and Segmentation: Subnets, Routing, Firewalls

### Problem

Running everything together is risky. If one compromise happens, attacker can access everything.

### Network Segmentation with Subnets

- Split network into smaller isolated sections (subnets).
- Typical pattern:
  - Public/front-end subnet
  - App subnet
  - Database subnet

Benefits:

- Better isolation
- Better security boundaries
- Better organization

### Routing

- Routing connects different subnets.
- Router decides path from source to destination (like GPS for packets).

### Firewalls

Even if routing allows reachability, security policy must control what is actually allowed.

Two levels:

- Host firewall: on individual server
- Network firewall: between network segments

Example rules taught:

- DB server allows port 3306 only from approved subnet/IP range.
- Internet-facing firewall allows only 80/443 inbound, blocks others.

Security principle:

- Layered defense (multiple checkpoints).

### Key takeaway

Segmentation reduces blast radius, routing enables needed communication, firewalls enforce least privilege.

---

## 4. NAT (Network Address Translation)

### Problem

Many backend servers use private IPs (like 10.x.x.x). Private IPs cannot be reached directly from the public internet.

But private servers still need outbound internet access for:

- Updates
- Third-party APIs
- External services

Assigning public IP to every private server is costly and less secure.

### NAT solution

- NAT device translates private source IP to one public IP.
- Return traffic is mapped back to the correct private host.

Analogy: office receptionist using one company phone line for many employees.

### Key takeaway

NAT enables private instances to access internet while staying hidden from direct inbound internet traffic.

---

## 5. Cloud Networking: VPC, Subnets, Gateways, Route Tables

### Why move to cloud

- Hardware management is slow and expensive.
- Scaling on physical hardware takes weeks.
- Cloud enables rapid scaling and managed infrastructure.

### Important principle

Concepts do not change in cloud. They are provided as managed services.

### VPC (Virtual Private Cloud)

- Isolated logical network in a cloud provider.
- Similar to renting your own secured area in a larger building.

### Public and Private Subnets

- Public subnet: resources that need direct internet access.
- Private subnet: protected internal resources.

### Internet Gateway

- Connects public subnet resources to internet.

### Route Tables

- Rules that define where traffic goes from each subnet.

### NAT Gateway

- Managed cloud NAT service.
- Usually placed in public subnet.
- Private subnets route outbound internet traffic via NAT gateway.

### Key takeaway

Cloud abstracts hardware, not fundamentals. You still design around IPs, subnets, routing, and security.

--- 

## 6. Container Networking (Docker)

### Why containers were introduced

As architecture grows into microservices, deployment consistency becomes hard:

- "Works on my machine" problems
- Dependency/version drift

### Containers

- Package app code + runtime + dependencies + config.
- Portable across environments.

### Docker Bridge Network

- Default private network on a single host.
- Containers on same bridge can communicate.

### Port Mapping

- Container app listens on an internal port.
- Host port is mapped to container port for external access.
- Example concept: host:9090 -> container:9090.

### Overlay Network

- Spans multiple hosts.
- Allows containers on different servers to communicate as one virtual network.

### Key takeaway

Container networking introduces host/container boundaries and multi-host virtual networking.

---

## 7. Kubernetes Networking

### Problem at scale

Managing hundreds of containers manually is impractical.

### Pods

- Smallest deployable unit in Kubernetes.
- Usually one container per pod.
- Pod gets its own IP.
- Containers in same pod share that pod IP.

### Pod ephemerality

- Pods can be recreated anytime (crash, rollout, reschedule).
- New pod usually gets a new IP.
- Directly targeting pod IPs is fragile.

### Services

- Stable virtual endpoint for a set of pods.
- Provides stable IP and DNS name.
- Load balances to healthy backing pods.
- Consumers call service name, not individual pod.

### Ingress

- External entry point layer for HTTP/HTTPS traffic.
- Routes requests to internal services based on host/path rules.

Example routing pattern:

- `travelbody.com` -> website service
- `travelbody.com/api/booking` -> booking service
- `travelbody.com/api/payment` -> payment service

### Key takeaway

In Kubernetes, pods are dynamic, services provide stability, and ingress provides controlled external access.

--- 

## 8. Placement-Oriented Revision Checklist

Use this checklist before interviews:

- Explain difference between IP and DNS with a real request flow.
- Explain why ports are needed when one server runs multiple apps.
- Draw a 3-subnet architecture (public/app/db) and describe allowed traffic.
- Explain routing vs firewall (reachability vs permission).
- Explain NAT using outbound access from private subnet.
- Explain cloud equivalents: VPC, route table, internet gateway, NAT gateway.
- Explain Docker bridge network, port mapping, overlay network.
- Explain pod vs service vs ingress in Kubernetes.

---

## 9. Fast Self-Test Questions

1. If DNS is down but IP is known, can users still access the app?
2. Why is opening all ports dangerous even inside a private network?
3. Can private IP instances receive direct inbound internet traffic through NAT?
4. Why should app pods call Kubernetes service names instead of pod IPs?
5. What is the difference between ingress and a service in Kubernetes?

If you can answer these clearly, your fundamentals are in strong shape for placements.
