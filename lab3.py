import mmap
import os
import time
import socket
import struct

# HPS/FPGA Memory Addresses
HW_REGS_BASE = 0xFC000000
HW_REGS_SPAN = 0x04000000
HW_REGS_MASK = HW_REGS_SPAN - 1
ALT_LWFPGASLVS_OFST = 0xFF200000
LEDS = 0x00000100

# UDP Server Info
UDP_IP = "192.168.1.9"  # Replace with your IP address
UDP_PORT = 5005  # Replace with your desired port

# Convert 1 digit into 7-seg bit pattern
numtable = {
    "0": 0x40,
    "1": 0x79,
    "2": 0x24,
    "3": 0x30,
    "4": 0x19,
    "5": 0x12,
    "6": 0x02,
    "7": 0x78,
    "8": 0x00,
    "9": 0x10,
    "-": 0xBF
}

# Convert list of 4 numtable into mmap writable string
def cons(bins):
    s = ""
    f = 0
    for i in range(0, 4):
        f = f | bins[i] << (i * 7)

    for i in range(0, 4):
        t = f >> (i * 8)
        s = s + chr(t & 0xFF)

    return s

# Open memory as file descriptor
fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)

# Check if opened successfully
if fd == -1:
    print("Error opening /dev/mem!")
    exit()

# Map /dev/mem to writable block of memory
vb = mmap.mmap(
    fd,
    HW_REGS_SPAN,
    flags=mmap.MAP_SHARED,
    offset=HW_REGS_BASE
)

# 7-seg base address
pos = (ALT_LWFPGASLVS_OFST + LEDS) & HW_REGS_MASK

# Move memory block pointer to above address
vb.seek(pos)

# Display 4 numbers on Hex0-Hex3
def display(a, b, c, d):
    vb.write(cons([
        numtable[str(d)],
        numtable[str(c)],
        numtable[str(b)],
        numtable[str(a)]
    ]))
    vb.seek(pos)

# Sanity check
for i in range(0, 10):
    display(i, i, i, i)
    time.sleep(0.1)

# Reset
display("-", "-", "-", "-")

# UDP Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# UDP Server Listener
print("READY")
while True:
    # Receive data with a buffer size of 8 bytes (2 integers * 4 bytes per integer)
    data, addr = sock.recvfrom(8)

    # Unpack the brightness and contrast values
    brightness, contrast = struct.unpack('ii', data)
    
    print("Received Brightness: {}, Contrast: {}".format(brightness, contrast))

    # Display the brightness and contrast values (as an example, you can update this to match your display requirements)
    display(brightness // 10, brightness % 10, contrast // 10, contrast % 10)
