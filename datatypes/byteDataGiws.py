#!/usr/bin/python -u

from dataGiws import dataGiws

class byteDataGiws(dataGiws):

	type="jbyte"
	nativeType="byte"
	
	def getTypeSignature(self):
		return "B"

	def getRealJavaType(self):
		return "byte"
	
	def getDescription(self):
		return "signed 8 bits"
	
	def CallMethod(self):
		return "CallByteMethod"

if __name__ == '__main__':
	print byteDataGiws().getReturnTypeSyntax()

