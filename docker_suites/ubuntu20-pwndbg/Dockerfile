FROM ubuntu:20.04
 
ENV DEBIAN_FRONTEND=noninteractive
 
RUN dpkg --add-architecture i386
RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install libc6:i386 libncurses5:i386 libstdc++6:i386
RUN apt-get -y install socat gdb git gcc vim
RUN apt-get -y install gcc-multilib
 
RUN git clone https://github.com/pwndbg/pwndbg
WORKDIR pwndbg
RUN ./setup.sh
RUN apt-get -y install tmux
RUN apt-get -y install python3 libssl-dev libffi-dev build-essential
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pwntools
RUN apt-get -y install

