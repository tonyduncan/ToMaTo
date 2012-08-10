# -*- coding: utf-8 -*-
# ToMaTo (Topology management software) 
# Copyright (C) 2010 Dennis Schwerdel, University of Kaiserslautern
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from django.db import models
from tomato.connections import Connection

from tomato.lib import db, attributes, util
from tomato.lib.decorators import *

TYPES = {}
REMOVE_ACTION = "__remove__"

class Element(db.ChangesetMixin, db.ReloadMixin, attributes.Mixin, models.Model):
	type = models.CharField(max_length=20, validators=[db.nameValidator], choices=[(t, t) for t in TYPES.keys()])
	owner = models.CharField(max_length=20, validators=[db.nameValidator])
	parent = models.ForeignKey('self', null=True, related_name='children')
	connection = models.ForeignKey(Connection, null=True, related_name='elements')
	state = models.CharField(max_length=20, validators=[db.nameValidator])
	attrs = db.JSONField()
	
	CAP_ACTIONS = {}
	CAP_ATTRS = {}
	CAP_CHILDREN = {}
	CAP_PARENT = []
	CAP_CON_PARADIGMS = []
	DEFAULT_ATTRS = {}
	
	class Meta:
		pass

	def init(self, parent=None, attrs={}):
		if parent:
			fault.check(parent.type in self.CAP_PARENT, "Parent type %s not allowed for type %s", (parent.type, self.type))
			fault.check(self.type in parent.CAP_CHILDREN, "Parent type %s does not allow children of type %s", (parent.type, self.type))
			fault.check(parent.state in parent.CAP_CHILDREN[self.type], "Parent type %s does not allow children of type %s in state %s", (parent.type, self.type, parent.state))
		self.parent = parent
		self.owner = currentUser()
		self.attrs = dict(self.DEFAULT_ATTRS)
		self.save()
		self.modify(attrs)
		
	def upcast(self):
		try:
			return getattr(self, self.type)
		except:
			pass
		fault.raise_("Failed to cast element #%d to type %s" % (self.id, self.type))

	def hasParent(self):
		return not self.parent is None

	def checkModify(self, attrs):
		for key in attrs.keys():
			fault.check(key in self.CAP_ATTRS, "Unsuported attribute for %s: %s", (self.type, key))
			fault.check(self.state in self.CAP_ATTRS[key], "Attribute %s of %s can not be changed in state %s", (key, self.type, self.state))
		
	def modify(self, attrs):
		self.checkModify(attrs)
		for key, value in attrs.iteritems():
			getattr(self, "modify_%s" % key)(value)
		self.save()
	
	def checkAction(self, action):
		fault.check(action in self.CAP_ACTIONS, "Unsuported action for %s: %s", (self.type, action))
		fault.check(self.state in self.CAP_ACTIONS[action], "Action %s of %s can not be executed in state %s", (action, self.type, self.state))
	
	def action(self, action, params):
		self.checkAction(action)
		getattr(self, "action_%s" % action)(**params)
		self.save()

	def checkRemove(self, recurse=True):
		fault.check(recurse or self.children.empty(), "Cannot remove element with children")
		fault.check(not REMOVE_ACTION in self.CAP_ACTIONS or self.state in self.CAP_ACTIONS[REMOVE_ACTION], "Element type %s can not be removed in its state %s", (self.type, self.state))
		for ch in self.getChildren():
			ch.checkRemove(recurse=recurse)

	def setState(self, state, recursive=False):
		if recursive:
			for ch in self.getChildren():
				ch.setState(self, state, True)
		self.state = state
		self.save()

	def remove(self, recurse=True):
		self.checkRemove(recurse)
		for ch in self.getChildren():
			ch.remove(recurse=True)
		self.delete()
			
	def getChildren(self):
		return [el.upcast() for el in self.children.all()]
			
	def getConnection(self):
		return self.connection.upcast() if self.connection else None
		
	def onConnected(self):
		pass
	
	def onDisconnected(self):
		pass
			
	def info(self):
		return {
			"id": self.id,
			"type": self.type,
			"parent_id": self.parent.id if self.hasParent() else None,
			"state": self.state,
			"attrs": self.attrs,
			"children": [ch.id for ch in self.getChildren()],
			"connection": self.connection.id if self.connection else None,
		}
		
def get(id_, **kwargs):
	try:
		el = Element.objects.get(id=id_, **kwargs)
		return el.upcast()
	except Element.DoesNotExist:
		return None

def getAll(**kwargs):
	return (el.upcast() for el in Element.objects.filter(**kwargs))

def create(type_, parent=None, attrs={}):
	fault.check(type_ in TYPES, "Unsupported type: %s", type_)
	el = TYPES[type_]()
	el.init(parent, attrs)
	return el

from tomato import fault, currentUser