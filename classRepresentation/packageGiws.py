#!/usr/bin/python -u
from objectGiws import objectGiws

class packageGiws:
	__name=""
	__objects=[]
	
	def __init__(self, name):
		self.__name=name
		self.__objects=[]

	def getName(self):
		return self.__name
	
	def getNameForCXX(self):
		return self.__name.replace('.','_')
	
	def getNameForJNI(self):
		return self.__name.replace('.','/')
	
	def getObjects(self):
		return self.__objects

	def addObject(self, object):
		if isinstance(object,objectGiws):
			self.__objects.append(object)
