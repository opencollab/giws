#!/usr/bin/python -u

from dataGiws import dataGiws

class doubleDataGiws(dataGiws):
	"""
	Manages Java datatype double
	"""

	type="jdouble"
	nativeType="double"
	callMethod="CallDoubleMethod"
	
	def getTypeSignature(self):
		return "D"

	def getRealJavaType(self):
		return "double"

	def getDescription(self):
		return "64 bits"
	
