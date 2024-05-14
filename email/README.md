
# sample cron cmd
```
*/3 * * * * cd /Users/weileizeng/Documents/GitHub/python-player/email && python3 check_ip.py >> /Users/weileizeng/Documents/GitHub/python-player/email/run.log 2>&1
```
run every 3 mins

`2>&1` combine stderr output to same file


# Q&A

## Fix cron not working issue on Mac OS

solution from

https://www.bejarano.io/fixing-cron-jobs-in-mojave/



```
Fixing cron jobs in macOS
Published Oct 8, 2018 by Ricard Bejarano
macOS Mojave introduced a new access control mechanism that lets you decide which apps have access to certain parts of the disk.

That’s great! (except it breaks some things)

The problem

Those familiar with UNIX-like systems sure know about cron, a job scheduler that comes installed on all macOS systems.

With the introduction of Mojave’s access control mechanism, cron can no longer access some directories, which might break your cron jobs.

The solution

macOS lets you add apps and binaries to the Full Disk Access allowlist, so let’s see which binary runs my cron jobs:

$ ps aux | grep [c]ron | awk '{print $NF}'
/usr/sbin/cron
The binary that runs the system’s cron jobs is /usr/sbin/cron.

Granting Full Disk Access to cron

Go to System Settings > Privacy & Security > Full Disk Access: 

Click on the (+) icon to add an item to the list.

Press command+shift+G, type /usr/sbin/cron and press enter: 

Select the cron exexcutable and click Open: 

That’s it!

Beware, this is not a great idea security-wise, if an attacker can modify cron jobs or their scripts, they would have Full Disk Access too.

Monitor the system’s installed cron jobs manually, or with a tool such as KnockKnock, and proceed with caution.



Thanks for dropping by!

Did you find what you were looking for?
Let me know if you didn't.

Have a great day!

Copyright © 2024 Ricard Bejarano.
Subscribe via RSS or email.
```





