#!/usr/bin/python -u
from types import MethodType

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	JNIEnvVariable="JEnv"
	JNIEnvVariableType="JNIEnv"
	def getHeader(self):
		return """#include <jni.h>
		#include <string>
		"""

	def JNIEnvAccess(self):
		return ("""%s->""" % self.JNIEnvVariable)

	def getJNIEnvVariable(self):
		return self.JNIEnvVariable
	
	def getJNIEnvVariableType(self):
		return self.JNIEnvVariableType
	
	def getObjectInstanceProfile(self):		
		return """
		jclass instanceClass = this->%sGetObjectClass(*instance) ;
		""" % self.JNIEnvAccess()

	def getMethodIdProfile(self, methodName, parametersTypes, returnType):
		params=""
		for parameter in parametersTypes:
			params+=parameter.getType().getTypeSignature()
		return ("""
		jmethodID methodId = this->%sGetMethodID(instanceClass, "%s", "(%s)%s" ) ;
		    if (methodId == 0) {
			cerr << "Could not access to the method %s" << endl;
			return;
			}
		
		"""%(self.JNIEnvAccess(), methodName, params, returnType.getTypeSignature()))

	def getCallObjectMethodProfile(self,parametersTypes,returnType):
		i=1
		params=""
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
		else:
			returns="""%s res ="""%returnType.getJavaTypeSyntax()

		return ("""
	 	%s (%s) this->%s%s( instanceClass, methodId %s);
""" % (returns, returnType.getJavaTypeSyntax(),  self.JNIEnvAccess(), returnType.CallMethod(), params ))

	def getReturnProfile(self, returnType):
		
		if hasattr(returnType, "specificReturn") and type(returnType.specificReturn) is MethodType:
			return returnType.specificReturn()
		else:
			return """
			return res;
			"""
		
