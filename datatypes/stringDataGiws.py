#!/usr/bin/python -u

from dataGiws import dataGiws
from JNIFrameWork import JNIFrameWork

class stringDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "Ljava/lang/String;"

	def getJavaTypeSyntax(self):
		return "jstring"

	def getRealJavaType(self):
		return "java.lang.String"

	def getDescription(self):
		return "Java String"

	def getNativeType(self):
		return "char *"
	
	def CallMethod(self):
		return "CallObjectMethod"
	
	def specificPreProcessing(self):
		return """
		char myStringBuffer[1000];
		"""
	def specificPostProcessing(self):
		return ("""
		char * tempJavaPointer = (char *)this->%sGetStringUTFChars(res, 0);
		strcpy(myStringBuffer, tempJavaPointer);
		this->%sReleaseStringUTFChars(res, tempJavaPointer);""" % (JNIFrameWork().JNIEnvAccess(),JNIFrameWork().JNIEnvAccess()))

	def specificReturn(self):
		return """
		return (char*)*myStringBuffer;
		"""
	
