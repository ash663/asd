import re
import mapData as md
import json

#filename = "datastore"
#target = open(filename, 'a')
#w = csv.writer(open("datastore.csv", "a"))
datastore = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
dataF = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
#TODO: Use addr:port or dict of arrays?

def checkInfo(data, d_addr, s_addr, dest_port, datastore):
    #d_addr = []
    #print data
    if re.search('GET /wp-.', data):
        if d_addr not in datastore['wp']:
            datastore['wp'].append(d_addr)
            #d_addr.add(dest_port)
            #datastore['wp'] = d_addr
            print d_addr+" hosts wordpress application"
    if re.search('.sql.', data) and re.search('.client.', data):
        if d_addr not in datastore['sql']:
            datastore['sql'].append(d_addr+':'+dest_port)
            print d_addr+" has MySQL server"
    if re.search('Server: ', data):
        position = re.search('Server: ', data).start()
        server = data[position:]
        server = server.split('\r\n')
        server = server[0]
        server = server.split(':')[1]
        if s_addr+":"+server not in datastore['server']:
            print s_addr+":"+server
            datastore['server'].append(s_addr+":"+server)
    if re.search('M.i.c.r.o.s.o.f.t. .S.Q.L. .S.e.r.v.e.r.....', data):
        print "MSSQL server here"
    #Write data to file
    #target.write(datastore)
    #for key, val in datastore.items():
    #    w.writerow([key, val])
    #with open('packetData.json', 'w+') as outfile:
    #        json.dump(data, outfile)

    dataF=json.load(open('datastore.json'))
    for k, v in datastore.iteritems():
        for i in v:
        #print '-' * 20
            #print i, v
            if i not in dataF[k]:
                        #print dataFile[k]
                        #print i
                dataF[k].append(i)
    with open('datastore.json', 'w+') as outfile:
        #writer = csv.writer(outfile)
        #for key, val in dataFile.items():
        #    writer.writerow([key, val])
        #writer.writerows(dataFile.items())
        try:
            json.dump(dataF, outfile)
        except:
            print "Cant write"

    #md.mapData()
def writeData():
    #for key, val in datastore.items():
        #w.writerow([key, val])
    dataFile = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
    #print datastore
    #Open the file, read it. Compare the data with new found data and merge data.
    #with open('datastore.json', 'r+') as infile:
        #data = csv.reader(infile)


    dataF=json.load(open('datastore.json'))
            #dataF = json.load(infile)
            #print dataF
            #for row in data:
                #k, v = row
                #dataFile[k] = v #Current data
                #print type(v)
            #for key, val in datastore.items():
                #writer.writerow([key, val])
            #ds = (datastore, dataFile)
            #newData = {}
            #for k in datastore.iterkeys():
            #    newData[k] = list(newData[k] for newData[k] in ds)
            #newData = {}
    for k, v in datastore.iteritems():
        for i in v:
        #print '-' * 20
            print i, v
            if i not in dataF[k]:
                        #print dataFile[k]
                        #print i
                dataF[k].append(i)
            #datastore=data
    #except:
    #        print "Cant read datastore file"
    '''    data = json.load(infile)

        for row in data:
            print row
            k, v = row
            dataFile[k] = v #Current data
            print type(v)
        #for key, val in datastore.items():
            #writer.writerow([key, val])
        #ds = (datastore, dataFile)
        #newData = {}
        #for k in datastore.iterkeys():
        #    newData[k] = list(newData[k] for newData[k] in ds)
        #newData = {}
        print datastore
        for k, v in datastore.iteritems():
            for i in v:
                if i not in dataFile[k]:
                    #print dataFile[k]
                    #print i
                    dataFile[k].append(i)'''
    #Write data to file
    with open('datastore.json', 'w+') as outfile:
        #writer = csv.writer(outfile)
        #for key, val in dataFile.items():
        #    writer.writerow([key, val])
        #writer.writerows(dataFile.items())
        try:
            json.dump(dataF, outfile)
        except:
            print "Cant write"
    #md.mapData()
