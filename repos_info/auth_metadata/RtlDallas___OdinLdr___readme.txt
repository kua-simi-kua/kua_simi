# OdinLdr

Cobaltstrike UDRL

Features:
  - Redirect all WININET calls over callstack crafting
  - Encrypt beacon during sleep
  - Encrypt beacon heap during sleep
  - Self delete of loader

Callstack exemples:

CreateThread:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/createthread_callstack.PNG)

InternetOpenA:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/internetopa_callstack.PNG)

WaitForSingleObject:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/wfso_scalltack.png)

# EXECUTION OF LOADER
    
1 - Create heap for beacon usage

2 - Allocation of RWX area with beacon size + UDRL size

3 - Copy the UDRL at the end of beacon in allocated area

    | 0x00 | beacon | 0xBEACON_SIZE | UDRL | 0xEND_Alloc
    
4 - Copy the ODIN structure (heap handle, beacon addr, alloc size) to the start of allocated area (no pe header is present)

5 - Copy beacon section

6 - Resolve beacon import and patch IAT (also set hook)

7 - Patch relocation table

8 - Init the beacon

9 - Create thread on TpReleaseCleanupGroupMembers+0x450 to spoof the thread start addr & beacon run

10 - Self delete the loader

# BEACON RUN

- All WININET function is hooked and use callstack crafting for all wininet call
  
- Sleep is hooked:
  
    1 - XOR the heap (random key for each sleep)
  
    2 - Encrypt the beacon + udrl (remember this was copied at the end of beacon) with KrakenMask (ropchain, rwx->rw, encrypt, sleep, rw->rwx)
  
    3 - XOR the heap 


- ExitThread is hooked:
  
    1 - Destroy the beacon heap
  
    2 - Free the memory region with the beacon
  
    3 - Exit thread


 # HOW TO USE

Compile the loader and load the cna script (odin.cna)
  
About the cna, you need to edit path of variable $loader_path at line 11 & 38

# COBALTSTRIKE PROFILE NEEDED

```
http-beacon {
    set library "wininet";
	
}

stage {
	set smartinject "false";
	set sleep_mask "false";
}
```

# WARNING

It's a POC, be careful when using this UDRL

If you happen to have a crash, you can dm on twitter or open github issues, please send:

	- Cobaltstrike profil

  	- Debugger screen with callstack

You need to have python on your windows machine, you have post-ex build to run python script.

Python script uses two libraries: sys and pefile

# MEMORY SCANNER 

Moneta:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/moneta.PNG)

Pe-Sieve:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/pe-sieve.PNG)

HuntSleepingBeacons:

![alt text](https://raw.githubusercontent.com/RtlDallas/OdinLdr/main/img/HuntSleepingBeacons.PNG)


# CREDIT 

For code:

- Callstack craffting : https://github.com/susMdT/LoudSunRun
- Some parts of code : https://www.cobaltstrike.com/product/features/user-defined-reflective-loader

For idea:

- AceLdr : https://github.com/kyleavery/AceLdr
- BokuLdr : https://github.com/boku7/BokuLoader
- KaynStrike : https://github.com/Cracked5pider/KaynStrike

Thanks to:

- chatGPT, Bakki, Caracal & CobaltAD : For debug and somes help
