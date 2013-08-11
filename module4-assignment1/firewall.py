'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import os
import csv
#from pprint import pprint


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

        # Our firewall table
        self.firewall = {}
        myreader = csv.reader(open(policyFile))
        headerline = myreader.next()
        for myrow in myreader:
            myid, mysrc, mydst = myrow
            self.firewall[mysrc] = mydst
            #print 'my rule: block src:', mysrc, ' dst:', mydst
        #pprint(self.firewall)
                             

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        log.debug(" handle_connectionUp ")

        for key in self.firewall:
            msg = of.ofp_flow_mod()
            msg.priority = 65535
            msg.match = of.ofp_match()
            msg.match.dl_src = EthAddr(key)
            msg.match.dl_dst = EthAddr(self.firewall[key])

            #print ' match src:', msg.match.dl_src, ' dst:', msg.match.dl_dst
            event.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
