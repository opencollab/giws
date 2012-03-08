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

from dataGiws import dataGiws
from configGiws import configGiws
from JNIFrameWork import JNIFrameWork

class stringDataGiws(dataGiws):

	nativeType="char *"
	callMethod="CallObjectMethod"
	callStaticMethod="CallStaticObjectMethod"
	temporaryVariableName="myStringBuffer"

	def getTypeSignature(self):
		return "Ljava/lang/String;"

	def getJavaTypeSyntax(self):
		if self.isArray():
			return "jobjectArray"
		else:			
			return "jstring"

	def getRealJavaType(self):
		return "java.lang.String"

	def getDescription(self):
		return "Java String"

	def getNativeType(self, ForceNotArray=False, UseConst=False):
		if self.isArray():
			if UseConst:
				pointer = " const*"
			else:
				pointer = "*"
			return ("char" + pointer) + pointer * self.getDimensionArray()
		else:
			if UseConst:
				pointer = " const*"
			else:
				pointer = "*"
			return "char" + pointer

        def __errorMemoryString(self, detachThread):
		# Management of the error when not enought memory to create the string
		if configGiws().getThrowsException():
			errorMgntMemBis="""%sthrow %s::JniBadAllocException(curEnv);"""%(detachThread,configGiws().getExceptionFileName())
		else:
			errorMgntMemBis="""std::cerr << "Could not convert C string to Java UTF string, memory full." << std::endl;%s
			exit(EXIT_FAILURE);"""%(detachThread)
                return errorMgntMemBis

	def specificPreProcessing(self, parameter, detachThread):
		""" Overrides the preprocessing of the array """
		name=parameter.getName()
		# Management of the error when not enought memory to create the string
		if configGiws().getThrowsException():
			errorMgntMem="""%sthrow %s::JniBadAllocException(curEnv);"""%(detachThread,configGiws().getExceptionFileName())
		else:
			errorMgntMem="""std::cerr << "Could not allocate Java string array, memory full." << std::endl;%s
			exit(EXIT_FAILURE);"""%(detachThread)

                errorMgntMemBis = self.__errorMemoryString(detachThread)

		if self.isArray():
			if self.getDimensionArray() == 1:
				return """			
			
				// create java array of strings.
				jobjectArray %s_ = curEnv->NewObjectArray( %sSize, stringArrayClass, NULL);
				if (%s_ == NULL)
				{
				%s
				}

				// convert each char * to java strings and fill the java array.
				for ( int i = 0; i < %sSize; i++)
				{
				jstring TempString = curEnv->NewStringUTF( %s[i] );
				if (TempString == NULL)
				{
				%s
				}
			
				curEnv->SetObjectArrayElement( %s_, i, TempString);
			
				// avoid keeping reference on to many strings
				curEnv->DeleteLocalRef(TempString);
				}"""%(name,name,name,errorMgntMem,name,name,errorMgntMemBis,name)
			else:
				return """
				// create java array of array of strings.
				jobjectArray %s_ = curEnv->NewObjectArray( %sSize, curEnv->FindClass("[Ljava/lang/String;"), NULL);
				if (%s_ == NULL)
				{
				%s
				}

				for ( int i = 0; i < %sSize; i++)
				{
				jobjectArray %sLocal = curEnv->NewObjectArray( %sSizeCol, stringArrayClass, NULL);
				// convert each char * to java strings and fill the java array.
				for ( int j = 0; j < %sSizeCol; j++) {
				jstring TempString = curEnv->NewStringUTF( %s[i][j] );
				
				if (TempString == NULL)
				{
				%s
				}

				curEnv->SetObjectArrayElement( %sLocal, j, TempString);

				// avoid keeping reference on to many strings
				curEnv->DeleteLocalRef(TempString);
				}
				curEnv->SetObjectArrayElement(%s_, i, %sLocal);
				curEnv->DeleteLocalRef(%sLocal);

				}"""%(name,name,name,errorMgntMem,name,name,name,name,name,errorMgntMemBis,name,name,name,name)

		else:
			# Need to store is for the post processing (delete)
			self.parameterName=name
                        tempName=name+"_"
			return """
			jstring %s = curEnv->NewStringUTF( %s );
			if (%s != NULL && %s == NULL)
			{
			%s
			}

			"""%(tempName,name,name,tempName,errorMgntMemBis)
	
	def specificPostProcessing(self, detachThread):
		""" Called when we are returning a string or an array of string """
		# We are doing an exception check here JUST in this case because
		# in methodGiws::__createMethodBody we usually do it at the end
		# of the method just after deleting the variable
		# but when dealing with string, in this method, we are calling some
		# methods which override the "exception engine" which drive the JNI
		# engine crazy.

		str=JNIFrameWork().getExceptionCheckProfile(detachThread)

		if self.isArray():
			strCommon=""
			strDeclaration=""
			if configGiws().getDisableReturnSize()==True:
				strCommon+="int lenRow;"
			else:
				# The size of the array is returned as output argument of the function 
				strDeclaration="*"
			strCommon+="""
			%s lenRow = curEnv->GetArrayLength(res);
			"""%(strDeclaration)
                        self.temporaryVariableName="arrayOfString"
			if self.getDimensionArray() == 1:
				str+=strCommon+"""
				char **arrayOfString;
				arrayOfString = new char *[%slenRow];
				for (jsize i = 0; i < %slenRow; i++){
				jstring resString = reinterpret_cast<jstring>(curEnv->GetObjectArrayElement(res, i));
				const char *tempString = curEnv->GetStringUTFChars(resString, 0);
				arrayOfString[i] = new char[strlen(tempString) + 1];
	
				strcpy(arrayOfString[i], tempString);
				curEnv->ReleaseStringUTFChars(resString, tempString);
				curEnv->DeleteLocalRef(resString);
				}
				"""%(strDeclaration, strDeclaration)
				return str
			else:
				if configGiws().getDisableReturnSize()==True:
					str+="int lenCol;"
				str+=strCommon+"""
				char ***arrayOfString;
				arrayOfString = new char **[%slenRow];
				for (jsize i = 0; i < %slenRow; i++){ /* Line of the array */
				jobjectArray resStringLine = reinterpret_cast<jobjectArray>(curEnv->GetObjectArrayElement(res, i));
				%slenCol = curEnv->GetArrayLength(resStringLine);
				arrayOfString[i]=new char*[%slenCol];
				for (jsize j = 0; j < %slenCol; j++){
				jstring resString = reinterpret_cast<jstring>(curEnv->GetObjectArrayElement(resStringLine, j));
				const char *tempString = curEnv->GetStringUTFChars(resString, 0);
				arrayOfString[i][j] = new char[strlen(tempString) + 1];
				strcpy(arrayOfString[i][j], tempString);
				curEnv->ReleaseStringUTFChars(resString, tempString);
				curEnv->DeleteLocalRef(resString);
}
				curEnv->DeleteLocalRef(resStringLine);
				 }
				"""%(strDeclaration, strDeclaration, strDeclaration, strDeclaration, strDeclaration)
				return str

		else:
			if hasattr(self,"parameterName"):
				str+="""curEnv->DeleteLocalRef(%s);"""%(self.parameterName+"_")
			return str+"""

			const char *tempString = curEnv->GetStringUTFChars(res, 0);
			char * %s = new char[strlen(tempString) + 1];
			strcpy(%s, tempString);
			curEnv->ReleaseStringUTFChars(res, tempString);
			curEnv->DeleteLocalRef(res);
			"""%(self.temporaryVariableName, self.temporaryVariableName)

	def getReturnSyntax(self):
		if self.isArray():
			return """
			curEnv->DeleteLocalRef(res);
			return arrayOfString;
			"""
		else:
			return """
			return %s;
			"""%(self.temporaryVariableName)
	
