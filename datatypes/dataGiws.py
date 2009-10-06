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

import sys
from configGiws import configGiws
from JNIFrameWork import JNIFrameWork

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
		
	def getCallStaticMethod(self):
		""" Returns the JNI static method call
		"""
		if self.isArray():
			return "CallObjectMethod"
		else:
			return self.callStaticMethod
		
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


	def __getProfileCreationOfTheArray(self, varName):
		"""
		When we deal with an array as input, we need to 'transform' it for
		Java"""
		javaType=self.getJavaTypeSyntaxForceNotArray()
		
		# removes the leading j and put the first char uppercase
		shortType=self.getJavaShortTypeForceNotArray()

		if configGiws().getThrowsException():
			errorMgnt="""
			if (%s_ == NULL)
			{
			// check that allocation succeed
			throw %s::JniBadAllocException(curEnv);
			}
			"""%(varName,configGiws().getExceptionFileName())
		else:
			errorMgnt=""
  
		# Yep, it seems ugly to have that much varName but it is normal.
		return """
		%sArray %s_ = curEnv->New%sArray( %sSize ) ;
		%s
		curEnv->Set%sArrayRegion( %s_, 0, %sSize, (%s*) %s ) ;

		"""%(javaType, varName, shortType, varName, errorMgnt, shortType, varName, varName, javaType, varName) 

	def specificPreProcessing(self, parameter):
		""" Preprocessing before calling the java method
		"""
		if self.isArray():
			return self.__getProfileCreationOfTheArray(parameter.getName())
		else:
			return None


	def specificPostDeleteMemory(self, parameter):
		""" Preprocessing before calling the java method
		"""
		return """curEnv->DeleteLocalRef(%s_);
		"""%(parameter.getName())
		
		
	def specificPostProcessing(self):
		""" Preprocessing after calling the java method
		"""

		javaType=self.getJavaTypeSyntax()
		javaTypeNotArray=self.getJavaTypeSyntaxForceNotArray()
		shortType=self.getJavaShortType(forceNotArray=True)
		nativeTypeForceNotArray=self.getNativeTypeForceNotArray()
		
		if self.isArray():
			str=JNIFrameWork().getExceptionCheckProfile()
			return str+"""
			jsize len = curEnv->GetArrayLength(res);
			jboolean isCopy = JNI_FALSE;

			/* faster than getXXXArrayElements */
			%s *resultsArray = (%s *) curEnv->GetPrimitiveArrayCritical(res, &isCopy);
			%s myArray= new %s[len];

			for (jsize i = 0; i < len; i++){
			myArray[i]=resultsArray[i];
			}
			curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);

                        curEnv->DeleteLocalRef(res);
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
