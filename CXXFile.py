#!/usr/bin/python -u
from classRepresentation.packageGiws import packageGiws
from outputWriter import outputWriter
from JNIFrameWork import JNIFrameWork
from licenseWrapper import licenseWrapper

""" Engine to create the C++ files """


class CXXFile:
	
	package=None
	
	def __init__(self, package):
		if isinstance(package,packageGiws):
			self.package=package
		else:
			raise Exception("The type must be a packageGiws object")

	
	def getFileNameForObjectDeclaration(self, config, typeFile, object):
		fileName=object.getName()
		if typeFile=="header":
			fileName+=config.getCPPHeaderExtension()
		else:
			fileName+=config.getCPPBodyExtension()
		return fileName
	
	def getFileNameForPackageDeclaration(self, config, typeFile):
		fileName=self.package.getNameForCXX()
		if typeFile=="header":
			fileName+=config.getCPPHeaderExtension()
		else:
			fileName+=config.getCPPBodyExtension()
		return fileName

	def getObjectCXX(self, type="header"):
		i=1
		str=""
		for object in self.package.getObjects():
			if type=="header":
				str=str+object.generateCXXHeader()
			else:
				str=str+object.generateCXXBody(self.package.getNameForJNI())
			if len(self.package.getObjects())!=i:
				str+="""
				"""
			i=i+1
		return str


	def generateCXXHeader(self,config):
		strCommon="""
		%s
		namespace %s {
		""" % (JNIFrameWork().getHeader(),self.package.getNameForCXX())

		strCommonEnd="""
		}
		"""
		str=""
		if config.getSplitPerObject()==True:
			for object in self.package.getObjects():
				fileName=self.getFileNameForObjectDeclaration(config, "header",object)
				str=licenseWrapper().getLicense()+strCommon+object.generateCXXHeader()+strCommonEnd
				outputWriter().writeIntoFile(config.getOutput(), fileName, str)
				print "%s generated ..."%fileName
		else:
			fileName=self.getFileNameForPackageDeclaration(config, "header")
			str="""%s
			%s
			%s
			""" % (strCommon, self.getObjectCXX("header"), strCommonEnd)
			
			outputWriter().writeIntoFile(config.getOutput(),fileName, str)
			print "%s generated ..."%fileName

	def generateCXXBody(self,config):
		strCommon="""
		%s
		namespace %s {
		"""%(JNIFrameWork().getHeader(), self.package.getNameForCXX())
		
		strCommonEnd="""
		}
		"""
		
		str=""
		
		if config.getSplitPerObject()==True:
			for object in self.package.getObjects():
				strInclude="""#include "%s"
				"""%(self.getFileNameForObjectDeclaration(config, "header",object))
				
				fileName=self.getFileNameForObjectDeclaration(config, "body",object)
				str=licenseWrapper().getLicense()+strInclude+strCommon+object.generateCXXBody(self.package.getNameForJNI())+strCommonEnd
				outputWriter().writeIntoFile(config.getOutput(),fileName, str)
				print "%s generated ..."%fileName
		else:
			strInclude="""#include "%s"
			"""%(self.getFileNameForPackageDeclaration(config, "header"))
			fileName=self.getFileNameForPackageDeclaration(config, "body")
			str="""%s
			%s
			%s
			%s
			""" % (strInclude, strCommon, self.getObjectCXX("body"), strCommonEnd)
			outputWriter().writeIntoFile(config.getOutput(),fileName, str)
			print "%s generated ..."%fileName

