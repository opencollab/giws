#!/usr/bin/python -u
from datatypes.dataGiws import dataGiws
from datatypes.dataFactoryGiws import dataFactoryGiws

class returnDataGiws(dataGiws):
	__name=""
	__type=""

	def __init__(self, type):
		myDataFactory=dataFactoryGiws()
		self.__type=myDataFactory.create(type)

	def getType(self):
		return self.__type
	
	def __str__(self):
		return """%s """ % (self.getType().getNativeType())
	
	def generateCXXHeader(self):
		return """%s""" % (self.getType().getNativeType())
