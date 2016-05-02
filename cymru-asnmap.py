#!/usr/bin/python
"""Copyright (c) 2016, Daniel C. Marques
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of cymru-asnmap nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cymru-asnmap.py is a wrapper to perform bulk IP submissions to the Team Cymru
whois service.

Team Cymru Whois service: http://www.team-cymru.org/IP-ASN-mapping.html
"""

import socket
import csv
import argparse
from netaddr import IPNetwork


def to_csv(data, filename):
    """ Parses and cleans up the query response and generates a CSV file with
    the result.
    """
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(["AS", "IP", "BGP Prefix", "CC", "Registry",
                            "Allocated", "Info", "AS Name"])

        for line in data.split('\n')[1:]:
            csvwriter.writerow([column.rstrip(" ").lstrip(" ")
                                for column in line.split("|")])


def query(bulk_query, timeout):
    """ Connects to the whois server and sends the bulk query. Returns the
    result of this query.
    """
    try:
        data = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(("whois.cymru.com", 43))
        s.sendall(bulk_query)
        reply = s.recv(4098)
        data = reply
        # Gets data until an empty line is found.
        while True:
            reply = s.recv(1024)
            data += reply
    except socket.timeout:
        if data != '':
            pass
        else:
            raise
    except Exception as e:
        raise e
    finally:
        s.close()

    return data


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("target", help="Target to be queried (CIDR or filename).")
        parser.add_argument("-f", "--file", help="Loads the IPs from a file.",
                            dest="from_file", action="store_true")
        parser.add_argument("-t", "--timeout", type=int, dest="timeout",
                            default=5, help="Timeout (default is 5).")
        parser.add_argument("-o", "--output", help="Output CSV file.",
                            dest="filename")
        args = parser.parse_args()

        if args.filename:
            filename = argparse.filename
        else:
            filename = "output-asnmap.csv"

        if args.from_file:
            with open(args.target, "rb") as input_file:
                ips = input_file.read().rstrip("\n")
        else:
            net = IPNetwork(args.target)
            ips = "\n".join([str(ip) for ip in list(net)])

        # Creates the file for bulk submission
        bulk_query = "begin\nverbose\n%s\nend" % ips

        response = query(bulk_query, args.timeout)

        print response

        to_csv(response, filename)
        print "Output saved to: %s" % filename

    except Exception as e:
        print "Unable to proceed. Error: %s" % e

if __name__ == '__main__':
    main()
