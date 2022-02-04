# Goldbach (server)

## Running program on WSL2
To run the program in wsl2 it is necessary to configure the windows ports to connect with the virtual machine; this setting prepares ports from 5000 and up until you have enough ports for the variable called $CONSUMERS COUNT which is defined in the scripts, it is also necessary to modify the $WSL_IP variable with the wsl ip (it can be seen with the ifconfig command)

Steps (in powershell with admin permissions):
- Open script directory: cd goldbach-s_conjecture\goldbach_server
- Run script: .\wsl2_ports_conf.ps1
- Allow script: z

to restore the original settings:
- Open script directory: cd goldbach-s_conjecture\goldbach_server
- Run script: .\wsl2_ports_reset.ps1
- Allow script: z