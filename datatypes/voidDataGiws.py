#!/usr/bin/python -u

from dataGiws import dataGiws

class voidDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "V"

	def getJavaTypeSyntax(self):
		return "void"

	def getDescription(self):
		return "void type"

	def getNativeType(self):
		return "void"

 	def specificReturn(self):
		return ""
	
	def CallMethod(self):
		return "CallVoidMethod"

if __name__ == '__main__':
	print voidDataGiws().getReturnTypeSyntax()

