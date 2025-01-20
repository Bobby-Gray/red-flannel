# red-flannel
Red Flannel

**Placeholder**
---
FIM/security log monitoring python project to watch log files, directories, and files for changes along with Mac OS Endpoint Security events for a later use case. 
---
Example output:
[2025-01-20 13:11:44] New file hash detected: /var/log/system.log: c9ec01c19c3b564393d85dd3ad8b8baa
[2025-01-20 13:11:44] New file hash detected: /var/log/install.log: 1c6d4a2a5c247c20bb7a3da9eac67265
[2025-01-20 13:11:44] New directory hash detected: /Library/Logs: cd2bce482260ea651bc5fb74bd92493c
[2025-01-20 13:11:44] New directory hash detected: /Users/username/Library/Logs: c172c7af5c330394fd07ac40bdba99cd
[2025-01-20 13:11:44] New directory hash detected: /Users/username/Documents/screenshots: c846afab228686d40b059cc601fed4af
[2025-01-20 13:11:44] New file hash detected: /Users/username/Documents/environments/red-flannel/tests/test_file_monitor.py: 848bec6c5a0b0d6f27232a7f4300a2f1
[2025-01-20 13:11:45] New directory hash detected: /private/var/db/uuidtext: b4a5ede3d3330de9045e9ab8670e413e
[2025-01-20 13:11:45] New file hash detected: /etc/hosts: a3f51a033f988bc3c16d343ac53bb25f
[2025-01-20 13:11:45] New file hash detected: /etc/passwd: 91210284c9d33258f8a90ecccaf7a7bf
[2025-01-20 13:13:14] New directory hash detected: /Applications: a63d4745c2da59b275e567afb626e9ed
[2025-01-20 13:13:14] New directory hash detected: /System/Library/LaunchDaemons: 1396ed57725f3d6a6f4daef2e85fc33e
[2025-01-20 13:13:14] New directory hash detected: /Library/LaunchDaemons: d41d8cd98f00b204e9800998ecf8427e
[2025-01-20 13:13:14] New directory hash detected: /tmp: 7d3f46ae35f1f78a2fffb7eb891eb2d3
[2025-01-20 13:13:18] New directory hash detected: /var/folders: 80ca04e6575af47b40b591a006efc13a
[2025-01-20 13:13:18] New file hash detected: /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist: 969269f6a9c90b0a742d0e044289b6cf
[2025-01-20 13:14:18] File(s) in monitored directory '/Users/username/Documents/screenshots' changed:
Old Directory MD5: c846afab228686d40b059cc601fed4af
New Directory MD5: 8264670f486a7182e9eb2df236b9de17
File(s) Changed: {('Screenshot 2025-01-20 at 1.11.59\u202fPM.png', '1fc6e496128b47ddd5aa5817811040bb')}
[2025-01-20 13:14:18] File modified: /Users/username/Documents/environments/red-flannel/tests/test_file_monitor.py:
 Old MD5: 848bec6c5a0b0d6f27232a7f4300a2f1
 New MD5: b0b70fadda6b7c417c61eda55b71b978
[2025-01-20 13:16:51] Pattern match: Unauthorized File Access
Path: '/Users/username/Documents/environments/red-flannel/tests/test_file_monitor.py'
Context: Log message contains unauthorized activity.
Line: !!!unauthorized!!!
