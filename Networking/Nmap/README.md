# Nmap Network Reconnaissance Lab

## Objective

Learn how to perform basic network reconnaissance using Nmap
in an authorized lab environment.

## Environment

- Kali Linux
- Target: Authorized laboratory machine
- Tool: Nmap

## Tasks

- Identify live hosts
- Identify open ports
- Identify running services
- Perform service/version detection
- Analyze discovered services

## Commands Used

```bash
nmap <target>
nmap -sV <target>
nmap -O <target>
```
## Security Implications

The reconnaissance scan identified three externally accessible TCP services on the authorized target:
## Nmap scan report for [AUTHORIZED-TARGET] ([REDACTED-IP])
* **Port 80/tcp — HTTP**
* **Port 443/tcp — HTTPS**
* **Port 587/tcp — SMTP Submission**

The presence of these open ports indicates that the target exposes web and email-related services to the network. Each publicly accessible service represents part of the system's attack surface and should therefore be properly configured, secured, and maintained.

Port 80 provides HTTP access, which is unencrypted by default. It should be investigated to determine whether it appropriately redirects users to HTTPS.

Port 443 provides HTTPS access and should use a properly configured and up-to-date TLS implementation.

Port 587 is commonly used for SMTP message submission. Because this service may handle email authentication and transmission, it should require appropriate authentication and encryption.

The scan also showed that **997 TCP ports were filtered**, meaning Nmap received no response from those ports. This may indicate that firewall rules or other network controls are limiting access to those ports.

The scan itself does not establish that any of these services are vulnerable. Further authorized enumeration and security testing would be required to determine whether vulnerabilities exist.

## Recommendations

Based on the reconnaissance results, the following security measures are recommended:

1. **Review HTTP (Port 80):** Verify that HTTP traffic is intentionally exposed and, where appropriate, redirected to HTTPS.

2. **Secure HTTPS (Port 443):** Ensure that HTTPS uses current TLS protocols, valid certificates, and secure configurations.

3. **Secure SMTP Submission (Port 587):** Require strong authentication and encrypted connections for email submission.

4. **Keep Services Updated:** Regularly apply security updates and patches to the web server, mail server, and associated software.

5. **Review Exposed Services:** Confirm that all publicly accessible services are necessary and properly configured.

6. **Maintain Firewall Controls:** Continue using firewall rules to restrict unnecessary network access and reduce the attack surface.

7. **Perform Further Authorized Testing:** Conduct additional service enumeration and vulnerability assessment to determine whether the exposed services contain security weaknesses.

## What I Learned

This lab introduced me to the practical use of Nmap for network reconnaissance during the early stages of a penetration test.

I learned how Nmap can identify whether a host is reachable and determine which TCP ports are open, filtered, or not responding.

The scan identified HTTP, HTTPS, and SMTP submission services on the authorized target. This helped me understand how open ports can reveal information about the services a system exposes to a network.

I also learned that an open port does not automatically mean that a vulnerability exists. The service running on the port needs to be identified, enumerated, and assessed before determining whether a security weakness is present.

Most importantly, this exercise helped me understand the relationship between **reconnaissance, enumeration, and vulnerability assessment** in a penetration-testing workflow.



