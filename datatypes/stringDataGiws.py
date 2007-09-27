#!/usr/bin/python -u

from dataGiws import dataGiws
from JNIFrameWork import JNIFrameWork

class stringDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "Ljava/lang/String;"

	def getJavaTypeSyntax(self):
		return "jstring"

	def getJavaTypeArraySyntax(self):
		return "jobjectArray"

	def getRealJavaType(self):
		return "java.lang.String"

	def getDescription(self):
		return "Java String"

	def getNativeType(self):
		if self.getIsArray():
			return "char **"
		else:
			return "char *"
	
	def CallMethod(self):
		return "CallObjectMethod"

	def specificPreProcessing(self, parameter):
		return """
		jstring %s = curEnv->NewStringUTF( %s );
		"""%(parameter.getName()+"_", parameter.getName())
	
	
	def specificPostProcessing(self):
		""" Called when we are returning a string"""
		if self.getIsArray():
			return """
			jsize len = curEnv->GetArrayLength(res);
			char **arrayOfString;
			for (jsize i = 0; i < len; i++){
			jstring resString = (jstring)curEnv->GetObjectArrayElement(res, i);
			const char *tempString = curEnv->GetStringUTFChars(resString, 0);
			arrayOfString[i]= (char*)malloc (strlen(tempString)*sizeof(char)+1);
			strcpy(arrayOfString[i], tempString);
			curEnv->ReleaseStringUTFChars(resString, tempString);
			}
			"""
		else:
			return """
			const char *tempString = curEnv->GetStringUTFChars(res, 0);
			char * myStringBuffer= (char*)malloc (strlen(tempString)*sizeof(char)+1);
			strcpy(myStringBuffer, tempString);
			curEnv->ReleaseStringUTFChars(res, tempString);
			"""			

	def specificReturn(self):
		if self.getIsArray():
			return """
			return arrayOfString;
			"""
		else:
			return """
			return myStringBuffer;
			"""
	
