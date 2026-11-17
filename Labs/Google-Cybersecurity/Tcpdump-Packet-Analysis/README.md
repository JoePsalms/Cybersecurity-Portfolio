# Capturing and Viewing Network Traffic with tcpdump — Google Cybersecurity Professional Certificate

## Project Description

A guided lab from the Google Cybersecurity Professional
Certificate, focused on using `tcpdump` — a command-line packet
analyzer — to capture live network traffic, save it to a file, and
read it back for inspection. This builds directly on the earlier
Wireshark packet analysis lab, applying the same packet-structure
concepts (headers, flags, source/destination, ports) through a
terminal-based tool instead of a GUI.

## Objective

- Identify available network interfaces for packet capture.
- Capture and interpret live packet data from a specific
  interface.
- Generate real network traffic and capture it to a `.pcap` file.
- Read and filter captured packet data from that file.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment, Qwiklabs)
- Operating System: Linux
- Tool: `tcpdump`, `curl`

## Techniques Practiced

**Listing available capture interfaces:**
```bash
sudo tcpdump -D
```
Lists every network interface available for capture — useful on
systems without `ifconfig` installed.

**Capturing live traffic with verbose output:**
```bash
sudo tcpdump -i eth0 -v -c5
```
| Flag | Purpose |
|---|---|
| `-i eth0` | Capture only from the `eth0` interface |
| `-v` | Verbose output — show detailed packet fields |
| `-c5` | Stop after capturing 5 packets |

**Capturing traffic to a file in the background:**
```bash
sudo tcpdump -i eth0 -nn -c9 port 80 -w capture.pcap &
curl opensource.google.com
ls -l capture.pcap
```
| Flag | Purpose |
|---|---|
| `-nn` | Don't resolve IP addresses or port numbers to names |
| `-c9` | Capture 9 packets, then exit |
| `port 80` | Only capture traffic on port 80 (HTTP) |
| `-w capture.pcap` | Write captured packets to a file |
| `&` | Run the capture in the background so the shell stays free |

Running `curl opensource.google.com` immediately afterward
generates real HTTP traffic for `tcpdump` to capture, and `ls -l`
confirms the file was written.

**Reading and filtering the captured file:**
```bash
sudo tcpdump -nn -r capture.pcap -v
sudo tcpdump -nn -r capture.pcap -X
```
| Flag | Purpose |
|---|---|
| `-r capture.pcap` | Read packets from the saved file instead of live traffic |
| `-v` | Verbose — detailed packet fields |
| `-X` | Show packet payload in both hex and ASCII |

## Key Findings

Running the live verbose capture (`-v`) surfaced several packet
fields worth understanding individually:

- **Link type and capture size** — e.g. `listening on eth0,
  link-type EN10MB (Ethernet), capture size 262144 bytes`,
  confirming which interface and Ethernet framing is in use.
- **Timestamp and protocol** — each packet line starts with a
  timestamp (e.g. `22:24:18.910372`) followed by the protocol,
  `IP`.
- **IP header details** (from `-v`) — ToS, TTL, packet ID, fragment
  offset, flags (e.g. `[DF]` = Don't Fragment), the inner protocol
  (e.g. `TCP (6)`), and total packet length.
- **Source and destination** — shown as
  `source_host.port > destination_host.port`, with the `>` arrow
  indicating the direction the traffic is flowing, and each
  hostname's suffix giving the port number used on that side of
  the connection.
- **TCP-specific fields** — flags (e.g. `[P.]` for PUSH+ACK),
  checksum, sequence and acknowledgment numbers, window size, TCP
  options, and payload length.

Using `-nn` when capturing to a file (rather than relying on
default name resolution) is a deliberate security practice: it
avoids relying on DNS/port-name lookups that may not be accurate,
and avoids generating extra DNS traffic that could tip off anyone
monitoring the network during an investigation.

Reading the saved file back with `-X` showed the packet payload in
both hex and ASCII side by side, which is useful for actually
reading human-readable content (such as HTTP headers) directly out
of a capture, rather than just seeing structured field summaries.

## What I Learned

This lab reinforced the same packet-structure concepts from the
earlier Wireshark activity, but from the command line — which
matters because `tcpdump` is available on virtually every Linux
system by default, with no GUI required, making it a practical
tool for a remote server or a system where installing Wireshark
isn't an option.

Running a capture in the background (`&`) while generating traffic
with `curl` in the same terminal session was a good practical
pattern: it's the same idea as "start recording, then do the thing
you want to observe," which is how a real investigation or
troubleshooting session would actually work — you often need to
capture traffic while simultaneously triggering the activity you
want to inspect.

I also picked up on why `-nn` matters specifically from a security
perspective: letting `tcpdump` resolve names by default isn't just
slower, it can also alert someone being investigated (through the
extra DNS lookups it generates) that their traffic is being
captured.

## Ethical Considerations

This lab was performed in a sandboxed Google Cybersecurity
Professional Certificate guided lab environment, generating only
test traffic (a `curl` request to a public site) for the purpose
of the exercise. No real network traffic or personal data was
captured.
