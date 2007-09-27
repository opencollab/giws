#!/usr/bin/python -u

from dataGiws import dataGiws

class voidDataGiws(dataGiws):

	nativeType="void"	

	def getTypeSignature(self):
		return "V"

	def getJavaTypeSyntax(self):
		return "void"

	def getJavaTypeSyntaxForceNotArray(self):
		return self.getJavaTypeSyntax()
	
	def getDescription(self):
		return "void type"

 	def getReturnSyntax(self):
		return ""
	
	def CallMethod(self):
		return "CallVoidMethod"

if __name__ == '__main__':
	print voidDataGiws().getReturnTypeSyntax()

