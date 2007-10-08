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
		std::cerr << "Could not instantiate the object " << className << " with the constructor : " << construct << param << std::endl;
		exit(EXIT_FAILURE);
		}
		 
		this->instance = curEnv->NewGlobalRef(localInstance) ;
		if(this->instance == NULL){
		std::cerr << "Could not create a new global ref of " << className << std::endl;
		exit(EXIT_FAILURE);
		}
                /* Methods ID set to NULL */
		%s
		
		}
		"""%(self.getName(), self.__getConstructorProfileWhichInstanciateTheNewObject(), JNIObjectName, str)

		
	def __getConstructorWhichUsesAnAlreadyExistingJObject(self):
		### Init the list of the cache of methodID
		str=""
		for method in self.__methods:
			str+="""%s=NULL; 
			"""%method.getUniqueNameOfTheMethod()
			
		return """
		%s::%s {
        jvm=jvm_;

        JNIEnv * curEnv = getCurrentEnv();

        this->instanceClass = (jclass) curEnv->NewGlobalRef(curEnv->GetObjectClass(JObj));
        if (this->instanceClass == NULL) {
               std::cerr << "Could not create a Global Ref of " << this->instanceClass <<  std::endl;
               exit(EXIT_FAILURE);
        }

        this->instance = curEnv->NewGlobalRef(JObj) ;
        if(this->instance == NULL){
               std::cerr << "Could not create a new global ref of " << this->instanceClass << std::endl;
               exit(EXIT_FAILURE);
        }
        /* Methods ID set to NULL */
        %s

}
		"""%(self.getName(), self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject(), str)

		
	def getConstructorBodyCXX(self, JNIObjectName):
		str=self.__getConstructorWhichInstanciateTheNewObject(JNIObjectName)
		str+=self.__getConstructorWhichUsesAnAlreadyExistingJObject()
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
			* Get the environment matching to the current thread.
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
			*/
			%s

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

			""" % (self.getName(),  JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable(), self.getMethodsProfileForMethodIdCache(), self.getConstructorWhichInstanciateTheNewObjectHeaderCXX(),self.getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(),self.getName(), self.getMethodsCXX()) 

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
