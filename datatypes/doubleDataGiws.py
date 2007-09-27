#!/usr/bin/python -u

from dataGiws import dataGiws

class doubleDataGiws(dataGiws):
	"""
	Manages Java datatype double
	"""
			
	def getTypeSignature(self):
		return "D"

	def getJavaTypeSyntax(self):
		return "jdouble"

	def getRealJavaType(self):
		return "double"

	def getDescription(self):
		return "64 bits"

	def getNativeType(self):
		return super(doubleDataGiws, self).getNativeType("double")

	def CallMethod(self):
		return "CallDoubleMethod"
	
