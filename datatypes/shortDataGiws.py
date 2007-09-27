#!/usr/bin/python -u

from dataGiws import dataGiws

class shortDataGiws(dataGiws):

	type="jshort"
	nativeType="short"
	
	def getTypeSignature(self):
		return "S"

	def getRealJavaType(self):
		return "short"
	
	def getDescription(self):
		return "signed 16 bits"

	def CallMethod(self):
		return "CallShortMethod"

if __name__ == '__main__':
	print shortDataGiws().getReturnTypeSyntax()

