import networkx as nx
import matplotlib.pyplot as plt
#import csv
import json
import re

datastore = {'wp':[], 'sql':[], 'server':[], 'ssh':[], 'redis':[]}
G=nx.MultiDiGraph()


def mapData():
    #reader = csv.reader(open('datastore.csv', 'r'))
    datastore = json.load(open('datastore.json'))
    #print type(datastore)
    #datastore = {'wp':'', 'sql':'', 'server':'', 'ssh':'', 'redis':''}
    #for row in reader:
    #    k, v = row
        #print v
        #v = v.replace("[","")
        #v = v.replace("]","")
        #v = v.split(",")
    #    datastore[k] = v
    print "----Mapping----"
    #print datastore


    for i, j in datastore.items():
        #print j+"JJJJJJJJJJJJ"
        if j is not []:
            for k in j:
                G.add_node(i+":"+k)

    '''try: # draw
        #pos=nx.spring_layout(G,iterations=1)
        nx.draw(G, with_labels=True)
        plt.savefig("test.png")
        plt.show()
    except: # matplotlib not available
        print "Nope"
        #Call Map'''
    map(datastore)

    #TODO: One module to map them all
def map(datastore):
    #packetData = json.load(open('packetData.json'))
    info = open('info', 'r')
    info = info.read()
    #print type(info)
    #Mapping wordpress

    for i in datastore['wp']:
        #print "THIS IS III"
        #print i
        for j in datastore['server']:
            #print '-'*50
            if i == j.split(':')[0]:
                #print i, j.split(':')[0]
                #print "Adding"
                G.add_edge('wp:'+i, 'server:'+j)
    for i in datastore['server']:
        serverIP = str(i.split(':')[0])
        serverName = str(i.split(':')[1])
        for j in datastore['sql']:
            sqlIP = str(j.split(':')[0])
            sqlPort = str(j.split(':')[1])
            #print type(serverIP), type(serverName), type(sqlIP), type(sqlPort)
            if re.search('Source Port: (.)* Dest Port: '+sqlPort+' Source Address: '+serverIP+' Dest Address: '+sqlIP, info):
                #print "Coming in SQL"
                G.add_edge('server:'+i, 'sql:'+j)
    for i in datastore['server']:
        serverIP = str(i.split(':')[0])
        serverName = str(i.split(':')[1])
        for j in datastore['redis']:
            if re.search('Source Port: (.)* Dest Port: 6379 Source Address: '+serverIP+' Dest Address: '+j, info):
                G.add_edge('server:'+i, 'redis:'+j)
    for i in datastore['sql']:
        for j in datastore['sql']:
            sqlIP1 = str(i.split(':')[0])
            sqlPort1 = str(i.split(':')[1])
            sqlIP2 = str(j.split(':')[0])
            sqlPort2 = str(j.split(':')[1])
            if re.search('Source Port: '+sqlPort1+' Dest Port'+sqlPort2, info):
                G.add_edge('sql:'+i, 'sql:'+j)
    




    nx.draw(G, with_labels=True)
    plt.savefig("test.png")
    plt.show()
    #except:
    #    print "Nah"
