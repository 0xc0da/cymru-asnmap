# cymru-asnmap.py

cymru-asnmap.py is a python script to perform bulk IP submissions to the Team Cymru
whois service.

More on the Team Cymru Whois service: http://www.team-cymru.org/IP-ASN-mapping.html

## Dependencies
The netaddr module: https://pypi.python.org/pypi/netaddr

```
pip install netaddr
```

## Usage

```
usage: cymru-asnmap.py [-h] [-f] [-o FILENAME] target

positional arguments:
  target                Target to be queried.

optional arguments:
  -h, --help            show this help message and exit
  -f, --file            Load IPs from a file.
  -o FILENAME, --output FILENAME
                        Output CSV file.
```

### Examples

#### CIDR
```
$ python cymru-asnmap.py 68.22.187.0/29
Bulk mode; whois.cymru.com [2016-05-02 04:40:56 +0000]
23028   | 68.22.187.0      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.1      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.2      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.3      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.4      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.5      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.6      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
23028   | 68.22.187.7      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
```


#### List of IPs from a file
```
$ python cymru-asnmap.py -f input.txt
Bulk mode; whois.cymru.com [2016-05-02 04:34:05 +0000]
23028   | 68.22.187.5      | 68.22.187.0/24      | US | arin     | 2002-03-15 | TEAM-CYMRU - Team Cymru Inc., US
6079    | 207.229.165.18   | 207.229.128.0/18    | US | arin     |            | RCN-AS - RCN, US
701     | 198.6.1.65       | 198.6.0.0/16        | US | arin     |            | UUNET - MCI Communications Services, Inc. d/b/a Verizon Business, US
```

# License
* Copyright (c) 2016, Daniel C. Marques - Check the LICENSE file for license.
* Team Cymru WHOIS Copyright (c) 2015 Team Cymru. All Rights Reserved.
