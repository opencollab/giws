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
	__dimensionArray=0
	temporaryVariableName="myArray"
	"""
	Interface for the datatype mapping
	"""

	def isByteBufferBased(self):
		return False

	def getJavaTypeSyntax(self, ForceNotArray=False):
		""" Returns the Java type syntax of a data with the Array type
		when applies
		"""
		if self.isArray() and not ForceNotArray:
                    if self.getDimensionArray() == 1:
                        return self.type+"Array"
                    else:
                        return "jobjectArray"
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


	def getNativeType(self, ForceNotArray=False, UseConst=False):
		""" Returns the native type (C/C++)
		"""
		if self.isArray() and not ForceNotArray:
			if UseConst:
				pointer = " const*"
			else:
				pointer = "*"
			return self.nativeType + pointer * self.__dimensionArray
		else:
			return self.nativeType

	def getNativeTypeForceNotArray(self):
		return self.getNativeType(ForceNotArray=True)

	def getNativeTypeWithConst(self):
		return self.getNativeType(UseConst=True)

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
			return "CallStaticObjectMethod"
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



	def setDimensionArray(self, dimensionArray):
		""" Defines the size of the array
		"""
		self.__dimensionArray=dimensionArray

	def getDimensionArray(self):
		""" return the size of the array
		"""
		return self.__dimensionArray


	def __getProfileCreationOfTheArray(self, varName, detachThread):
		"""
		When we deal with an array as input, we need to 'transform' it for
		Java"""
		javaType=self.getJavaTypeSyntaxForceNotArray()

		# removes the leading j and put the first char uppercase
		shortType=self.getJavaShortTypeForceNotArray()

		if configGiws().getThrowsException():
			errorMgnt="""
			if (%s_ == NULL)
			{%s
			// check that allocation succeed
			throw %s::JniBadAllocException(curEnv);
			}
			"""%(varName,detachThread,configGiws().getExceptionFileName())
                        errorMgntLocal="""
			if (%sLocal == NULL)
			{%s
			// check that allocation succeed
			curEnv->DeleteLocalRef(%s_);
			throw %s::JniBadAllocException(curEnv);
			}
			"""%(varName, detachThread, varName, configGiws().getExceptionFileName())
		else:
			errorMgnt=""
                        errorMgntLocal=""

                if self.getDimensionArray() == 1:
			# Yep, it seems ugly to have that much varName but it is normal.
			return """
			%sArray %s_ = curEnv->New%sArray( %sSize ) ;
			%s
			curEnv->Set%sArrayRegion( %s_, 0, %sSize, (%s*)(%s) ) ;

			"""%(javaType, varName, shortType, varName, errorMgnt, shortType, varName, varName, javaType, varName)
                else:
			return """
			 jobjectArray %s_ = curEnv->NewObjectArray(%sSize, curEnv->FindClass("[%s"),NULL);
			%s
			 for (int i=0; i<%sSize; i++){

			%sArray %sLocal = curEnv->New%sArray( %sSizeCol ) ;
			%s
			curEnv->Set%sArrayRegion( %sLocal, 0, %sSizeCol, (%s*)(%s[i]) ) ;
			curEnv->SetObjectArrayElement(%s_, i, %sLocal);
			curEnv->DeleteLocalRef(%sLocal);
			}
			"""%(varName, varName, self.getTypeSignature(), errorMgnt, varName, javaType, varName, shortType, varName, errorMgntLocal, shortType, varName, varName, javaType, varName, varName, varName, varName)

	def specificPreProcessing(self, parameter, detachThread):
		""" Preprocessing before calling the java method
		"""
		if self.isArray():
			return self.__getProfileCreationOfTheArray(parameter.getName(), detachThread)
		else:
			return None


	def specificPostDeleteMemory(self, parameter):
		""" Preprocessing before calling the java method
		"""
		return """curEnv->DeleteLocalRef(%s_);
		"""%(parameter.getName())


	def specificPostProcessing(self, detachThread):
		""" Preprocessing after calling the java method
		"""

		javaType=self.getJavaTypeSyntax()
		javaTypeNotArray=self.getJavaTypeSyntaxForceNotArray()
		shortType=self.getJavaShortType(forceNotArray=True)
		nativeTypeForceNotArray=self.getNativeTypeForceNotArray()

		if self.isArray():
                        str="""if (res == NULL) { return NULL; }
                        """
                        str+=JNIFrameWork().getExceptionCheckProfile(detachThread)
                        strCommon=""
                        strDeclaration=""
			if configGiws().getDisableReturnSize()==True:
                            strCommon+="int lenRow;"
                        else:
                            # The size of the array is returned as output argument of the function 
                            strDeclaration="*"
                        strCommon+="""
			%s lenRow = curEnv->GetArrayLength(res);
			jboolean isCopy = JNI_FALSE;
			"""%(strDeclaration)
                        if self.getDimensionArray() == 1:
                            	str+=strCommon+"""
				/* GetPrimitiveArrayCritical is faster than getXXXArrayElements */
				%s *resultsArray = static_cast<%s *>(curEnv->GetPrimitiveArrayCritical(res, &isCopy));
				%s myArray= new %s[%s lenRow];

				for (jsize i = 0; i < %s lenRow; i++){
				myArray[i]=resultsArray[i];
				}
				curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);

                        	curEnv->DeleteLocalRef(res);
				"""%(javaTypeNotArray, javaTypeNotArray, self.getNativeType(), nativeTypeForceNotArray, strDeclaration, strDeclaration)
                                return str

                        else:
				if configGiws().getDisableReturnSize()==True:
					str+="int lenCol"
				str+=strCommon+"""
				%s ** myArray = new %s*[%s lenRow];
				for(int i=0; i<%s lenRow; i++) {
				%sArray oneDim = (%sArray)curEnv->GetObjectArrayElement(res, i);
				%s lenCol=curEnv->GetArrayLength(oneDim);
				%s *resultsArray = static_cast<%s *>(curEnv->GetPrimitiveArrayCritical(oneDim, &isCopy));
				myArray[i] = new %s[%s lenCol];
				for(int j=0; j<%s lenCol; j++) {
				myArray[i][j]= resultsArray[j];
				}
				curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);
				}

				curEnv->DeleteLocalRef(res);
				"""%(self.nativeType, self.nativeType, strDeclaration,  strDeclaration, javaTypeNotArray, javaTypeNotArray, strDeclaration, self.nativeType, self.nativeType, nativeTypeForceNotArray, strDeclaration, strDeclaration)
                                return str
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
