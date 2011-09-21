#!/usr/bin/python -u
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
# 
# This software is a computer program whose purpose is to generate C++ wrapper 
# for Java objects/methods.
# 
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# 
# For more information, see the file COPYING

import sys, pprint
import libxml2
import os.path

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
		if os.path.isfile(descFile)!=True:
			print ('Could not find declaration file "%s"'%descFile)
			sys.exit(-2)
		try:
			doc = libxml2.parseFile(descFile)
		except libxml2.parserError:
			print ('Error while parsing XML file "%s"'%descFile)
			sys.exit(-3)
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
			extendsObject=None
			propObj=objectNode.properties
			# look for the name of the object
			while propObj is not None:
				if propObj.name=="name":
					objectName=propObj.getContent()
				if propObj.name=="extends":
					extends=propObj.getContent()
					# Retrieve the father (inheritance)
					extendsObject=self.Jpackage.getObject(extends)
					if extendsObject==None:
						print ('Class "%s" must be defined before being use as father class.\nPlease check that "%s" is defined before "%s".'%(extends, extends, objectName))
						sys.exit(-4)
				propObj = propObj.next

			# creates the object
			newObject=objectGiws(objectName,extendsObject)

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
		returns=method.prop("returnType")
		myFactory=dataFactoryGiws()
		myReturnData=myFactory.create(returns)

		modifier=method.prop("modifier")
		detachThreadProp=method.prop("detachThread")
		detachThread=False
		if detachThreadProp!=None:
			str=detachThreadProp.lower()
			if str=="true":
				detachThread=True

		if modifier!=None:
			Jmethod=methodGiws(method.properties.getContent(),myReturnData,detachThread,modifier)
		else:
			Jmethod=methodGiws(method.properties.getContent(),myReturnData,detachThread)
		child = method.children
		parametersName=[] # To check if the parameter is not already defined
		while child is not None: # We browse the parameters of the method
			if child.type == "element":
				prop=child.properties
				param=self.__loadParameter(prop)
				try:
					if parametersName.index(param.getName()) >= 0:
						print ('%s is already defined as parameters'%param.getName())
						sys.exit(-3)					
				except ValueError: #Cannot find the parameter => not defined. Good!
	   				parametersName.append(param.getName())

				Jmethod.addParameter(param)

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
