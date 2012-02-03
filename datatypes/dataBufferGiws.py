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

class dataBufferGiws(dataGiws):
	callMethod="CallObjectMethod"
	callStaticMethod="CallStaticObjectMethod"

	def isByteBufferBased(self):
		return True

	def getJavaTypeSyntax(self):
		return "jobject"

	def __errorMemoryByteBuffer(self, detachThread):
		# Management of the error when not enough memory to create the XXXXXBuffer
		if configGiws().getThrowsException():
			errorMgntMemBis="""%sthrow %s::JniBadAllocException(curEnv);"""%(detachThread,configGiws().getExceptionFileName())
		else:
			errorMgntMemBis="""std::cerr << "Could not convert C %s to Java UTF %s, memory full." << std::endl;%s
			exit(EXIT_FAILURE);"""%(self.getJavaBufferType(), self.getJavaBufferType(), detachThread)
		return errorMgntMemBis

	def specificPreProcessing(self, parameter, detachThread):
		""" Overrides the preprocessing of the array """
		name=parameter.getName()
		# Management of the error when not enought memory to create the XXXXXBuffer
		if configGiws().getThrowsException():
			errorMgntMem="""%sthrow %s::JniBadAllocException(curEnv);"""%(detachThread,configGiws().getExceptionFileName())
		else:
			errorMgntMem="""std::cerr << "Could not allocate Java %s array, memory full." << std::endl;%s
			exit(EXIT_FAILURE);"""%(self.getJavaBufferType(), detachThread)

			errorMgntMemBis = self.__errorMemoryByteBuffer(detachThread)


		return """

            jobject buffer%s = curEnv->NewDirectByteBuffer((void*)%s, (jlong)%sSize * sizeof(double));
if (!buffer%s)
{
    throw GiwsException::JniBadAllocException(curEnv);
}

if (ByteOrderClass == NULL) {
// TODO
// tu peux mettre en cache ByteOrderClass, nativeOrderID, bbCls et asdbID
// Les modifs ont essentiellement lieu ici
ByteOrderClass = curEnv->FindClass("java/nio/ByteOrder");
if (ByteOrderClass == NULL) {
curEnv->ExceptionDescribe();
}
// public static ByteOrder nativeOrder()
nativeOrderID = curEnv->GetStaticMethodID(ByteOrderClass, "nativeOrder", "()Ljava/nio/ByteOrder;");
if (nativeOrderID == NULL) {
curEnv->ExceptionDescribe();
}
}

nativeOrder = curEnv->CallStaticObjectMethod(ByteOrderClass, nativeOrderID, buffer%s);
//                        curEnv->DeleteLocalRef(cls);
if (curEnv->ExceptionCheck()) {
throw GiwsException::JniCallMethodException(curEnv);
}


if (bbCls == NULL) {
bbCls = curEnv->FindClass("java/nio/ByteBuffer");
if (bbCls == NULL) {
curEnv->ExceptionDescribe();
}

orderID = curEnv->GetMethodID(bbCls, "order", "(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;");
if (orderID == NULL) {
curEnv->ExceptionDescribe();
}
}

buffer%s = curEnv->CallObjectMethod(buffer%s, orderID, nativeOrder);

if (asdbID == NULL) {
 asdbID = curEnv->GetMethodID(bbCls, "as%s", "()%s");
if (asdbID == NULL) {
curEnv->ExceptionDescribe();
}
}

jobject %s_ = curEnv->CallObjectMethod(buffer%s, asdbID);


if (%s_ == NULL)
{
// check that allocation succeed
throw GiwsException::JniBadAllocException(curEnv);
}
"""%(name, name, name, name, name, name, name, self.getJavaBufferType(), self.getTypeSignature(), name, name, name)
	
	def specificPostProcessing(self, detachThread):
		""" Called when we are returning a XXXXXBuffer or an array of XXXBuffer TODO """
		# We are doing an exception check here JUST in this case because
		# in methodGiws::__createMethodBody we usually do it at the end
		# of the method just after deleting the variable
		# but when dealing with DoubleBuffer, in this method, we are calling some
		# methods which override the "exception engine" which drive the JNI
		# engine crazy. TODO check

		str=JNIFrameWork().getExceptionCheckProfile(detachThread)

		if self.isArray():
			strCommon=""
			strDeclaration=""
			if configGiws().getDisableReturnSize()==True:
				strCommon+="int lenRow;"
			else:
				# The size of the array is returned as output argument of the function 
				strDeclaration="*"
			self.temporaryVariableName="byteBufferRes"
			if self.getDimensionArray() == 1:
				str+=strCommon+"""
        *lenRow = curEnv->GetDirectBufferCapacity(res);
        %s %s = static_cast<%s>(curEnv->GetDirectBufferAddress(res));

        curEnv->DeleteLocalRef(res);
        curEnv->DeleteLocalRef(cls);
        if (curEnv->ExceptionCheck()) {
            curEnv->ExceptionDescribe() ;
        }
				"""%(self.getNativeType(), self.temporaryVariableName, self.getNativeType())
				return str
			else:
				if configGiws().getDisableReturnSize()==True:
					str+="int lenCol;"
				str+=strCommon+"""
                TODO voir si on delete ca
				char ***arrayOfByteBuffer;
				arrayOfByteBuffer = new char **[%slenRow];
				for (jsize i = 0; i < %slenRow; i++){ /* Line of the array */
				jobjectArray resByteBufferLine = reinterpret_cast<jobjectArray>(curEnv->GetObjectArrayElement(res, i));
				%slenCol = curEnv->GetArrayLength(resByteBufferLine);
				arrayOfByteBuffer[i]=new char*[%slenCol];
				for (jsize j = 0; j < %slenCol; j++){
				jDoubleBuffer resByteBuffer = reinterpret_cast<jDoubleBuffer>(curEnv->GetObjectArrayElement(resByteBufferLine, j));
				const char *tempByteBuffer = curEnv->GetByteBufferUTFChars(resByteBuffer, 0);
				arrayOfByteBuffer[i][j] = new char[strlen(tempByteBuffer) + 1];
				strcpy(arrayOfByteBuffer[i][j], tempByteBuffer);
				curEnv->ReleaseByteBufferUTFChars(resByteBuffer, tempByteBuffer);
				curEnv->DeleteLocalRef(resByteBuffer);
}
				curEnv->DeleteLocalRef(resByteBufferLine);
				 }
				"""%(strDeclaration, strDeclaration, strDeclaration, strDeclaration, strDeclaration)
				return str

		else:
			if hasattr(self,"parameterName"):
				str+="""curEnv->DeleteLocalRef(%s);"""%(self.parameterName+"_")
			return str+"""

			const char *tempByteBuffer = curEnv->GetByteBufferUTFChars(res, 0);
			char * %s = new char[strlen(tempByteBuffer) + 1];
			strcpy(%s, tempByteBuffer);
			curEnv->ReleaseByteBufferUTFChars(res, tempByteBuffer);
			curEnv->DeleteLocalRef(res);
			"""%(self.temporaryVariableName, self.temporaryVariableName)

	def getReturnSyntax(self):
		if self.isArray():
			return """
			curEnv->DeleteLocalRef(res);
			return %s;
			"""%(self.temporaryVariableName)
		else:
			return """
			return %s;
			"""%(self.temporaryVariableName)
	
