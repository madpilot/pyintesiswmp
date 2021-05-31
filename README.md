```
netcat -ulk 3310
echo -e "DISCOVER\r\n" | nc -b -u 255.255.255.255 3310 -v
```
