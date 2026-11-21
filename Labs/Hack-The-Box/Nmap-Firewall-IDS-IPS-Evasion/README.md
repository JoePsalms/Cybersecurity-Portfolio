# Nmap — Firewall and IDS/IPS Evasion (Hard Lab) — Hack The Box

## Lab Overview

An authorized Hack The Box Academy lab, part of the Network
Enumeration with Nmap module, focused on evading basic
firewall and IDS/IPS controls while enumerating a protected
target.

## Objective

- Identify the target's operating system.
- Enumerate the DNS service and determine its version.
- Identify a service hidden behind firewall rules and
  determine its version.

## Environment

- Platform: Hack The Box Academy
- Operating System: Kali Linux (HTB Pwnbox)
- Tool: Nmap, ncat
- Target: HTB-provided lab target

## Techniques Practiced

- OS fingerprinting
- DNS service/version enumeration
- Firewall rule inference from scan behavior
- Source port spoofing (`--source-port`) to bypass
  port-based firewall filtering
- Manual banner grabbing with `ncat` when automated
  version detection returned `tcpwrapped`
- Resolving local port-binding conflicts (system DNS
  stub resolver) by binding to a specific interface

## Key Findings

An initial full port scan showed most high-numbered ports as
filtered, indicating firewall rules rather than closed
services. Spoofing the scan's source port to 53 (DNS) revealed
an additional open port that was not visible otherwise,
consistent with a firewall rule trusting traffic that appears
to originate from a DNS server.

Standard Nmap version detection against the discovered port
returned `tcpwrapped` — the TCP handshake succeeded, but the
service did not respond to Nmap's structured version probes.
Manually connecting with `ncat`, still spoofing the source
port, produced a banner that identified the service and its
version.

Nmap's default service-name guess for the port (based on its
well-known-ports list) did not match the actual service
running there, reinforcing that a banner or version scan
should always be trusted over a port-number assumption.

## What I Learned

This lab deepened my understanding of how firewalls can filter
traffic by source port, and how `--source-port` spoofing in
Nmap (and the equivalent in `ncat`) can be used to test and
bypass such rules during an authorized assessment.

I also learned that a `tcpwrapped` result doesn't mean
enumeration has failed — it means the automated probes didn't
get a response, and a manual banner grab is often the next
step.

Finally, I ran into a practical issue binding a local source
port that was already in use by the system's own DNS resolver,
and learned to resolve it by binding to a specific network
interface instead of the default wildcard address.

## Ethical Considerations

This exercise was performed against an authorized Hack The Box
Academy laboratory target. No unauthorized systems were
scanned.

## Note

Challenge-specific answers, flags, credentials, and other
solution details have been omitted from this public write-up.
