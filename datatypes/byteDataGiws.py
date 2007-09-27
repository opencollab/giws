#!/usr/bin/python -u

from dataGiws import dataGiws

class byteDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "B"

	def getJavaTypeSyntax(self):
		return "jbyte"

	def getRealJavaType(self):
		return "byte"
	
	def getDescription(self):
		return "signed 8 bits"

	def getNativeType(self):
		return "byte"
	
	def CallMethod(self):
		return "CallByteMethod"

if __name__ == '__main__':
	print byteDataGiws().getReturnTypeSyntax()

