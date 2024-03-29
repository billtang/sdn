'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 7 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.examples.load_balancer import *
from pprint import pprint

class ResonancePolicy():

  state_policy_map = {}

  def __init__(self):
    self.state_policy_map['default'] = self.default_policy

  def get_policy(self, state):
    if self.state_policy_map.has_key(state):
      return self.state_policy_map[state]
    else:
      return self.default_policy
    
  """ Default state policy """
  def default_policy(self): return drop

class LBPolicy(ResonancePolicy):
  def __init__(self, fsm):
    self.fsm = fsm

  def portA_policy(self):                       
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.2')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.2] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.2] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)
    
  def portB_policy(self):
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.3')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.3] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.3] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)

# --------- Update the code below ------------

  def default_policy(self):
    # Add the logic to return the right policy (i.e., portA_policy or portB_policy 
    # based on the state of the FSMs)
    #return self.portA_policy()
    portA_hosts = self.fsm.get_portA_hosts()
    portB_hosts = self.fsm.get_portB_hosts()
    print "myAs: " + str(portA_hosts)
    print "myBs: " + str(portB_hosts)
    isNone = False
    if ( len(portA_hosts) == 0 and len(portB_hosts) == 0 ): isNone = True
    isA = parallel([match(dstip=portA_host) for portA_host in portA_hosts])
    isB = parallel([match(dstip=portB_host) for portB_host in portB_hosts])

    if isNone:
      print "isNone"
      return self.portB_policy()
    if isA:
      print "isA"
      return self.portA_policy()
    if isB:
      print "isB"
      return self.portB_policy()
    return drop





