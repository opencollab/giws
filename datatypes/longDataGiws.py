#!/usr/bin/python -u
from dataGiws import dataGiws

class longDataGiws(dataGiws):
	"""
	Manages Java datatype long
	"""
	type="jlong"
	def getTypeSignature(self):
		return "J"

	def getRealJavaType(self):
		return "long"

	def getDescription(self):
		return "signed 64 bits"

	def getNativeType(self):
		return super(longDataGiws, self).getNativeType("long long")
	
	def CallMethod(self):
		return "CallLongMethod"

if __name__ == '__main__':
	longDataGiws().getReturnTypeSyntax()

