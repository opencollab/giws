#!/usr/bin/python -u

from dataGiws import dataGiws

class floatDataGiws(dataGiws):

	type="jfloat"
	nativeType="float"
	
	def getTypeSignature(self):
		return "F"

	def getRealJavaType(self):
		return "float"
	
	def getDescription(self):
		return "unsigned 8 bits"
	
	def CallMethod(self):
		return "CallFloatMethod"

if __name__ == '__main__':
	print floatDataGiws().getReturnTypeSyntax()

