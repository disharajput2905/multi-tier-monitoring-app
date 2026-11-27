#!/bin/bash
echo "=======MEMORY======="
free -h

echo "=======DISK========="
df -h / 

echo "======SYSTEMLOAD======="
uptime

echo "======TOP MEMORY PROCESS======="
ps aux --sort=-%mem | head -n 8
