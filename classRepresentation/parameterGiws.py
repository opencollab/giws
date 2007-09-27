#!/usr/bin/python -u
from datatypes.dataGiws import dataGiws
from datatypes.dataFactoryGiws import dataFactoryGiws

class parameterGiws(dataGiws):
	__name=""
	__type=""

	def __init__(self, name, type):

		myDataFactory=dataFactoryGiws()
		self.__type=myDataFactory.create(type)
		self.__name=name
		
#		if isinstance(type,dataGiws):
#			self.__type=type
#		else:
#		raise Exception("The type must be a dataGiws object")

	def getName(self):
		return self.__name

	def getType(self):
		return self.__type
	
	def __str__(self):
		return """%s %s, """ % (self.getType().getNativeType(), self.getName())
	
	def generateCXXHeader(self):
		""" Generate the profil of the parameter """
		str="""%s %s""" % (self.getType().getNativeType(), self.getName())
		if self.getType().isArray():
			str+=", int %sSize"%self.getName()
		return str
