# Linux

## CPU

## Mem

## Disk

## Performance

- Request profiling with bash

```
#!/bin/bash -xev
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

URL="https://www.example.com"
input="id.txt"

while IFS= read -r i
do
    curl -s -w '\nLookup time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nAppCon time:\t%{time_appconnect}\nRedirect time:\t%{time_redirect}\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n' "${URL}/id=${i}"
done < "${input}"
```
