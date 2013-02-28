import command
import subprocess
import multiprocessing
import re
from inspect import stack

def get_current_resolution():
    screen = command.run("xrandr -q -d :0")
    width = screen.split()[7]
    height = screen.split()[9][:-1]
    return width+ ' x ' +height
    
def get_maximum_resolution():
    screen = command.run("xrandr -q -d :0")
    width = screen.split()[11]
    height = screen.split()[13]
    return width+ ' x ' +height
    
def get_cpu_type():
    cpuInfo = subprocess.check_output("cat /proc/cpuinfo", shell=True).strip()
    for line in cpuInfo.split("\n"):
        if "model name" in line:
            return re.sub( ".*model name.*:", "", line,1)
          
def get_cpu_load():
    return command.run("ps aux|awk 'NR > 0 { s +=$3 }; END {print s}'")
    
def get_cpu_core_count():
    return multiprocessing.cpu_count()
    
def get_vga():
    return command.run("lspci |grep VGA")
    
def get_gpu_manufacturer():
    vga = get_vga()
    manufacturer = vga.split()[4]
    return manufacturer
    
def get_gpu_type():
    vga = get_vga()
    version = vga.split("[")[1].replace("]", "")
    return version
    
def get_total_ram():
    ramInfo = subprocess.check_output("cat /proc/meminfo", shell=True).strip()
    for line in ramInfo.split("\n"):
        if "MemTotal" in line:
            return (int(re.sub( "MemTotal: ", "", line , 1).replace(" kB", "")) / 1024)
            
def get_free_ram():
    ramInfo = subprocess.check_output("cat /proc/meminfo", shell=True).strip()
    for line in ramInfo.split("\n"):
        if "MemFree" in line:
            return (int(re.sub( "MemFree: ", "", line , 1).replace(" kB", "")) / 1024)
            
def get_ram_in_use():
    return (int(get_total_ram()) - int(get_free_ram()))
