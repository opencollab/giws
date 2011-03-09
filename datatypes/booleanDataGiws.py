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
from JNIFrameWork import JNIFrameWork
from configGiws import configGiws

# This class is not like other primitive datatypes because we need
# to compare variables with JNI_TRUE or JNI_FALSE
class booleanDataGiws(dataGiws):

	type="jboolean"
	nativeType="bool"
	callMethod="CallBooleanMethod"
	callStaticMethod="CallStaticBooleanMethod"
	
	def getTypeSignature(self):
		return "Z"

	def getRealJavaType(self):
		return "boolean"
	
	def getDescription(self):
		return "unsigned 8 bits"
	
	def specificPreProcessing(self, parameter, detachThread):
		name=parameter.getName()
		if self.isArray():
			if self.getDimensionArray() == 1: 
				return """			
				jbooleanArray %s = curEnv->NewBooleanArray( %sSize ) ;
				curEnv->SetBooleanArrayRegion( %s, 0, %sSize, (jboolean*)%s ) ;
				""" % (name+"_", name, name+"_", name, name)
			else:
				return """			
				jobjectArray %s_ = curEnv->NewObjectArray(%sSize, curEnv->FindClass("[%s"),NULL);
				for (int i=0; i<%sSize; i++){
	                        jbooleanArray %sLocal = curEnv->NewBooleanArray( %sSizeCol ) ;
        	                curEnv->SetBooleanArrayRegion( %sLocal, 0, %sSizeCol, (jboolean*)(%s[i]) ) ;
                	        curEnv->SetObjectArrayElement(%s_, i, %sLocal);
                        	curEnv->DeleteLocalRef(%sLocal);
	                        }
				""" % (name, name, self.getTypeSignature(), name, name, name, name, name, name, name, name, name)
		else:
			return """
			jboolean %s = (static_cast<bool>(%s) ? JNI_TRUE : JNI_FALSE);
			"""%(name+"_",name)

	def specificPostProcessing(self, detachThread):
		""" needed to avoid casting issue with Visual (myArray[i]=(resultsArray[i] == JNI_TRUE);) """
		if self.isArray():
			str=JNIFrameWork().getExceptionCheckProfile(detachThread)
			strCommon=""
			if configGiws().getDisableReturnSize()==True:
				strCommon+="int *lenRow;"
			strCommon+="""                   
			*lenRow = curEnv->GetArrayLength(res);
			jboolean isCopy = JNI_FALSE;
			"""

			if self.getDimensionArray() == 1: 

				return str+strCommon+"""
			
				/* faster than getXXXArrayElements */
				jboolean *resultsArray = static_cast<jboolean *>(curEnv->GetPrimitiveArrayCritical(res, &isCopy));
				bool * myArray= new bool[*lenRow];
				
				for (jsize i = 0; i < *lenRow; i++){
				myArray[i]=(resultsArray[i] == JNI_TRUE);
				}
				curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);
	
				curEnv->DeleteLocalRef(res);
				"""
			else:
				if configGiws().getDisableReturnSize()==True:
					str+="int *lenCol;"
				return str+strCommon+"""
				bool ** myArray = new bool*[*lenRow];
				for(int i=0; i<*lenRow; i++) {
				jbooleanArray oneDim = (jbooleanArray)curEnv->GetObjectArrayElement(res, i);
				*lenCol=curEnv->GetArrayLength(oneDim);
				bool *resultsArray = static_cast<bool *>(curEnv->GetPrimitiveArrayCritical(oneDim, &isCopy));
				myArray[i] = new bool[*lenCol];
				for(int j=0; j<*lenCol; j++) {
				myArray[i][j]=(resultsArray[j] == JNI_TRUE);
				}
				curEnv->ReleasePrimitiveArrayCritical(res, resultsArray, JNI_ABORT);
				}
 
				curEnv->DeleteLocalRef(res);
				"""

		else:
			return ""
	def getReturnSyntax(self):
		""" Avoids warnings about casting a jboolean to a bool """
		if self.isArray():
			return """
			return myArray;
			"""
		else:
			return """
			return (res == JNI_TRUE);
			"""
if __name__ == '__main__':
	print booleanDataGiws().getReturnTypeSyntax()

