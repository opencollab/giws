#!/usr/bin/python -u
from dataGiws import dataGiws

class longDataGiws(dataGiws):
	"""
	Manages Java datatype long
	"""
	
	type="jlong"
	nativeType="long long"
	callMethod="CallLongMethod"
	
	def getTypeSignature(self):
		return "J"

	def getRealJavaType(self):
		return "long"

	def getDescription(self):
		return "signed 64 bits"

if __name__ == '__main__':
	longDataGiws().getReturnTypeSyntax()

