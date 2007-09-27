#!/usr/bin/python -u

from dataGiws import dataGiws

class floatDataGiws(dataGiws):

	type="jfloat"
	nativeType="float"
	callMethod="CallFloatMethod"
	
	def getTypeSignature(self):
		return "F"

	def getRealJavaType(self):
		return "float"
	
	def getDescription(self):
		return "unsigned 8 bits"

if __name__ == '__main__':
	print floatDataGiws().getReturnTypeSyntax()

