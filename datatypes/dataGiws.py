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

	def getJavaTypeSyntax(self, ForceNotArray=False):
		""" Returns the Java type syntax of a data with the Array type
		when applies
		"""
		if self.isArray() and not ForceNotArray:
			return self.type+"Array"
		else:
			return self.type
		
	def getJavaTypeSyntaxForceNotArray(self):
		""" Return the java type any time""" 
		return self.getJavaTypeSyntax(ForceNotArray=True)
		
	def getJavaShortType(self, forceNotArray=False):
		if forceNotArray:
			type=self.getJavaTypeSyntaxForceNotArray()
		else:
			type=self.getJavaTypeSyntax()
		# removes the leading j and put the first char uppercase
		return type[1].upper()+type[2:]

	def getJavaShortTypeForceNotArray(self):
		return self.getJavaShortType(forceNotArray=True)


	def getNativeType(self, ForceNotArray=False):
		""" Returns the native type (C/C++)
		"""
		if self.isArray() and not ForceNotArray:
			return self.nativeType+" *"
		else:
			return self.nativeType

	def getNativeTypeForceNotArray(self):
		return self.getNativeType(ForceNotArray=True)

	
	def getTypeSignature(self):
		""" Returns the java type signature
		"""
		if self.isArray():
			return "["+self.__signature
		else:
			return self.__signature

	def getCallMethod(self):
		""" Returns the JNI method call
		"""
		if self.isArray():
			return "CallObjectMethod"
		else:
			return self.callMethod
		
	def getRealJavaType(self):
		""" Returns the real datatype 
		"""
		abstractMethod(self)

	def getDescription(self):
		""" Returns the description
		"""
		abstractMethod(self)

		
		
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
		javaType=self.getJavaTypeSyntaxForceNotArray()
		
		# removes the leading j and put the first char uppercase
		shortType=self.getJavaShortTypeForceNotArray()

		# Yep, it seems ugly to have that much varName but it is normal.
		return """
		%sArray %s_ = curEnv->New%sArray( %sSize ) ;
		curEnv->Set%sArrayRegion( %s_, 0, %sSize, (%s*) %s ) ;
		"""%(javaType, varName, shortType, varName, shortType, varName, varName, javaType, varName) 

	def specificPreProcessing(self, parameter):
		""" Preprocessing before calling the java method
		"""
		if self.isArray():
			return self.getProfileCreationOfTheArray(parameter.getName())
		else:
			return None
		
	def specificPostProcessing(self):
		""" Preprocessing after calling the java method
		"""

		javaType=self.getJavaTypeSyntax()
		javaTypeNotArray=self.getJavaTypeSyntaxForceNotArray()
		shortType=self.getJavaShortType(forceNotArray=True)
		nativeTypeForceNotArray=self.getNativeTypeForceNotArray()
		
		if self.isArray():
			return """
			jsize len = curEnv->GetArrayLength(res);
			jboolean isCopy = JNI_FALSE;

			/* faster than getXXXArrayElements */
			%s *resultsArray = (%s *) curEnv->GetPrimitiveArrayCritical(res, &isCopy);
			%s myArray= new %s[len];

			for (jsize i = 0; i < len; i++){
			myArray[i]=resultsArray[i];
			}
			curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);
			"""%(javaTypeNotArray, javaTypeNotArray, self.getNativeType(), nativeTypeForceNotArray)
		else:
			# Not post processing when dealing with primitive types
			return ""

	def getReturnSyntax(self):
		
		if self.isArray():
			return """
			return myArray;
			"""
		else:
			return """
			return res;
			"""
