#!/usr/bin/python -u


def abstractMethod(obj=None):
    """ Use this instead of 'pass' for the body of abstract methods. """
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))

#
# This class intend to create a generic object for datatype
# see http://en.wikipedia.org/wiki/Java_Native_Interface#Mapping_types
class dataGiws:
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
		abstractMethod(self)
		
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

