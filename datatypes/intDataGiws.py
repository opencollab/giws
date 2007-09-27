#!/usr/bin/python -u

from dataGiws import dataGiws

class intDataGiws(dataGiws):
	"""
	Manages Java datatype int
	"""
	type="jint"
	nativeType="long"
	callMethod="CallIntMethod"

	def getTypeSignature(self):
		return "I"

	def getRealJavaType(self):
		return "int"
		
	def getDescription(self):
		return "signed 32 bits"
			
if __name__ == '__main__':
	print intDataGiws().getReturnTypeSyntax()

