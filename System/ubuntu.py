import os
import platform
import command
from inspect import stack

def get_architecture():
    if os.name == "posix":
        uname = platform.uname()
        return uname[4]
    else:
        return "Unknown architecture"

def get_numeric_version():
    if os.name == "posix":
        dist = platform.linux_distribution()
        return dist[1]
    else:
        return 0.0

def get_version():
    if os.name == "posix":
        dist = platform.linux_distribution()
        return dist[0]+ ' ' +get_numeric_version()+ ' ' +dist[2]+ ' ' +get_architecture()
    else:
        return "Unknown operating system version"

def get_kernel_version():
    if os.name == "posix":
        uname = platform.uname()
        return uname[2]
    else:
        return "Unknown kernel version"

def shutdown():
    return command.run('sudo shutdown now -h -q', True)

def reboot():
    return command.run('sudo reboot now -q', True)
