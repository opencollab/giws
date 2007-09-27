#!/usr/bin/python -u
from dataGiws import dataGiws

class longDataGiws(dataGiws):
	"""
	Manages Java datatype long
	"""
	def getTypeSignature(self):
		return "J"

	def getJavaTypeSyntax(self):
		return "jlong"

	def getRealJavaType(self):
		return "long"

	def getDescription(self):
		return "signed 64 bits"

	def getNativeType(self):
		return "long long"
	
	def CallMethod(self):
		return "CallLongMethod"

if __name__ == '__main__':
	longDataGiws().getReturnTypeSyntax()

