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
	
	def specificPostProcessing(self):
		return ("""
		const char *tempString = this->%sGetStringUTFChars(res, 0);
		char * myStringBuffer= (char*)malloc (strlen(tempString)*sizeof(char)+1);
		strcpy(myStringBuffer, tempString);
		this->%sReleaseStringUTFChars(res, tempString);
""" % (JNIFrameWork().JNIEnvAccess(),JNIFrameWork().JNIEnvAccess()))

	def specificReturn(self):
		return """
		return myStringBuffer;
		"""
	
