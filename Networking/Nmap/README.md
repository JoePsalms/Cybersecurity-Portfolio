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

The Nmap scan identified open network ports and the services
associated with them.

Open ports increase the attack surface of a system because
they provide potential entry points that an attacker could
attempt to interact with.

During this lab, particular attention was given to:

- Open ports and their associated services
- Service versions that may require security updates
- Services that may not be necessary for the system
- Potentially exposed administrative services

An exposed service is not automatically a vulnerability. Further
investigation would be required to determine whether the service
is securely configured and whether it contains known vulnerabilities.


## Recommendations

Based on the reconnaissance performed, the following security
measures are recommended:

1. Disable unnecessary services and close unused ports.
2. Keep exposed services updated with the latest security patches.
3. Restrict administrative services such as SSH to trusted
   networks where possible.
4. Use strong authentication and disable insecure authentication
   methods.
5. Implement firewall rules to limit unnecessary network exposure.
6. Regularly scan systems to identify newly exposed services.
7. Investigate identified service versions for known vulnerabilities
   during a full authorized security assessment.

## What I Learned

This lab helped me understand how network reconnaissance is
performed during the early stages of a penetration test.

I learned how Nmap can be used to identify open ports and
determine which services are running on a target system.

I also learned that discovering an open port does not
automatically mean that the system is vulnerable. The service,
version, configuration, and surrounding security controls need
to be investigated before determining whether a security issue
exists.

This lab also helped me understand the importance of
enumeration in penetration testing, because information
collected during reconnaissance can guide later stages of
security testing.




