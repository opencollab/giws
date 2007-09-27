#!/usr/bin/python -u
from datatypes.dataGiws import dataGiws
from datatypes.dataFactoryGiws import dataFactoryGiws

class returnDataGiws(dataGiws):
	__type=""

	def __init__(self, type):
		myDataFactory=dataFactoryGiws()
		self.__type=myDataFactory.create(type)

	def getType(self):
		return self.__type
	
	def generateCXXHeader(self):
		return """%s""" % (self.getType().getNativeType())
