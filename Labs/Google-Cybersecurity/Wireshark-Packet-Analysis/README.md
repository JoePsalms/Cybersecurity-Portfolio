# Analyze Your First Packet with Wireshark — Google Cybersecurity Professional Certificate

## Project Description

A guided activity from the Google Cybersecurity Professional
Certificate, introducing packet capture analysis with Wireshark.
Completed with a perfect score (100%). The activity covers reading
a packet capture (PCAP), applying display filters to isolate
specific traffic, and manually inspecting individual packets to
identify key header fields.

## Objective

- Understand what a network packet is and how it's structured.
- Use Wireshark display filters to isolate specific traffic within
  a packet capture.
- Analyze individual packets to identify fields such as Header
  Length, Time to Live (TTL), and Destination Address.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment, via Qwiklabs)
- Tool: Wireshark
- Sample file: `sample.pcap`

## Concepts Covered

- **Traffic flows** — the path data takes across a network between
  source and destination.
- **Data exfiltration** — unauthorized transfer of data out of a
  network, something packet analysis can help detect.
- **Packets and packet captures (PCAP)** — a packet is the basic
  unit of data sent across a network; a PCAP file is a recorded
  collection of packets captured from network traffic.
- **Packet structure** — a packet is made up of a **header**
  (contains metadata such as source and destination IP addresses),
  a **payload** (the actual data being carried), and a **footer**.

## Techniques Practiced

Applied Wireshark display filters to isolate specific traffic
within the capture, including:

| Filter | Purpose |
|---|---|
| `ip.src == 142.250.1.139` | Show only packets originating from this source IP address |
| `ip.dst` | Show only packets addressed to a specific destination IP |
| `eth.addr` | Filter by a specific Ethernet (MAC) address |
| `udp.port == 53` | Isolate DNS traffic (UDP port 53) |
| `tcp.port == 80` | Isolate HTTP traffic (TCP port 80) |
| `tcp contains "curl"` | Find TCP packets whose payload contains a specific string |

## Key Findings

Using the `ip.src == 142.250.1.139` filter isolated a sequence of
ICMP echo replies and a short TCP/HTTP exchange from that source,
including a `301 Moved Permanently` HTTP response, all directed to
`172.21.224.2`.

Expanding the **Internet Protocol Version 4** layer of an
individual packet in the Packet Details pane surfaced the raw IP
header fields directly, rather than relying on the summary shown
in the packet list:

- **Header Length:** 20 bytes (the standard IPv4 header length,
  confirming no IP options were present in this packet)
- **Time to Live (TTL):** 115
- **Destination Address:** 172.21.224.2

The TTL value is also a useful clue on its own: common operating
systems ship with a handful of standard starting TTL values (64,
128, 255), and the number decreases by one with every router hop a
packet passes through. A TTL of 115 is consistent with a packet
that started at 128 and crossed roughly 13 hops before being
captured.

## What I Learned

This activity was a good first exposure to reading raw packet data
rather than relying on a tool's summarized view of traffic. I
learned how to narrow down a large capture to just the traffic
that matters using display filters, and how to read the IP header
fields directly from an individual packet rather than inferring
them from the packet list's summary columns.

The TTL field in particular stood out as more than just a
technical detail — its value can hint at the originating device's
operating system and roughly how many network hops a packet
traveled, which is useful context when investigating traffic
during an incident.

## Ethical Considerations

This activity used a sample packet capture provided in a sandboxed
Google Cybersecurity Professional Certificate guided lab
environment. No real network traffic or personal data was
captured or analyzed.
