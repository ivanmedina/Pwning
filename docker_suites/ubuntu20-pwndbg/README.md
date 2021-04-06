# Ubuntu20-pwndbg

- Ubuntu 20.04
- Gdb:      9.2
- Python:   3.8.5 [GCC 9.3.0]
- Pwndbg:   1.1.0 build: cd3cbf3
- Capstone: 4.0.1024
- Unicorn:  1.0.2

### How to use

##### Build image
```
docker build -t pwn20:0.0 .
```
 ##### Run container to first time
```
 docker run -v /path/to/volume:/root/shared --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it --name pwn20 pwn20:0.0 bash
```
 ##### Start container after run and exit
```
 docker start  pwn20
```
 ##### Access the container
```
docker exec -ti pwn20 /bin/bash
```
 ##### Stop the container
```
docker stop pwn20
```
## Notes

To run exploit, first create a virtual environment for the python version you prefer with virtualenv ...

Python2.7: ```virtualenv -p /usr/bin/python2.7 /path/to/venv```

Python3:   ```virtualenv -p /usr/bin/python3 /path/to/venv```

Start virtualenv
```
source path/to/venv/bin/activate
```
Install pwntools
```
pip install pwn
```

If you want debug with ```python exploit.py GDB NOASLR```, first you need start tmux.
