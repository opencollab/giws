#!/usr/bin/python -u 
import sys, pprint
import libxml2
from classRepresentation.packageGiws import packageGiws
from classRepresentation.objectGiws import objectGiws
from classRepresentation.methodGiws import methodGiws
from classRepresentation.parameterGiws import parameterGiws
from classRepresentation.returnDataGiws import returnDataGiws
from datatypes.dataFactoryGiws import dataFactoryGiws

libxml2.debugMemory(1)

class parseXMLEngine:
	__ctxt=None
	Jpackage=None
	
	def __init__(self, descFile):
		try: 
			doc = libxml2.parseFile(descFile)
		except libxml2.parserError:
			print ('Error while parsing XML file "%s"'%descFile)
			sys.exit
		self.__ctxt = doc.xpathNewContext()
		self.__loadPackage()
		doc.freeDoc()

	def getJpackage(self):
		return self.Jpackage
		
	def __loadPackage(self):
		objectNode = self.__ctxt.xpathEval("//package")
		propPackage=objectNode[0].properties
		while propPackage is not None:
			if propPackage.name=="name":
				packageName=propPackage.getContent()
				propPackage = propPackage.next
		self.Jpackage=packageGiws(packageName)
		self.__loadObject()
#		self.__ctxt.xpathFreeContext()

	def __loadObject(self):
		objectsNode = self.__ctxt.xpathEval("//package/object")
		for objectNode in objectsNode:
			propObj=objectNode.properties
			# look for the name of the object
			while propObj is not None:
				if propObj.name=="name":
					objectName=propObj.getContent()
					propObj = propObj.next
			# creates the object
			newObject=objectGiws(objectName)

			# Load the methods
			methods=objectNode.children
			while methods is not None:
				if methods.type == "element":
					newObject.addMethod(self.__loadMethods(methods))
				methods = methods.next

			# Add to the package the object found
			self.Jpackage.addObject(newObject)
		self.__ctxt.xpathFreeContext()

	def __loadMethods(self, method):
		# @TODO : check the order

		returns=method.properties.next.getContent()
		myFactory=dataFactoryGiws()
		myReturnData=myFactory.create(returns)
		
		
		Jmethod=methodGiws(method.properties.getContent(),myReturnData)
		child = method.children
		while child is not None: # We browse the parameters of the method
			if child.type == "element":
				prop=child.properties
				Jmethod.addParameter(self.__loadParameter(prop))
			child = child.next
		return Jmethod


	def __loadParameter(self,prop):
		while prop is not None:
			if prop.name=="type":
				type=prop.getContent()
			if prop.name=="name":
				name=prop.getContent()
			prop = prop.next
		return parameterGiws(name,type)
						

if __name__ == '__main__':
	print "Parsing ..."
	templateObj=parseXMLEngine("template.xml")
	print templateObj.getJpackage().generateCXXHeader()
	print templateObj.getJpackage()
