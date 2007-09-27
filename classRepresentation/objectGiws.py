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

	def __getConstructorWhichInstanciateTheNewObject(self, JNIObjectName):
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
		
		localClass = %sFindClass( className.c_str() ) ;
		if (localClass == NULL) {
		cerr << "Could not get the Class " << className <<  endl;
		exit(EXIT_FAILURE);
		}
		
		instanceClass = (jclass) %sNewGlobalRef(localClass) ;
		if (instanceClass == NULL) {
		cerr << "Could not create a Global Ref of " << className <<  endl;
		exit(EXIT_FAILURE);
		}
		
		constructObject = %sGetMethodID( instanceClass, construct.c_str() , param.c_str() ) ;
		if(constructObject == NULL){
		cerr << "Could not retrieve the constructor of the class " << className << " with the profile : " << construct << param << endl;
		exit(EXIT_FAILURE);
		}
		
		localInstance = %sNewObject( instanceClass, constructObject ) ;
		if(localInstance == NULL){
		cerr << "Could not instance the object " << className << " with the constructor : " << construct << param << endl;
		exit(EXIT_FAILURE);
		}
		 
		*this->instance = %sNewGlobalRef(localInstance) ;
		if(this->instance == NULL){
		cerr << "Could not create a new global ref of " << className << endl;
		exit(EXIT_FAILURE);
		}
		}
		"""%(self.getName(), self.__getConstructorProfileWhichInstanciateTheNewObject(), JNIObjectName, envAccess, envAccess, envAccess, envAccess, envAccess)

		
	def __getConstructorWhichUsesAnAlreadyExistingJObject(self):
		return """
		%s::%s {
JEnv=JEnv_;

*this->instance = JEnv->NewGlobalRef(*JObj) ;
if(this->instance == NULL){
cerr << "Could not create a new global ref " << endl;
exit(EXIT_FAILURE);
}
}
		"""%(self.getName(), self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject())

		
	def getConstructorBodyCXX(self, JNIObjectName):
		str=self.__getConstructorWhichInstanciateTheNewObject(JNIObjectName)
		str+=self.__getConstructorWhichUsesAnAlreadyExistingJObject()
		return str

	def __getConstructorProfileWhichInstanciateTheNewObject(self):
	  return """%s(%s * %s_)"""% (self.getName(), JNIFrameWork().getJNIEnvVariableType(), JNIFrameWork().getJNIEnvVariable())

  	def __getConstructorProfileWhichUsesAnAlreadyExistingJObject(self):
	  return """%s(%s * %s_, jobject *JObj)"""% (self.getName(), JNIFrameWork().getJNIEnvVariableType(), JNIFrameWork().getJNIEnvVariable())
  
	def getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject()
  
	def getConstructorWhichInstanciateTheNewObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichInstanciateTheNewObject()

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
			/**
			* Create a wrapping of the object from a JNIEnv.
			* It will call the default constructor
			* @param JEnv_ the Java Env
			*/
			%s
			/**
			* Create a wrapping of an already existing object from a JNIEnv.
			* The object must have already been instantiated
			* @param JEnv_ the Java Env
			* @param JObj the object
			*/
			%s
			// Methods
			%s
			
			};

			""" % (self.getName(),  JNIFrameWork().getJNIEnvVariableType(), JNIFrameWork().getJNIEnvVariable(), self.getConstructorWhichInstanciateTheNewObjectHeaderCXX(), self.getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(), self.getMethodsCXX())

	def generateCXXBody(self, packageName):
		JNIObjectName=packageName+"/"+self.getName()
		return """%s
		%s
			""" % (self.getConstructorBodyCXX(JNIObjectName), self.getMethodsCXX("body"))
