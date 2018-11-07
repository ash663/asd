from socket import *
import re
import mapData as md
#import csv
import json
import redis

#filename = "datastore"
#target = open(filename, 'a')

#w = csv.writer(open("datastore.csv", "a"))

data = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
datastore = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}

'''
For webservers, I can send a GET request as a message
'''

def checkActive(targetIP):
    #Check port 22 TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(10)
    result = s.connect_ex((targetIP, 22))
    if(result == 0) :
        #print 'Port %d: OPEN' % (2222,)
        s.send('Testing this')
        data = s.recv(1024)
        if targetIP not in datastore['ssh']:
            #datastore['ssh'] = targetIP
            datastore['ssh'].append(targetIP)
            print targetIP+" has SSH service running"
    s.close()

    #Check port 80 HTTP
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(5)
    result = s.connect_ex((targetIP, 80))
    #print result
    #print targetIP
    if(result == 0) :
        #print 'Port %d: OPEN' % (80,)
        data = '0'
        try:
            s.send('GET \r\n')
            data = s.recv(1024)
        except:
            print "Timeout"
        #print '-'*50
        #print targetIP

        #print data
        if re.search('Server: ', data):
            position = re.search('Server: ', data).start()
            server = data[position:]
            server = server.split('\r\n')
            server = server[0]
            server = server.split(':')[1]
            if targetIP+":"+server not in datastore['server']:
                print targetIP+":"+server
                datastore['server'].append(targetIP+":"+server)

    s.close()


    #Check port 1433 MSSQL
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(10)

    result = s.connect_ex((targetIP, 1433))
    if(result == 0) :
        #print 'Port %d: OPEN' % (1433,)
        s.send('Testing this')
        #print s.recv(1024)
    s.close()

    #Check port 3306 MySQL
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((targetIP, 3306))
    if(result == 0) :
        #print 'Port %d: OPEN' % (3306,)
        s.send('show databases;')
        data = s.recv(1024)
        if re.search('.mysql.', data):
            if targetIP not in datastore['sql']:
                datastore['sql'].append(targetIP+':'+'3306')
                print targetIP+" has MySQL server"
    s.close()

    #Check port 6379 redis
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(10)
    result = s.connect_ex((targetIP, 6379))
    if(result == 0) :
        #s.send('PING')
        #print s.recv(1024)
        r = redis.StrictRedis(host=targetIP, port=6379, db=0)
        if r.ping():
            if targetIP not in datastore['redis']:
                datastore['redis'].append(targetIP)
                print targetIP+" has redis server"

    #target.write(datastore)

def writeData():
    #for key, val in datastore.items():
        #w.writerow([key, val])
    data = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}

    #Open the file, read it. Compare the data with new found data and merge data.
    with open('datastore.json', 'r+') as infile:
        #data = csv.reader(infile)
        try:
            data = json.load(infile)
            #print type(data)
            #for row in data:
            #    print row
            #    k, v = row
            #    dataFile[k] = v #Current data
            #    print type(v)
            #for key, val in datastore.items():
                #writer.writerow([key, val])
            #ds = (datastore, dataFile)
            #newData = {}
            #for k in datastore.iterkeys():
            #    newData[k] = list(newData[k] for newData[k] in ds)
            #newData = {}
            for k, v in datastore.iteritems():
                for i in v:
                    if i not in data[k]:
                        #print dataFile[k]
                        #print i
                        data[k].append(i)
            #print data
        except:
            print "ok"

    #Write data to file
    with open('datastore.json', 'w+') as outfile:
        #writer = csv.writer(outfile)
        #for key, val in dataFile.items():
        #    writer.writerow([key, val])
        #writer.writerows(dataFile.items())
        json.dump(data, outfile)
    md.mapData()
