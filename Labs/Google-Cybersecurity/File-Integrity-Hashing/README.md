# File Integrity Hashing — Google Cybersecurity Professional Certificate

## Lab Overview

A guided lab from the Google Cybersecurity Professional
Certificate, focused on using hash functions to verify file
integrity on Linux and detect when two files with identical
visible content are not actually identical at the byte level.

## Objective

- Compare the visible contents of two files.
- Generate a SHA-256 hash for each file.
- Save each hash to its own output file.
- Compare the hash output files to identify differences.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment)
- Operating System: Linux
- Tools: `ls`, `cat`, `sha256sum`, `cmp`

## Techniques Practiced

- File content comparison with `cat`
- Cryptographic hash generation with `sha256sum`
- Redirecting command output to a file (`>>`)
- Byte-level file comparison with `cmp`
- File integrity verification concepts

## Key Findings

Two files, `file1.txt` and `file2.txt`, appeared identical when
their contents were displayed with `cat` — both showed the same
visible text (an EICAR antivirus test string).

Generating a SHA-256 hash for each file, however, produced two
completely different hash values. Each hash was redirected into
its own file (`file1hash`, `file2hash`), and comparing those
files with `cmp` confirmed a difference starting at the very
first character.

This demonstrated that two files can look identical on screen
while differing in their underlying data — for example, due to
hidden characters, encoding differences, or trailing bytes not
visible in standard output.

## What I Learned

This lab reinforced why hashing is a core tool for file
integrity verification: visual inspection of a file's contents
is not reliable evidence that two files are the same. A hash
comparison can catch differences that `cat` alone would miss,
which is directly relevant to verifying that a file hasn't been
tampered with or corrupted.

I also practiced redirecting command output into files for
later comparison, and using `cmp` to quickly confirm whether two
files are byte-for-byte identical.

## Ethical Considerations

This exercise was performed in an authorized, sandboxed guided
lab environment using a well-known, non-malicious antivirus
test file (EICAR). No unauthorized systems or live malware
samples were involved.

## Note

Lab-specific questions and answers have been omitted from this
public write-up.
