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

from types import MethodType
from configGiws import configGiws

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	__JavaVMVariable="jvm"
	__JavaVMVariableType="JavaVM"

	def getHeader(self,namespaceName):
		strHeader="""
		#ifndef __%s__
		#define __%s__
		#include <iostream>
		#include <string>
		#include <string.h>
		#include <stdlib.h>
		#include <jni.h>
		"""%(namespaceName.upper(), namespaceName.upper())
		# add the include for giws exception
		if configGiws().getThrowsException() and not namespaceName==configGiws().getExceptionFileName():
			strHeader+="""
			#include "%s"
			"""%(configGiws().getExceptionFileName()+configGiws().getCPPHeaderExtension())
		# Byte support
		strHeader+="""
        #if !defined(byte) | !defined(_MSC_VER) /* Defined anyway with Visual */
                typedef signed char byte;
        #else
                #pragma message("Byte has been redefined elsewhere. Some problems can happen")
        #endif
		"""
		return strHeader

	# For the extends (inheritance) support
	def getHeaderInheritance(self):
		strHeader="""
		#ifndef FAKEGIWSDATATYPE
		#define FAKEGIWSDATATYPE
		namespace fakeGiwsDataType {
		struct fakeGiwsDataType {
		};
		}
		#endif
		"""
		return strHeader

	def getJavaVMVariable(self):
		return self.__JavaVMVariable
	
	def getJavaVMVariableType(self):
		return self.__JavaVMVariableType

	def getMethodGetCurrentEnv(self,objectName):
		if configGiws().getThrowsException():
			error = """throw %s::JniException(getCurrentEnv());"""%(configGiws().getExceptionFileName())

		else:
			error = """std::cerr << "Could not retrieve the current JVM." << std::endl;
			exit(EXIT_FAILURE);
			"""
		return """
		JNIEnv * %s::getCurrentEnv() {
		JNIEnv * curEnv = NULL;
		jint res=this->jvm->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);
		if (res != JNI_OK) {
		%s
		}
		return curEnv;
		}"""%(objectName, error)

	
	def getObjectDestuctor(self,objectName,stringClassSet=False):
		myStr="""
		%s::~%s() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);
		
		curEnv->DeleteGlobalRef(this->instance);
		curEnv->DeleteGlobalRef(this->instanceClass);
		"""%(objectName, objectName)
		if stringClassSet==True:
			myStr += "curEnv->DeleteGlobalRef(this->stringArrayClass);"
		myStr+="}"
		return myStr

	def getSynchronizeMethod(self,objectName):
		myStr="""
		void %s::synchronize() {
		if (getCurrentEnv()->MonitorEnter(instance) != JNI_OK) {
		"""%(objectName)
		if configGiws().getThrowsException():
			myStr += """throw %s::JniMonitorException(getCurrentEnv(), "%s");"""%(configGiws().getExceptionFileName(),objectName)
		else:
			myStr += """std::cerr << "Fail to enter monitor." << std::endl;
			exit(EXIT_FAILURE);
			"""
		return myStr + """
		}
		}"""
	
	def getEndSynchronizeMethod(self,objectName):
		myStr="""
		void %s::endSynchronize() {
		if ( getCurrentEnv()->MonitorExit(instance) != JNI_OK) {
		"""%(objectName)
		if configGiws().getThrowsException():
			myStr+="""throw %s::JniMonitorException(getCurrentEnv(), "%s");"""%(configGiws().getExceptionFileName(),objectName)
		else:
			myStr+= """
			std::cerr << "Fail to exit monitor." << std::endl;
			exit(EXIT_FAILURE);"""
		return myStr + """
		}
		}"""
	
        # For static methods, we can not call getCurrentEnv() because it is not static
	def getStaticProfile(self):
		return """
		JNIEnv * curEnv = NULL;
		jvm_->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);
		jclass cls = curEnv->FindClass( className().c_str() );
		""" 

	def getDeleteStaticProfile(self):
		return """curEnv->DeleteLocalRef(cls);
		"""
	
	def getObjectInstanceProfile(self):
		return """
		JNIEnv * curEnv = getCurrentEnv();
		"""
	
	def getExceptionCheckProfile(self, detachThread, methodReturn=""):
		if configGiws().getThrowsException():
			str="""if (curEnv->ExceptionCheck()) {
			"""
                        if methodReturn != "":
                                str+="""delete[] %s;
                                """%(methodReturn)
                        str+= """%sthrow %s::JniCallMethodException(curEnv);
			}"""%(detachThread,configGiws().getExceptionFileName())
                        return str
		else:
			return """if (curEnv->ExceptionCheck()) {
			curEnv->ExceptionDescribe() ;
			}
			"""

	def getMethodIdProfile(self, method):
		params=""

		for parameter in method.getParameters():
			if parameter.getType().isArray() and not parameter.getType().isByteBufferBased(): # It is an array
				params+="[" * parameter.getType().getDimensionArray()
			params+=parameter.getType().getTypeSignature()

		methodIdName=method.getUniqueNameOfTheMethod()
		
		signatureReturn=method.getReturn().getTypeSignature()
		if method.getReturn().isArray() and not method.getReturn().isByteBufferBased(): # Returns an array ... 
			signatureReturn="["* method.getReturn().getDimensionArray() + signatureReturn
		
                if method.getModifier()=="static":
                        getMethod = "GetStaticMethodID"
                        firstParam = "cls"
                else:
                        getMethod = "GetMethodID"
                        firstParam = "this->instanceClass"
		if method.getModifier()=="static":
			methodCall="jmethodID"
		else:
			methodCall="""if (%s==NULL) { /* Use the cache */
			"""%methodIdName

		# Management of the error
		if configGiws().getThrowsException():
			errorMgnt="""%sthrow %s::JniMethodNotFoundException(curEnv, "%s");"""%(method.getDetachThread(),configGiws().getExceptionFileName(),method.getName())
		else:
			errorMgnt="""std::cerr << "Could not access to the method " << "%s" << std::endl;
			curEnv->ExceptionDescribe();
			%s
			exit(EXIT_FAILURE);"""%(method.getName(),method.getDetachThread())
			
		methodIdProfile="""
		%s %s = curEnv->%s(%s, "%s", "(%s)%s" ) ;
		if (%s == NULL) {
		%s
		}
		"""%(methodCall, methodIdName, getMethod, firstParam, method.getName(), params,signatureReturn, methodIdName, errorMgnt)
		if method.getModifier()!="static":
			methodIdProfile+="}" # Cached methodId 
		return methodIdProfile


	def getCallObjectMethodProfile(self, method):
		parametersTypes=method.getParameters()
		returnType=method.getReturn()
		i=1
		params=""
		
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if parameter.getType().specificPreProcessing(parameter,method.getDetachThread())!=None:
				params+="_" # There is a pre-processing, then, we add the _ 
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
			
			
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
			returnsEnd=""
		else:
			typeOfReturn=returnType.getJavaTypeSyntax()
			returns="""%s res =  static_cast<%s>("""%(typeOfReturn, typeOfReturn)
			returnsEnd=")"

                if method.getModifier()=="static":
                        return """
                        %s curEnv->%s(cls, %s %s)%s;
                        """ % (returns, returnType.getCallStaticMethod(), method.getUniqueNameOfTheMethod(), params, returnsEnd)
                else:
                        return """
                        %s curEnv->%s( this->instance, %s %s)%s;
                        """ % (returns, returnType.getCallMethod(), method.getUniqueNameOfTheMethod(), params, returnsEnd)
		
	def getReturnProfile(self, returnType):
		return returnType.getReturnSyntax()
		

        def getDLLExportSyntax(self):
                return """
		#ifndef GIWSEXPORT
		# if defined(_MSC_VER) || defined(__WIN32__) || defined(__CYGWIN__)
		#   if defined(STATIC_LINKED)
		#     define GIWSEXPORT
		#   else
		#     define GIWSEXPORT __declspec(dllexport)
		#   endif
		# else
		#   if __GNUC__ >= 4
		#     define GIWSEXPORT __attribute__ ((visibility ("default")))
		#   else
		#     define GIWSEXPORT
		#   endif
		# endif
		#endif
		"""
