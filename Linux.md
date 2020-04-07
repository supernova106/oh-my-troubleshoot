# Linux

## Utilities

- search

```sh
# Search for pattern in file
grep pattern file

# Search recursively for pattern in directory
grep -r pattern directory

# Find files and directories by name
locate name

# Find files in /home/john that start with "prefix".
find /home/john -name 'prefix*'

# Find files larger than 100MB in /home
find /home -size +100M
```

- Find top disk usage dir/files

```sh
du -hs  * | sort -nr | head -5

# du command: Estimate file space usage.
# a : Displays all files and folders.
# sort command : Sort lines of text files.
# -n : Compare according to string numerical value.
# -r : Reverse the result of comparisons.
# head : Output the first part of files.
# -n : Print the first ‘n’ lines. (In our case, We displayed first 5 lines).
```

- Remove files older than 14 days

```sh
sudo find . -type f -mtime +14 -exec rm -r {} \;
```

### File transfer

```sh
# Secure copy file.txt to the /tmp folder on server
scp file.txt server:/tmp

# Copy *.html files from server to the local /tmp folder.
scp server:/var/www/*.html /tmp

# Copy all files and directories recursively from server to the current system's /tmp folder.
scp -r server:/var/www /tmp

# Synchronize /home to /backups/home
rsync -a /home /backups/

# Synchronize files/directories between the local and remote system with compression enabled
rsync -avz /home server:/backups/
```

### Tracing

strace

- Trace execution of command `strace`. Example: `strace ls`
- Trace only when certain/specific system calls are made: `strace -e trace=open,read who`
- Save a trace to a file `strace -o output.txt who`
- Watch a running process with PID=1363 `strace -p 1363`
- Print a timestamp for each output line of the trace: `strace -t who`
- Print relative time for system calls: `strace -r who`
- Generate batch statistics reports of system calls `strace -c who`

lsof

- List processes that have opened the specific file /var/log/syslog: `lsof /var/log/syslog`
- List processes that have opened files under the directory /var/log `lsof +d /var/log`
- List files opened by processes named "sshd": `lsof -c sshd`
- List files opened by a specific user named "foo": `lsof -u foo`
- List files opened by everyone except for the user named "foo" `lsof -u ^foo`
- List all open files for a specific process with PID=1081 `lsof -p 1081`
- List all network connections `lsof -i`
- List network connections in use by a specific process with PID=1014 `lsof -i -a -p 1014`
- List processes that are listening on port 22: `lsof -i :22`
- List all TCP or UDP connections

```sh
lsof -i tcp
lsof -i udp
```

## Sys Info

- Display Linux system information: `uname -a`
- Display kernel release information: `uname -r`
- Show which version of redhat installed: `cat /etc/redhat-release`
- Show how long the system has been running + load: `uptime`
- Show system host name: `hostname`
- Display the IP addresses of the host: `hostname -I`
- Show system reboot history: `last reboot`
- Show the current date and time: `date`
- Show this month's calendar: `cal`
- Display who is online: `w`
- Who you are logged in as: `whoami`
- Disk

```sh
# Show free and used inodes on mounted filesystems
df -i

# Display disks partitions sizes and types
fdisk -l

# Display disk usage for all files and directories in human readable format
du -ah

# Display total disk usage off the current directory
du -sh
```

## Hardware Info

- Display messages in kernel ring buffer: `dmesg`
- Display CPU information: `cat /proc/cpuinfo`
- Display memory information: `cat /proc/meminfo`
- Display free and used memory ( -h for human readable, -m for MB, -g for GB.): `free -h`
- Display PCI devices: `lspci -tv`
- Display USB devices: `lsusb -tv`
- Display DMI/SMBIOS (hardware info) from the BIOS: `dmidecode`
- Show info about disk sda: `hdparm -i /dev/sda`
- Perform a read speed test on disk sda: `hdparm -tT /dev/sda`
- Test for unreadable blocks on disk sda: `badblocks -s /dev/sda`

## Utilization

- Display processor related statistics: `mpstat 1`
- Display virtual memory statistics: `vmstat 1`
- Display free and used memory ( -h for human readable, -m for MB, -g for GB.): `free -h`
- top

  - us: user CPU time. More often than not, when you have CPU-bound load, it's due to a process run by a user on the system, such as Apache, MySQL or maybe a shell script. If this percentage is high, a user process such as those is a likely cause of the load.
  - sy: system CPU time. The system CPU time is the percentage of the CPU tied up by kernel and other system processes. CPU-bound load should manifest either as a high percentage of user or high system CPU time.
  - id: CPU idle time. This is the percentage of the time that the CPU spends idle. The higher the number here the better! In fact, if you see really high CPU idle time, it's a good indication that any high load is not CPU-bound.
  - wa: I/O wait. The I/O wait value tells the percentage of time the CPU is spending waiting on I/O (typically disk I/O). If you have high load and this value is high, it's likely the load is not CPU-bound but is due to either RAM issues or high disk I/O.

