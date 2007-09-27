#!/usr/bin/python -u

from methodGiws import methodGiws
from JNIFrameWork import JNIFrameWork

class objectGiws:
	__name=""
	__methods=[]
	
	def __init__(self, name):
		self.__name=name
		self.__methods=[]
		
	def addMethod(self, method):
		if isinstance(method,methodGiws):
			self.__methods.append(method)

	def getName(self):
		return self.__name

	def getMethods(self):
		return self.__methods

	def getConstructorBodyCXX(self, JNIObjectName):
		envAccess=JNIFrameWork().JNIEnvAccess()

		return """
		%s::%s {
		jmethodID constructObject = NULL ;
		jobject localInstance ;
		jclass localClass ;
		jclass instanceClass;
		string className="%s";
		string construct="<init>";
		string param="()V";
		JEnv=JEnv_;
		// récupère la classe de l'objet qu'on veut creer
		// className: org/scilab/.../maSuperClasse
		localClass = %sFindClass( className.c_str() ) ;

		// sauvegarde dans une référence global pour pouvoir l'utiliser ultérieurement.
		instanceClass = (jclass)  %sNewGlobalRef(localClass) ;

		/* "()V" for no parameters and return void */
		/* "<init>" for constructor */
		constructObject = %sGetMethodID( instanceClass, construct.c_str() , param.c_str() ) ;

		// crée une instance local à la fonction de la classe
		localInstance = %sNewObject( instanceClass, constructObject ) ;
 
		// crée une instance global
		*this->instance = %sNewGlobalRef(localInstance) ;
		}
		"""%(self.getName(), self.__getConstructorProfile(), JNIObjectName, envAccess, envAccess, envAccess, envAccess, envAccess)

	def __getConstructorProfile(self):
	  return """%s(%s * %s_)"""% (self.getName(), JNIFrameWork().getJNIEnvVariableType(), JNIFrameWork().getJNIEnvVariable())
  
	def getConstructorHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfile()

	def getMethodsCXX(self, type="header"):
		i=1
		str=""
		for method in self.__methods:
			if type=="header":
				str=str+method.generateCXXHeader()
			else:
				str=str+method.generateCXXBody(self.getName())
			if len(self.__methods)!=i:
				str+="""
				"""
			i=i+1
		return str
		
	def generateCXXHeader(self):
		return """
		class %s {
			private:
			%s * %s;
			jobject * instance;
			public:
			// Constructor
			%s
			%s
			
			};

			""" % (self.getName(),  JNIFrameWork().getJNIEnvVariableType(), JNIFrameWork().getJNIEnvVariable(), self.getConstructorHeaderCXX(), self.getMethodsCXX())

	def generateCXXBody(self, packageName):
		JNIObjectName=packageName+"/"+self.getName()
		return """%s
		%s
			""" % (self.getConstructorBodyCXX(JNIObjectName), self.getMethodsCXX("body"))
