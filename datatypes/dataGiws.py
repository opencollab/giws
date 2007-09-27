#!/usr/bin/python -u
import sys


def abstractMethod(obj=None):
    """ Use this instead of 'pass' for the body of abstract methods. """
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))

#
# This class intend to create a generic object for datatype
# see http://en.wikipedia.org/wiki/Java_Native_Interface#Mapping_types
class dataGiws(object):
	__isArray=False
	"""
	Interface for the datatype mapping
	"""

	def getJavaTypeSyntax(self, javaTypeSyntax):
		""" Returns the Java type syntax of a data
		"""
		if self.isArray():
			return javaTypeSyntax+"Array"
		else:
			return javaTypeSyntax
		
	def getTypeSignature(self):
		""" Returns the java type signature
		"""
		if self.isArray():
			return "["+self.__signature
		return self.__signature
		
	def getRealJavaType(self):
		""" Returns the real datatype 
		"""
		abstractMethod(self)

	def getDescription(self):
		""" Returns the description
		"""
		abstractMethod(self)

	def getNativeType(self, nativeType):
		""" Returns the native type (C/C++)
		"""
		if self.isArray():
			return nativeType+" *"
		else:
			return nativeType
		
		
	def setIsArray(self, isItAnArray):
		""" Defines if we have to deal with an array or not
		"""
		self.__isArray=isItAnArray

	def isArray(self):
		""" return if we have to deal with an array or not
		"""
		return self.__isArray

	def getProfileCreationOfTheArray(self, varName):
		"""
		When we deal with an array as input, we need to 'transform' it for
		Java"""
		javaType=self.getJavaTypeSyntax()
		
		# removes the leading j and put the first char uppercase
		shortType=javaType[1].upper()+javaType[2:]
		
		# Yep, it seems ugly to have that much varName but it is normal.
		return """
		%sArray %s_ = curEnv->New%sArray( %sSize ) ;
		curEnv->Set%sArrayRegion( %s_, 0, %sSize, (%s*) %s ) ;
		"""%(javaType, varName, shortType, varName, shortType, varName, varName, javaType, varName) 

	def specificPreProcessing(self, parameter):
		## Preprocessing before calling the java method
		if self.isArray():
			return self.getProfileCreationOfTheArray(parameter.getName())
		else:
			return None
