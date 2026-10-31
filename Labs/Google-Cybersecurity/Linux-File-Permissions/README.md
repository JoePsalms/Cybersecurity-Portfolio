# File Permissions in Linux — Google Cybersecurity Professional Certificate

## Project Description

A guided project simulating a request from a research team to
audit and update file and directory permissions within a
`projects` directory, so that access levels match what the
organization actually authorizes.

## Objective

- Check existing file and directory permissions.
- Interpret the 10-character permissions string returned by
  `ls -l`.
- Update permissions on files and a directory, including a
  hidden file, to match the organization's access requirements.

## Environment

- Platform: Google Cybersecurity Professional Certificate
  (guided lab environment)
- Operating System: Linux
- Tools: `ls`, `chmod`

## Techniques Practiced

- Reading and interpreting Linux permission strings
  (`-rwxrwxrwx` format: file type, owner, group, other)
- Listing hidden files with `ls -la`
- Modifying permissions with symbolic mode (`chmod u-w`,
  `chmod g-w+r`, `chmod o-w`, `chmod g-x`)
- Distinguishing permission changes for owner, group, and other
- Applying permission changes to both files and directories

## Key Findings

An initial `ls -l` on the `projects` directory showed a mix of
permission levels across several files and one subdirectory
(`drafts`). Reviewing the permissions string for each entry (for
example, `-rw-rw-r--` on `project_t.txt`) showed which of the
owner, group, and other categories had read, write, or execute
access.

Based on the organization's requirement that **other** should
not have write access to any file, `project_k.txt` was updated
with `chmod o-w`, removing write access for other while leaving
owner and group access unchanged.

For a hidden, archived file (`.project_x.txt`), the requirement
was that no one should have write access, while owner and group
should retain read access. This was handled in two steps:
removing write access from the owner (`chmod u-w`), then
removing write access from the group while adding read access
(`chmod g-w+r`) to bring the group permissions in line with the
requirement.

Finally, the `drafts` directory's group execute permission was
removed with `chmod g-x`, restricting the group's ability to
enter that directory.

## What I Learned

This project reinforced how to read a Linux permissions string
at a glance and map each character to a specific access level
for owner, group, and other. I also practiced using `chmod` in
symbolic mode to make targeted permission changes — including
on hidden files and directories — rather than overwriting all
permissions at once, which matters when only one access level
needs to change.

## Ethical Considerations

This exercise was performed in an authorized, sandboxed guided
lab environment using simulated organizational data. No
production systems or real user data were involved.

## Note

Lab-specific screenshots and raw terminal output have been
summarized rather than reproduced verbatim in this public
write-up.
