#!/usr/bin/python -u

from dataGiws import dataGiws

class booleanDataGiws(dataGiws):

	type="jboolean"

	def getTypeSignature(self):
		return "Z"

	def getRealJavaType(self):
		return "boolean"
	
	def getDescription(self):
		return "unsigned 8 bits"

	def getNativeType(self):
		return super(booleanDataGiws, self).getNativeType("bool")
	
	def CallMethod(self):
		return "CallBooleanMethod"

if __name__ == '__main__':
	print booleanDataGiws().getReturnTypeSyntax()

