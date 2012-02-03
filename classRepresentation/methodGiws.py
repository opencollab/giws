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

from parameterGiws import parameterGiws
from JNIFrameWork import JNIFrameWork
from datatypes.dataGiws import dataGiws
from datatypes.stringDataGiws import stringDataGiws
from types import MethodType
from configGiws import configGiws

class methodGiws:
	__name=""
	__returns=""
	__modifier=""
	__detachThread=""
	__parameters=[]
	
	def __init__(self, name, returns, detachThread, modifier=None):
		self.__name=name
		if isinstance(returns,dataGiws) or isinstance(returns,dataBufferGiws):
			self.__returns=returns
		else:
			raise Exception("The type must be a dataGiws object")
		self.__parameters=[]
		if detachThread:
			self.__detachThread="\njvm_->DetachCurrentThread();\n"
		self.__modifier=modifier

	def addParameter(self, parameter):
		if isinstance(parameter,parameterGiws):
			self.__parameters.append(parameter)

	def getName(self):
		return self.__name

	def getReturn(self):
		return self.__returns
	
	def getModifier(self):
		return self.__modifier

	def getParameters(self):
		return self.__parameters

	def getDetachThread(self):
		return self.__detachThread

	def getParametersCXX(self):
		""" Returns the parameters with their types """
		i=1
		if self.getModifier()=="static":
			str="JavaVM * jvm_"
			if len(self.__parameters)!=0:
				str+=", "	
			else:
				# In the case where there is no input argument
				# but return an array of int (or an other type)
				# needed to lenRow
				if self.getReturn().isArray() and configGiws().getDisableReturnSize()!=True:
					str+=", "

		else:
			str=""

		for parameter in self.__parameters:
			str=str+parameter.generateCXXHeader()
			if len(self.__parameters)!=i: 
				str+=", "
			i=i+1
		return str
	
	def __createMethodBody(self):
		if self.getModifier()=="static":
			str=JNIFrameWork().getStaticProfile()
		else:
			str=JNIFrameWork().getObjectInstanceProfile()
		str+=JNIFrameWork().getMethodIdProfile(self)

				
		arrayOfStringDeclared=False
		
		for parameter in self.__parameters:
			paramType=parameter.getType()
			# Only declared once this object
			if type(paramType) is stringDataGiws and paramType.isArray() and not arrayOfStringDeclared:
				str+="""		jclass stringArrayClass = curEnv->FindClass("java/lang/String");"""
				arrayOfStringDeclared=True
				
			if paramType.specificPreProcessing(parameter,self.getDetachThread())!=None:
				str+=paramType.specificPreProcessing(parameter,self.getDetachThread())

		# Retrieve the call profile to the java object
		str+=JNIFrameWork().getCallObjectMethodProfile(self)

		# add specific post processing stuff
		if hasattr(self.getReturn(), "specificPostProcessing") and type(self.getReturn().specificPostProcessing) is MethodType:
			# For this datatype, there is some stuff to do AFTER the method call
			str+=self.getReturn().specificPostProcessing(self.getDetachThread())

		# Delete the stringArrayClass object if used before
		if arrayOfStringDeclared:
			str+="""curEnv->DeleteLocalRef(stringArrayClass);
			"""

		for parameter in self.__parameters:
			paramType=parameter.getType()
			if paramType.isArray():
				str+=paramType.specificPostDeleteMemory(parameter)
			else:
				if isinstance(paramType,stringDataGiws):
					str+=paramType.specificPostDeleteMemory(parameter)


		if self.getModifier()=="static":
			str+=JNIFrameWork().getDeleteStaticProfile()

			if hasattr(self.getReturn(), "specificPostProcessing") and type(self.getReturn().specificPostProcessing) is MethodType and (self.getReturn().isArray() or isinstance(self.getReturn(),stringDataGiws)):
				# Check the exception with a delete to avoid memory leak
				str+=JNIFrameWork().getExceptionCheckProfile(self.getDetachThread(), self.getReturn().temporaryVariableName)
			else:
				str+=JNIFrameWork().getExceptionCheckProfile(self.getDetachThread())

		str+=self.getDetachThread()
		str+=JNIFrameWork().getReturnProfile(self.getReturn())

		return str

	def getUniqueNameOfTheMethod(self):
		paramStr=""
		for parameter in self.getParameters(): #Creates a unique string of all the profiles
			paramStr+=parameter.getType().getJavaTypeSyntax() + "_"*parameter.getType().getDimensionArray()
			paramStr+=parameter.getType().getRealJavaType().replace(".","_")
			if parameter.getType().isArray(): # Avoid to have jobjectArray in the profile. Does not show the actual type. Fixes bug #143
			  paramStr+=parameter.getType().getRealJavaType().replace(".","_")
		str="""%s%s%sID"""%(self.getReturn().getJavaTypeSyntax() + "_" * self.getReturn().getDimensionArray(), self.getName(), paramStr)
		

		return str
	
	def generateCXXHeader(self):
		""" Generates the profile of the method ... for the header """

		if self.getModifier()=="static":
			static="static "
		else:
                        static=""
		
		ret=""
		if self.getReturn().isArray() and configGiws().getDisableReturnSize()!=True:
			if len(self.__parameters)!=0:
				ret+=", "
			if self.getReturn().getDimensionArray() == 1:
				ret+="int *lenRow"
			else:
				ret+="int *lenRow, int *lenCol"

		str="""%s%s %s(%s%s);
		"""%(static, self.getReturn().getNativeType(), self.getName(), self.getParametersCXX(),ret)
		return str
	 
	def generateCXXBody(self, className):
		""" Generates the content of the method ... for the body """
		baseProfile="""%s %s::%s"""%(self.getReturn().getNativeType(),className, self.getName())
		
		ret=""
		if self.getReturn().isArray() and configGiws().getDisableReturnSize()!=True:
			if len(self.__parameters)!=0:
				ret+=", "
			if self.getReturn().getDimensionArray() == 1:
				ret+="int *lenRow"
			else:
				ret+="int *lenRow, int *lenCol"

		str="""
		%s (%s%s)"""%(baseProfile,self.getParametersCXX(),ret)
			
		str+="""{
		%s
		}"""%(self.__createMethodBody())
		
		return str
	
