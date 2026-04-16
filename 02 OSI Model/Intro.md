# Intro

How is data sent over the internet?
What does that have to do with the OSI model?
How does TCP/IP fit into this?
Let's take a look.

## OSI Model

The OSI model, or the Open Systems Interconnect model, is a theoretical framework that provides one way of thinking about networking.

It splits network communication between two devices on a network into seven abstraction layers.

The physical layer is the bottom-most layer.
It is responsible for transmitting raw bits of data across a physical connection.

The data link layer is the second layer.
It takes the raw bits from the physical layer and organizes them into frames.
It ensures that the frames are delivered to the correct destination.
Ethernet primarily lives in this layer.

The network layer is the third layer.
It is responsible for routing data frames across different networks.
The IP part of TCP/IP is a well-known example of this layer.

The transport layer is the fourth layer.
It handles end-to-end communication between two nodes.
This is the layer where TCP and UDP live.

## TCP

TCP provides reliable, end-to-end communication between devices.
It does this by dividing data into small, manageable segments and sending each segment individually.
Each segment has a sequence number attached to it.
The receiving end uses sequence numbers to reassemble the data in the correct order.
TCP also provides error checking to make sure data was not corrupted during transmission.

## UDP

UDP is another popular protocol in the transport layer.
It is similar to TCP, but it is simpler and faster.
Unlike TCP, UDP does not provide the same level of error checking and reliability.
It simply sends packets of data from one device to another.
The receiving end is responsible for determining whether packets were received correctly.
If an error is detected, the receiving end simply discards the packet.

The remaining layers are the session, presentation, and application layers.
This is where the OSI model loses some usefulness in practice.
They are often too fine-grained and do not always reflect reality.
In general, it is sufficient to collapse them into a single layer and consider application protocols like HTTP as layer 7 protocols.

Let's go through an example and examine how data moves through layers when transmitting over the network.

When a user sends an HTTP request to a web server over the network, an HTTP header is added to the data at the application layer.
Then, a TCP header is added to the data.
It is encapsulated into TCP segments at the transport layer.
The TCP header contains the source port, destination port, and sequence number.

The segments are then encapsulated with an IP header at the network layer.
The IP header contains the source and destination IP addresses.

A MAC header is added at the data link layer, with source and destination MAC addresses.

## MAC Addresses

It is worth noting that in the real world this is a bit nuanced.
The MAC addresses are usually not the MAC address of the sending and receiving ends.
They are often the MAC address of routing devices in the next hop of a long journey across the internet.

## Raw Bits

The encapsulated frames are sent over the network as raw bits in the physical layer.
When the web server receives raw bits from the network, it reverses the process.
Headers are removed layer by layer, and eventually the web server processes the HTTP request.

## Conclusion

To conclude, the OSI model is one way of thinking about networks.
Its primary purpose is educational.
Even though the layers do not fit real-world use cases perfectly, they are still widely used by networking vendors and cloud providers as a shorthand to describe where networking products sit in the OSI model.

## Cloud Load Balancers

For example, cloud load balancers are broadly divided into two categories: L4 and L7.

An L7 load balancer is shorthand for a load balancer that operates at the application protocol layer, such as HTTP or HTTPS.

An L4 load balancer, on the other hand, operates at the TCP level.

If you'd like to learn more about system design, check out our books and weekly newsletter.
Please subscribe if you learned something new.
Thank you so much, and we'll see you next time.