- iostat
  - tps: transactions per second.
  - Blk_read/s: blocks read per second.
  - Blk_wrtn/s: blocks written per second.
  - Blk_read: total blocks read.
  - Blk_wrtn: total blocks written.

```sh
Linux 4.4.0-1094-aws (hostname) 	04/06/1970 	_x86_64_	(2 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.51    0.00    0.47    0.06    0.68   96.28

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
loop0             0.00         0.01         0.00     126510          0
loop1             0.00         0.00         0.00      58873          0
loop2             0.01         0.01         0.00     194092          0
loop3             0.01         0.01         0.00     241909          0
loop4             0.01         0.01         0.00     233242          0
loop5             0.00         0.00         0.00         44          0
nvme2n1           0.05         1.15         0.00   18812918          0
nvme0n1           3.67        27.34        54.97  445455658  895569084
```

- iotop

```sh
# install
sudo apt-get update && sudo apt-get install -y iotop
```

```sh
Total DISK READ :       0.00 B/s | Total DISK WRITE :       0.00 B/s
Actual DISK READ:       0.00 B/s | Actual DISK WRITE:       0.00 B/s
  TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND
    1 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % systemd --system --deserialize 25
    2 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [kthreadd]
```

- Request profiling with bash

```
#!/bin/bash -xev
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

URL="https://www.example.com"
input="id.txt"

while IFS= read -r i
do
    curl -s -w '\nLookup time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nAppCon time:\t%{time_appconnect}\nRedirect time:\t%{time_redirect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' "${URL}/id=${i}"
done < "${input}"
```

## Users

```sh
# Display the user and group ids of your current user.
id

# Display the last users who have logged onto the system.
last

# Show who is logged into the system.
who

# Show who is logged in and what they are doing.
w

# Create a group named "test".
groupadd test

# Create an account named john, with a comment of "John Smith" and create the user's home directory.
useradd -c "John Smith" -m john

# Delete the john account.
userdel john

# Add the john account to the sales group
usermod -aG sales john
```

## Process

```sh
# Kill process with process ID of pid
kill pid

# Kill all processes named processname
killall processname

# Start program in the background
program &

# Display stopped or background jobs
bg

# Brings the most recent background job to foreground
fg

# Brings job n to the foreground
fg n
```

## Networking

```sh
# Display all network interfaces and ip address
ifconfig -a

# Display eth0 address and details
ifconfig eth0

# Query or control network driver and hardware settings
ethtool eth0

# Send ICMP echo request to host
ping host

# Display whois information for domain
whois domain

# Display DNS information for domain
dig domain

# Reverse lookup of IP_ADDRESS
dig -x IP_ADDRESS

# Display DNS ip address for domain
host domain

# Display the network address of the host name.
hostname -i

# Display all local ip addresses
hostname -I

# Download http://domain.com/file
wget http://domain.com/file

# Display listening tcp and udp ports and corresponding programs
netstat -nutlp
```

tcpdump

- Capture and display all packets on interface eth0: `tcpdump -i eth0`
- Monitor all traffic on port 80 ( HTTP ): `tcpdump -i eth0 'port 80'`
- Capture only 100 packets `tcpdump -c 100`
- Display captured packets in ASCII `tcpdump -A`
- Capture packet data, writing it into into a file `tcpdump -w saved.pcap`
- Read back saved packet data from a file `tcpdump -r saved.pcap`
- Capture only packets longer/smaller than 1024 bytes `tcpdump greater 1024`
- Capture only UDP or TCP packets `tcpdump tcp`
- Capture only packets going to/from a particular port `tcpdump port 22`
- Capture packets for a particular destination IP and port `tcpdump dst 54.165.81.189 and port 6666`

iftop

- Observe traffic for just the eth0 interface `iftop -i eth0`
- Filter to show only traffic going to/from IP address 54.84.222.1 `iftop -f "host 54.84.222.1"`

## Performance Tuning

There are two basic performance analysis methodologies you can use for most performance issues.

- The first is the resource-oriented USE Method, which provides a checklist for identifying common bottlenecks and errors.
- The second is the thread-oriented TSA Method, for identifying issues causing poor thread performance.

- [Read](http://www.brendangregg.com/index.html)
