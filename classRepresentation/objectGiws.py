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
		""" """

		### Init the list of the cache of methodID
		str=""
		for method in self.__methods:
			str+="""%s=NULL; 
			"""%method.getUniqueNameOfTheMethod()
			
		return """
		%s::%s {
		jmethodID constructObject = NULL ;
		jobject localInstance ;
		jclass localClass ;
		jclass instanceClass;
		const std::string className="%s";
		const std::string construct="<init>";
		const std::string param="()V";
		jvm=jvm_;

		JNIEnv * curEnv = getCurrentEnv();
		
		localClass = curEnv->FindClass( className.c_str() ) ;
		if (localClass == NULL) {
		std::cerr << "Could not get the Class " << className <<  std::endl;
		exit(EXIT_FAILURE);
		}
		
		this->instanceClass = (jclass) curEnv->NewGlobalRef(localClass) ;
		if (this->instanceClass == NULL) {
		std::cerr << "Could not create a Global Ref of " << className <<  std::endl;
		exit(EXIT_FAILURE);
		}
		
		constructObject = curEnv->GetMethodID( this->instanceClass, construct.c_str() , param.c_str() ) ;
		if(constructObject == NULL){
		std::cerr << "Could not retrieve the constructor of the class " << className << " with the profile : " << construct << param << std::endl;
		exit(EXIT_FAILURE);
		}
		
		localInstance = curEnv->NewObject( this->instanceClass, constructObject ) ;
		if(localInstance == NULL){
		std::cerr << "Could not instance the object " << className << " with the constructor : " << construct << param << std::endl;
		exit(EXIT_FAILURE);
		}
		 
		this->instance = curEnv->NewGlobalRef(localInstance) ;
		if(this->instance == NULL){
		std::cerr << "Could not create a new global ref of " << className << std::endl;
		exit(EXIT_FAILURE);
		}

		%s
		
		}
		"""%(self.getName(), self.__getConstructorProfileWhichInstanciateTheNewObject(), JNIObjectName, str)

		
	def __getConstructorWhichUsesAnAlreadyExistingJObject(self):
		return """
		%s::%s {

	this->instance = JEnv_->NewGlobalRef(JObj) ;
		this->instanceClass = (jclass) JEnv_->NewGlobalRef(JEnv_->GetObjectClass(JObj)) ;
if(this->instance == NULL){
std::cerr << "Could not create a new global ref " << std::endl;
exit(EXIT_FAILURE);
}
}
		"""%(self.getName(), self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject())

		
	def getConstructorBodyCXX(self, JNIObjectName):
		str=self.__getConstructorWhichInstanciateTheNewObject(JNIObjectName)
#		str+=self.__getConstructorWhichUsesAnAlreadyExistingJObject()
		return str

	def __getConstructorProfileWhichInstanciateTheNewObject(self):
	  return """%s(%s * %s_)"""% (self.getName(), JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable())

  	def __getConstructorProfileWhichUsesAnAlreadyExistingJObject(self):
	  return """%s(%s * %s_, jobject JObj)"""% (self.getName(), JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable())
  
	def getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject()
  
	def getConstructorWhichInstanciateTheNewObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichInstanciateTheNewObject()

	def getMethodsProfileForMethodIdCache(self):
		str=""
		for method in self.__methods:
			str+="""jmethodID %s; // cache method id
			"""%method.getUniqueNameOfTheMethod()
		return str
	
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
			jobject instance;
			
			jclass instanceClass; // cache class
			%s
			
			/**
			* Get the environmebnt matching to the current thread.
			*/
			JNIEnv * getCurrentEnv();
			
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
			* @TODO removed because don't remember with we did it :$
			*/
			
			// Destructor
			~%s();

			// Generic method
			// Synchronization methods
			/**
			* Enter monitor associated with the object.
			* Equivalent of creating a "synchronized(obj)" scope in Java.
			*/
			void synchronize();
			
			/**
			* Exit monitor associated with the object.
			* Equivalent of ending a "synchronized(obj)" scope.
			*/
			void endSynchronize();
					
			// Methods
			%s
			
			};

			""" % (self.getName(),  JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable(), self.getMethodsProfileForMethodIdCache(), self.getConstructorWhichInstanciateTheNewObjectHeaderCXX(),self.getName(), self.getMethodsCXX())
			#self.getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(), 

	def generateCXXBody(self, packageName):
		JNIObjectName=packageName+"/"+self.getName()
		return """
		// Returns the current env
		%s
		// Destructor
		%s
		// Constructors
		%s
		// Generic methods
		%s
		%s
		// Method(s)
		%s
			""" % (JNIFrameWork().getMethodGetCurrentEnv(self.getName()), JNIFrameWork().getObjectDestuctor(self.getName()), self.getConstructorBodyCXX(JNIObjectName), JNIFrameWork().getSynchronizeMethod(self.getName()) , JNIFrameWork().getEndSynchronizeMethod(self.getName()), self.getMethodsCXX("body"))
