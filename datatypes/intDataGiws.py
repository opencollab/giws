#!/usr/bin/python -u

from dataGiws import dataGiws

class intDataGiws(dataGiws):
	"""
	Manages Java datatype int
	"""
	type="jint"
	
	def getTypeSignature(self):
		return "I"

	def getRealJavaType(self):
		return "int"
		
	def getDescription(self):
		return "signed 32 bits"

	def getNativeType(self):
		return super(intDataGiws, self).getNativeType("long")
	
	def CallMethod(self):
		return "CallIntMethod"
			
if __name__ == '__main__':
	print intDataGiws().getReturnTypeSyntax()

