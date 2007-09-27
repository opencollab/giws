#!/usr/bin/python -u
from parameterGiws import parameterGiws
from JNIFrameWork import JNIFrameWork
from datatypes.dataGiws import dataGiws
from types import MethodType

class methodGiws:
	__name=""
	__returns=""
	__parameters=[]
	
	def __init__(self, name, returns):
		self.__name=name
		if isinstance(returns,dataGiws):
			self.__returns=returns
		else:
			raise Exception("The type must be a dataGiws object")
		self.__parameters=[]

	def addParameter(self, parameter):
		if isinstance(parameter,parameterGiws):
			self.__parameters.append(parameter)

	def getName(self):
		return self.__name

	def getReturn(self):
		return self.__returns
	
	def getParameters(self):
		return self.__parameters

	def getParametersCXX(self):
		""" Returns the parameters with their types """
		i=1
		str=""
		for parameter in self.__parameters:
			str=str+parameter.generateCXXHeader()
			if len(self.__parameters)!=i: 
				str+=", "
			i=i+1
		return str
	
	def __str__(self):
		parametersStr=""
		for parameter in self.getParameters():
			parametersStr=parametersStr+parameter.__str__()
		return """%s %s ( %s )
		""" % (self.getReturn(), self.getName(), parametersStr)

	def __createMethodBody(self):
		str=JNIFrameWork().getObjectInstanceProfile()
		str+=JNIFrameWork().getMethodIdProfile(self)
		
		if hasattr(self.getReturn(), "specificPreProcessing") and type(self.getReturn().specificPreProcessing) is MethodType:
			str+=self.getReturn().specificPreProcessing()
			
		str+=JNIFrameWork().getCallObjectMethodProfile(self)
		
		if hasattr(self.getReturn(), "specificPostProcessing") and type(self.getReturn().specificPostProcessing) is MethodType:
			str+=self.getReturn().specificPostProcessing()

		str+=JNIFrameWork().getReturnProfile(self.getReturn())

		return str

	def getUniqueNameOfTheMethod(self):
		paramStr=""
		for parameter in self.getParameters(): #Creates a unique string of all the profiles
			paramStr+=parameter.getType().getJavaTypeSyntax() 
		str="""%s%s%sID"""%(self.getReturn().getJavaTypeSyntax(), self.getName(), paramStr)
		

		return str
	
	def generateCXXHeader(self):
		 str="""%s %s(%s);
		 """%(self.getReturn().getNativeType(), self.getName(), self.getParametersCXX())
		 return str
	 
	def generateCXXBody(self, className):
		baseProfile="""%s %s::%s"""%(self.getReturn().getNativeType(),className, self.getName())
		
		str="""
		%s (%s)"""%(baseProfile,self.getParametersCXX())
			
		str+="""{
		%s
		}"""%(self.__createMethodBody())
		
		return str
	
