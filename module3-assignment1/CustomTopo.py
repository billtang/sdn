#!/usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        core = self.addSwitch('c1')
        edgecount = 1
        hostcount = 1
        for j in irange(1, fanout):
            agg = self.addSwitch('a%s' % j)
            self.addLink(core, agg, **linkopts1)
            print "core to agg ", j
            for k in irange(1, fanout):
                
                edge = self.addSwitch('e%s' % edgecount)
                edgecount += 1
                self.addLink(agg, edge, **linkopts2)
                print "agg to edge ", k
                for m in irange(1, fanout):
                    print "edge to host ", k
                    host = self.addHost('h%s' % hostcount )
                    hostcount += 1
                    self.addLink(edge, host, **linkopts3)



def output():
  """Uses the student code to compute the output for test cases."""

  "Set up link parameters"
  print "a. Setting link parameters"
  "--- core to aggregation switches"
  linkopts1 = {'bw':50, 'delay':'5ms'}
  "--- aggregation to edge switches"
  linkopts2 = {'bw':30, 'delay':'10ms'}
  "--- edge switches to hosts"
  linkopts3 = {'bw':10, 'delay':'15ms'}
  
  "Creating network and run simple performance test"
  print "b. Creating Custom Topology"
  topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=3)

  print "c. Firing up Mininet"
  net = Mininet(topo=topo, link=TCLink)
  net.start()
  h1 = net.get('h1')
  h27 = net.get('h27')
  
  print "d. Starting Test"

  # Start pings
  outputString = h1.cmd('ping', '-c6', h27.IP())
  print outputString.strip()
    
  print "e. Stopping Mininet"
  net.stop()
    

def simpleTest():
    "Create and test a simple network"

    linkopts1 = dict(bw=15, delay='1ms')
    linkopts2 = dict(bw=15, delay='1ms')
    linkopts3 = dict(bw=15, delay='1ms')


    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
    net = Mininet(topo, link = TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    #output()
    simpleTest()

topos = { 'custom': ( lambda: CustomTopo() ) }
                    
