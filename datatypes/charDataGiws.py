#!/usr/bin/python -u

from dataGiws import dataGiws

class charDataGiws(dataGiws):

	nativeType="char"
	
	def getTypeSignature(self):
		return "C"

	def getJavaTypeSyntax(self):
		return "jchar"

	def getRealJavaType(self):
		return "char"
	
	def getDescription(self):
		return "unsigned 16 bits"
	
	def CallMethod(self):
		return "CallCharMethod"

if __name__ == '__main__':
	print charDataGiws().getReturnTypeSyntax()

