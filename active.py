from socket import *
import checkActive as ca;
import nmap

if __name__ == '__main__':
    #target = raw_input('Enter host to scan: ')
    IP = []
    '''
    Todo:
    1. Ask user for IP or subnet mask (Make a config file later)
    2. Scan every port of all IP addresses
    3. Run signature analysis on each packet received
    4. Store data
    '''
    target = '127.0.0.1'
    targetIP = gethostbyname(target)
    #print 'Starting scan on host ', targetIP
    nm = nmap.PortScanner()
    for i in nm.scan(hosts='10.0.0.0/24', arguments='--min-parallelism 100 -sn')['scan']:
        IP.append(i)


    #scan reserved ports
    '''for i in range(20, 1025):
        s = socket(AF_INET, SOCK_STREAM)

        result = s.connect_ex((targetIP, i))

        if(result == 0) :
            print 'Port %d: OPEN' % (i,)
        s.close()'''
    #ca.checkActive(targetIP)

    for i in IP:
        ca.checkActive(i)

    ca.writeData()

    #After above returns, draw the map.
