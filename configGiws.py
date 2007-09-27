#!/usr/bin/python -u 

""" Configuration of the Env """

class configGiws:
	__version=0.1
	__descriptionFile="template.xml"
	__splitPerObject=False
	__output="." # Should be changed elsewhere
	__headerCPPExtension=".hxx"
	__bodyCPPExtension=".cxx"

	def setDescriptionFile(self, desc):
		self.__descriptionFile=desc
		
	def getDescriptionFile(self):
		return self.__descriptionFile

	def setSplitPerObject(self, split):
		self.__splitPerObject=split
		
	def getSplitPerObject(self):
		return self.__splitPerObject

	def setOutput(self, output):
		self.__output=output
		
	def getOutput(self):
		return self.__output

	def setCPPHeaderExtension(self, ext):
		self.__headerCPPExtension=ext
		
	def getCPPHeaderExtension(self):
		return self.__headerCPPExtension

	def setCPPBodyExtension(self, ext):
		self.__bodyCPPExtension=ext
		
	def getCPPBodyExtension(self):
		return self.__bodyCPPExtension

	def getVersion(self):
		return self.__version
