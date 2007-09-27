#!/usr/bin/python -u


def abstractMethod(obj=None):
    """ Use this instead of 'pass' for the body of abstract methods. """
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))

#
# This class intend to create a generic object for datatype
# see http://en.wikipedia.org/wiki/Java_Native_Interface#Mapping_types
class dataGiws:
	__isArray=False
	"""
	Interface for the datatype mapping
	"""
	def getJavaTypeSyntax(self):
		""" Returns the Java type syntax of a data
		"""
		abstractMethod(self)
		
	def getTypeSignature(self):
		""" Returns the java type signature
		"""
		if self.getIsArray():
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

	def getNativeType(self):
		""" Returns the native type (C/C++)
		"""
		abstractMethod(self)

	def setIsArray(self, isItAnArray):
		""" Defines if we have to deal with an array or not
		"""
		self.__isArray=isItAnArray

	def getIsArray(self):
		""" return if we have to deal with an array or not
		"""
		return self.__isArray

