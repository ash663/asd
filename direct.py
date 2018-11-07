import socket, sys
from struct import *
import re
import json
import checkInfo as ci
import thread


#initialise
datastore = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b

#create a AF_PACKET type raw socket (thats basically packet level)
#define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
try:
    s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# receive a packet
while True:
    packet = s.recvfrom(65565)

    #packet string from tuple
    packet = packet[0]

    #parse ethernet header
    eth_length = 14
    #6s6sH -> S_addr, d_addr, eth type
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    #2-byte swap operation
    eth_protocol = socket.ntohs(eth[2])
    #print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)

    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]

        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        #print iph[2]
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        #ntoa - convert 32bit IP address to dot-seperated string
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

        #TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]

            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4

            #Store data needed for mapping
            #if (source_port == 3306 or dest_port == 3306):
                #print "Source: " + str(source_port) + " Dest: " + str(dest_port)
            info = 'Source Port: ' + str(source_port) + ' Dest Port: ' + str(dest_port) + ' Source Address: ' + str(s_addr) + ' Dest Address: ' + str(d_addr) + '\n'
            with open('info', 'a+') as outfile:
                outfile.write(info)

            h_size = eth_length + iph_length + tcph_length * 4
            #data_size = len(packet) - h_size
            data_size = iph[2] - iph_length - tcph_length * 4

            #get data from the packet
            data = packet[h_size:]

            #thread.start_new_thread(ci.checkInfo, (data, d_addr, s_addr, str(dest_port), datastore),)
            ci.checkInfo(data, d_addr, s_addr, str(dest_port), datastore)
            #ci.writeData()
            #print 'Data : ' + data
            '''if re.search('GET /wp-.', data):
                if d_addr not in datastore['wp']:
                    datastore['wp'] = d_addr
                    print d_addr+" has wordpress application"

            elif re.search('.sql.', data) and re.search('.client.', data):
                if d_addr not in datastore['sql']:
                    datastore['sql'] = d_addr
                    print d_addr+" has SQL server"

            #elif re.search('')'''

        #ICMP Packets
        elif protocol == 1 :
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u+4]

            #now unpack them :)
            icmph = unpack('!BBH' , icmp_header)

            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]

            #print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)

            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) - h_size

            #get data from the packet
            data = packet[h_size:]

            #print 'Data : ' + str(data)

        #UDP packets
        elif protocol == 17 :
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]

            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)

            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)

            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size

            #get data from the packet
            data = packet[h_size:]

            #print 'Data : ' + str(data)

        #some other IP packet like IGMP. IGMP could be used to discover hosts
        else :
            print 'Protocol other than TCP/UDP/ICMP'

        #print
