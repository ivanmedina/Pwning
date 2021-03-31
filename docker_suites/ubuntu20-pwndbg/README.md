#ubuntu20-pwndbg

- Ubuntu 20.04
- Gdb:      9.2
- Python:   3.8.5 [GCC 9.3.0]
- Pwndbg:   1.1.0 build: cd3cbf3
- Capstone: 4.0.1024
- Unicorn:  1.0.2

###How to use

#####Build image
```
docker build -t pwn20:0.0 .
```
 #####Run container to first time
```
 docker run -v /path/to/volume:/root/shared -it --name pwn20 pwn20:0.0 bash
```
 #####Start container after run and exit
```
 docker start  pwn20
```
 #####Access the container
```
docker exec -ti pwn20 /bin/bash
```
 #####Access the container
```
docker exec -ti pwn20 /bin/bash
```
 #####Stop the container
```
docker stop pwn20
```
