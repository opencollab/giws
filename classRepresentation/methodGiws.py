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

class methodGiws:
	__name=""
	__returns=""
	__modifier=""
	__parameters=[]
	
	def __init__(self, name, returns, modifier=None):
		self.__name=name
		if isinstance(returns,dataGiws):
			self.__returns=returns
		else:
			raise Exception("The type must be a dataGiws object")
		self.__parameters=[]
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

	def getParametersCXX(self):
		""" Returns the parameters with their types """
		i=1
                if self.getModifier()=="static":
                        str="JavaVM * jvm_"
                        if len(self.__parameters)!=0:
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
				str+="""		jclass stringArrayClass = curEnv->FindClass("Ljava/lang/String;");"""
				arrayOfStringDeclared=True
				
			if paramType.specificPreProcessing(parameter)!=None:
				str+=paramType.specificPreProcessing(parameter)

		# Retrieve the call profile to the java object
		str+=JNIFrameWork().getCallObjectMethodProfile(self)

		# add specific post processing stuff
		if hasattr(self.getReturn(), "specificPostProcessing") and type(self.getReturn().specificPostProcessing) is MethodType:
			# For this datatype, there is some stuff to do AFTER the method call		
			str+=self.getReturn().specificPostProcessing()

		# Delete the stringArrayClass object if used before
		if arrayOfStringDeclared:
			str+="""curEnv->DeleteLocalRef(stringArrayClass);
			"""

		for parameter in self.__parameters:
			if paramType.specificPostDeleteMemory(parameter)!=None:
				str+=paramType.specificPostDeleteMemory(parameter)
			
		str+=JNIFrameWork().getReturnProfile(self.getReturn())

		return str

	def getUniqueNameOfTheMethod(self):
		paramStr=""
		for parameter in self.getParameters(): #Creates a unique string of all the profiles
			paramStr+=parameter.getType().getJavaTypeSyntax() 
		str="""%s%s%sID"""%(self.getReturn().getJavaTypeSyntax(), self.getName(), paramStr)
		

		return str
	
	def generateCXXHeader(self):
		""" Generates the profile of the method ... for the header """

                if self.getModifier()=="static":
                        static="static "
                else:
                        static=""
                
		str="""%s%s %s(%s);
		"""%(static, self.getReturn().getNativeType(), self.getName(), self.getParametersCXX())
		return str
	 
	def generateCXXBody(self, className):
		""" Generates the content of the method ... for the body """
		baseProfile="""%s %s::%s"""%(self.getReturn().getNativeType(),className, self.getName())
		
		str="""
		%s (%s)"""%(baseProfile,self.getParametersCXX())
			
		str+="""{
		%s
		}"""%(self.__createMethodBody())
		
		return str
	
