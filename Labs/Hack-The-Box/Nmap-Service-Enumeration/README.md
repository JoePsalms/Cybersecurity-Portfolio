# Nmap Service Enumeration — Hack The Box

## Lab Overview

An authorized Hack The Box Academy lab focused on TCP port
scanning and service enumeration using Nmap.

## Objective

- Identify all TCP ports exposed by the target.
- Enumerate the services running on discovered ports.
- Identify the hostname of the target.
- Perform service/version detection.
- Investigate an unidentified service.

## Environment

- Platform: Hack The Box Academy
- Operating System: Kali Linux
- Tool: Nmap
- Target: HTB-provided lab target

## Techniques Practiced

- TCP port scanning
- Full port scanning
- Service/version detection
- Hostname enumeration
- Nmap XML output
- Service identification
- Banner analysis

## Key Findings

The full TCP scan identified seven open TCP ports.

| Port | Service |
|---|---|
| 22 | SSH |
| 80 | HTTP |
| 110 | POP3 |
| 139 | NetBIOS/SMB |
| 143 | IMAP |
| 445 | SMB |
| 31337 | Unidentified service |

Several services revealed their software versions during
service enumeration.

The service on port 31337 was not confidently identified by
Nmap and required additional investigation.

## Nmap Output Management

The scan results were saved in XML format using Nmap's
`-oX` option for later analysis.

## What I Learned

This lab improved my understanding of the difference between
basic port scanning and service enumeration.

I learned that a full TCP scan can reveal services running
on uncommon ports that may be missed by a default scan.

I also learned how Nmap's service/version detection can
identify software running behind open ports and that unknown
services may require additional enumeration.

Saving results in XML format also introduced me to storing
Nmap results for later analysis and reporting.

## Ethical Considerations

This exercise was performed against an authorized Hack The Box
Academy laboratory target.

No unauthorized systems were scanned.

## Note

Challenge-specific answers, flags, credentials, and other
solution details have been omitted from this public write-up.
