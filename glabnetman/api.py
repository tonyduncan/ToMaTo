# -*- coding: utf-8 -*-

from host_store import *
from host import *
from topology_store import *
from topology import *

class TopologyInfo():
	def __init__(self, topology):
		self.id = topology.id
		self.state = str(topology.state)

class HostInfo():
	def __init__(self, host):
		self.name = host.name

class PublicAPI():
	def __init__(self):
		pass
	
	def top_info(self, id):
		return TopologyInfo(TopologyStore.get(id))

	def top_list(self, filter_owner=None, filter_state=None):
		tops=[]
		for t in TopologyStore.topologies.values():
			if filter_state==None or t.state==filter_state:
				tops.append(TopologyInfo(t))
		return tops
	
	def top_import(self, xml):
		dom=minidom.parseString(xml)
		id=TopologyStore.add(Topology(dom,False))
		return id
	
	def top_remove(self, top_id):
		TopologyStore.remove(top_id)
	
	def top_create(self, top_id):
		TopologyStore.get(top_id).create()
	
	def top_destroy(self, top_id):
		TopologyStore.get(top_id).destroy()
	
	def top_deploy(self, top_id):
		TopologyStore.get(top_id).deploy()
	
	def top_start(self, top_id):
		TopologyStore.get(top_id).start()
	
	def top_stop(self, top_id):
		TopologyStore.get(top_id).stop()
	
	def top_get(self, top_id, include_ids=False):
		top=TopologyStore.get(top_id)
		dom=top.create_dom(include_ids)
		return dom.toprettyxml(indent="\t", newl="\n")
		
	def host_list(self):
		hosts=[]
		for h in HostStore.hosts.values():
			hosts.append(HostInfo(h))
		return hosts

	def host_add(self, host_name):
		host=Host(host_name)
		host.check()
		HostStore.add(host)

	def host_remove(self, host_name):
		HostStore.remove(host_name)