#!/usr/bin/python -u

from dataGiws import dataGiws

class shortDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "S"

	def getJavaTypeSyntax(self):
		return "jshort"

	def getRealJavaType(self):
		return "short"
	
	def getDescription(self):
		return "signed 16 bits"

	def getNativeType(self):
		return "short"
	
	def CallMethod(self):
		return "CallShortMethod"

if __name__ == '__main__':
	print shortDataGiws().getReturnTypeSyntax()

