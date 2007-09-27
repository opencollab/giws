#!/usr/bin/python -u
from dataGiws import dataGiws

class longDataGiws(dataGiws):
	"""
	Manages Java datatype long
	"""
	
	type="jlong"
	nativeType="long long"
	
	def getTypeSignature(self):
		return "J"

	def getRealJavaType(self):
		return "long"

	def getDescription(self):
		return "signed 64 bits"
	
	def CallMethod(self):
		return "CallLongMethod"

if __name__ == '__main__':
	longDataGiws().getReturnTypeSyntax()

