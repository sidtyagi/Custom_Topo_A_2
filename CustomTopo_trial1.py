#!/usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.log import setLogLevel
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
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add your logic here ...
        # adding the agg core layer
        self.fanout = fanout

        core_switch_list=[]
        agg_switch_list=[]
        edge_switch_list=[]
        host_list=[]

        #----Push the core switch---#
        c_switch = self.addSwitch('c%s' % 1)
	print '---Core switch Pushed---'
        core_switch_list.append(c_switch)
        #---core switch pushed---#
        #----Now pushing the agg switch list---#
        lastSwitch = None
        for i in range(0, fanout):
           #host = self.addHost('h%s' % i, cpu=.5/k)
           agg_switch = self.addSwitch('a%s' % i)
           agg_switch_list.append(agg_switch)
           #self.addLink( c_switch, agg_switch, bw=10, delay='5ms', loss=1, max_queue_size=1000,  use_htb=True)
	   print '-------------Adding link between '+c_switch+' and '+agg_switch+'------------'
           self.addLink( c_switch, agg_switch,**linkopts1)
	   '''for k in range(0,fanout):
				host = self.addHost('h%s' % i)
				print '----For switch '+agg_switch+' adding host--'+host'''
	#-------for every agg switch create edge switches (no. equals fanout value)--------#
	#sw_no=0
	for agg_switch in agg_switch_list:
		#sw_no=0
		for j in range(0,fanout):
		#for j in range(sw_no,fanout)
			
			edge_switch=self.addSwitch(agg_switch+'_'+'e%s' % j)
			self.addLink( agg_switch, edge_switch,**linkopts2)
			print '---------Added link between---'+edge_switch+' and '+agg_switch
			edge_switch_list.append(edge_switch)
	#for agg_switch in agg_switch_list:
	print edge_switch_list
		



	#---For every switch in edge_switch_list create a host list with 2(where 2 is fanout val) hosts per edge switch---#
	for edge_switch in edge_switch_list:
		for m in range(0,fanout):
			host = self.addHost(edge_switch+'_'+'h%s' % m)
			self.addLink( edge_switch, host,**linkopts3)
			print '---------Added link between---'+host+' and '+edge_switch
			host_list.append(host)
	print '--------------FINAL TOPOLOGY ELEMENTS----------------'
	print '-----------CORE SWITCH LIST--------------------------'
	print core_switch_list
	print '\n\n\n'
	print '------------AGG_SWITCH_LIST--------------------------'
	print agg_switch_list
	print '\n\n\n'
	print '------------EDGE_SWITCH_LIST-------------------------'
	print edge_switch_list
	print '\n\n\n'
	print '------------HOST LIST--------------------------------'
	print host_list
           

topos = { 'custom': ( lambda: CustomTopo() ) }

if __name__ == '__main__':
   setLogLevel('info')
   def simpleTest():
              linkopts1 = {'bw':50, 'delay':'5ms'}
              linkopts2 = {'bw':30, 'delay':'10ms'}
              linkopts3 = {'bw':10, 'delay':'15ms'}
              topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
              net = Mininet(topo=topo, link=TCLink)
              net.start()
              net.pingAll()
              print net.hosts
              print net.switches
              net.stop
   simpleTest()


