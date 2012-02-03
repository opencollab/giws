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
from datatypes.stringDataGiws import stringDataGiws
from configGiws import configGiws

class objectGiws:
	__name=""
	__methods=[]
	__stringClassSet=False
	# Which class it extends
	__extends=None

	def __init__(self, name):
		self.__name=name
		self.__methods=[]

	def __init__(self, name, extends):
		self.__name=name
		self.__methods=[]
		self.__extends=extends
		
	def addMethod(self, method):
		if isinstance(method,methodGiws):
			self.__methods.append(method)

	def getName(self):
		return self.__name

	def getMethods(self):
		return self.__methods

	def __getDeclarationOfCachingMethodID(self):
		### Init the list of the cache of methodID
		str=""
		stringClassSet=False
		for method in self.__methods:
			str+="""%s=NULL;
			"""%method.getUniqueNameOfTheMethod()

			for param in  method.getParameters():
				### Avoids to load the class String each time we need it
				if isinstance(param.getType(),stringDataGiws) and param.getType().isArray()==True and stringClassSet!=True and method.getModifier()!="static":
					str+="""
					jclass localStringArrayClass = curEnv->FindClass("java/lang/String");
					stringArrayClass = static_cast<jclass>(curEnv->NewGlobalRef(localStringArrayClass));
					curEnv->DeleteLocalRef(localStringArrayClass);
					"""
					stringClassSet=True

		if self.getExtendedClass()!=None:
			# Get the father object to work on it.
			str+=self.getExtendedClass().__getDeclarationOfCachingMethodID()

		return str
	
	def __getConstructorWhichInstanciateTheNewObject(self):
		""" """

		# Management of the error when the class cannot be found
		if configGiws().getThrowsException():
			errorMgntClass="""  throw %s::JniClassNotFoundException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntClass="""std::cerr << "Could not get the Class " << this->className() <<  std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""

		# Management of the error when the global ref could not be created
		if configGiws().getThrowsException():
			errorMgntCreation="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntCreation="""std::cerr << "Could not create a Global Ref of " << this->className() <<  std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""

		# Management of the error when it is not possible to retrieve the constructor
		if configGiws().getThrowsException():
			errorMgntConstructor="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntConstructor="""std::cerr << "Could not retrieve the constructor of the class " << this->className() << " with the profile : " << construct << param << std::endl;
		curEnv->ExceptionDescribe();
		exit(EXIT_FAILURE);"""

		# Management of the error when it is not possible instantiate the obj
		if configGiws().getThrowsException():
			errorMgntInstantiate="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntInstantiate="""std::cerr << "Could not instantiate the object " << this->className() << " with the constructor : " << construct << param << std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""

		# Management of the error when it is not possible create a global ref
		if configGiws().getThrowsException():
			errorMgntRef="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntRef="""std::cerr << "Could not create a new global ref of " << this->className() << std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""
			
		### Init the list of the cache of methodID
		strMethodID=self.__getDeclarationOfCachingMethodID()
		constructorProfile="""%s::%s"""%(self.getName(), self.__getConstructorProfileWhichInstanciateTheNewObject())
		if self.getExtendedClass()!=None:
			constructorProfile+=""" : %s(fakeGiwsDataType::fakeGiwsDataType())""" % (self.getExtendedClass().getName())


		return """%s {
		jmethodID constructObject = NULL ;
		jobject localInstance ;
		jclass localClass ;

		const std::string construct="<init>";
		const std::string param="()V";
		jvm=jvm_;

		JNIEnv * curEnv = getCurrentEnv();
		
		localClass = curEnv->FindClass( this->className().c_str() ) ;
		if (localClass == NULL) {
		%s
		}
		
		this->instanceClass = static_cast<jclass>(curEnv->NewGlobalRef(localClass));
		
		/* localClass is not needed anymore */
		curEnv->DeleteLocalRef(localClass);
		
		if (this->instanceClass == NULL) {
		%s
		}
		

		constructObject = curEnv->GetMethodID( this->instanceClass, construct.c_str() , param.c_str() ) ;
		if(constructObject == NULL){
		%s
		}
		
		localInstance = curEnv->NewObject( this->instanceClass, constructObject ) ;
		if(localInstance == NULL){
		%s
		}
		 
		this->instance = curEnv->NewGlobalRef(localInstance) ;
		if(this->instance == NULL){
		%s
		}
		/* localInstance not needed anymore */
		curEnv->DeleteLocalRef(localInstance);

                /* Methods ID set to NULL */
		%s
		
		}
		"""%(constructorProfile, errorMgntClass, errorMgntCreation, errorMgntConstructor, errorMgntInstantiate, errorMgntRef, strMethodID)

		
	def __getConstructorWhichUsesAnAlreadyExistingJObject(self):
		### Init the list of the cache of methodID
		strMethodID=self.__getDeclarationOfCachingMethodID()
		
		# Management of the error when the instance class could not be created a global ref
		if configGiws().getThrowsException():
			errorMgntRef="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntRef="""
			std::cerr << "Could not create a Global Ref of " << this->className() <<  std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""

		# Management of the error when the instance class could not be created a global ref
		if configGiws().getThrowsException():
			errorMgntNewRef="""throw %s::JniObjectCreationException(curEnv, this->className());"""%(configGiws().getExceptionFileName())
		else:
			errorMgntNewRef="""
			std::cerr << "Could not create a new global ref of " << this->className() << std::endl;
			curEnv->ExceptionDescribe();
			exit(EXIT_FAILURE);"""
		constructorProfile="""%s::%s"""%(self.getName(), self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject())
		if self.getExtendedClass()!=None:
			constructorProfile+=""" : %s(fakeGiwsDataType::fakeGiwsDataType()) """ % (self.getExtendedClass().getName())
		return """
		%s {
        jvm=jvm_;

        JNIEnv * curEnv = getCurrentEnv();

		jclass localClass = curEnv->GetObjectClass(JObj);
        this->instanceClass = static_cast<jclass>(curEnv->NewGlobalRef(localClass));
        curEnv->DeleteLocalRef(localClass);
		
        if (this->instanceClass == NULL) {
		%s
        }

        this->instance = curEnv->NewGlobalRef(JObj) ;
        if(this->instance == NULL){
		%s
        }
        /* Methods ID set to NULL */
        %s

}
		"""%(constructorProfile, errorMgntRef, errorMgntNewRef, strMethodID)
	
	# Returns the class the current one is extending
	# Returns None if not existing
	def getExtendedClass(self):
		return self.__extends
		
	def getConstructorBodyCXX(self):
		str=self.__getConstructorWhichInstanciateTheNewObject()
		str+=self.__getConstructorWhichUsesAnAlreadyExistingJObject()
		return str

	def __getConstructorProfileWhichInstanciateTheNewObject(self):
	  str="""%s(%s * %s_)"""% (self.getName(), JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable())
#	  if self.__extends!=None:
#		  str+=""": %s(fakeGiwsDataType::fakeGiwsDataType())"""%(self.__extends)
	  return str

  	def __getConstructorProfileWhichUsesAnAlreadyExistingJObject(self):
	  return """%s(%s * %s_, jobject JObj)"""% (self.getName(), JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable())
  
	def getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichUsesAnAlreadyExistingJObject()
  
	def getConstructorWhichInstanciateTheNewObjectHeaderCXX(self):
		return """%s;"""%self.__getConstructorProfileWhichInstanciateTheNewObject()

	def __getFakeConstructorForExtendedClasses(self):
		str=""
		if self.getExtendedClass()==None:
			# It is a potential master class, add the fake constructor
			str+="""
			/** 
			* This is a fake constructor to avoid the constructor
			* chaining when dealing with extended giws classes 
			*/
			#ifdef FAKEGIWSDATATYPE
			%s(fakeGiwsDataType::fakeGiwsDataType /* unused */) {}
			#endif
			"""%(self.getName())
			
		return str

	def getMethodsProfileForMethodIdCache(self):
		str=""
		stringClassSet=False
		for method in self.__methods:
			str+="""jmethodID %s; // cache method id
			"""%method.getUniqueNameOfTheMethod()
			for param in  method.getParameters():
				### Avoids to load the class String each time we need it
				if isinstance(param.getType(),stringDataGiws) and param.getType().isArray()==True and stringClassSet!=True:
					str+="""jclass stringArrayClass;
					"""
					stringClassSet=True
					self.__stringClassSet=True
		return str
	
	def getProtectedFields(self):
		str=""
		if self.getExtendedClass()==None:
			str+="""
			jobject instance;
			jclass instanceClass; // cache class
			"""
		
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
		
        def generateCXXHeader(self, packageName):
                JNIObjectName=packageName+"/"+self.getName()
                
		if self.getExtendedClass()==None:
			classProfile="""class GIWSEXPORT %s {""" % (self.getName())
		else:
			classProfile="""class GIWSEXPORT %s : public %s {
			""" % (self.getName(), self.getExtendedClass().getName())
		return """%s

			private:
			%s * %s;

			protected:
			%s

			%s
                       
			// Caching (if any)
			%s

			/**
			* Get the environment matching to the current thread.
			*/
			virtual JNIEnv * getCurrentEnv();

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
			
                        /**
                        * Get class name to use for static methods
                        * @return class name to use for static methods
                        */
                        %s
			};

			""" % (classProfile, JNIFrameWork().getJavaVMVariableType(), JNIFrameWork().getJavaVMVariable(), self.getMethodsProfileForMethodIdCache(), self.getProtectedFields(), self.getCacheBuffer(), self.getConstructorWhichInstanciateTheNewObjectHeaderCXX(),self.getConstructorWhichUsesAnAlreadyExistingJObjectHeaderCXX(),self.__getFakeConstructorForExtendedClasses(), self.getName(), self.getMethodsCXX(), self.getClassNameProfile(JNIObjectName)) 

	def generateCXXBody(self):
		return """
                // Static declarations (if any)
                %s
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
			""" % (self.getStaticVariableDeclaration(), JNIFrameWork().getMethodGetCurrentEnv(self.getName()), JNIFrameWork().getObjectDestuctor(self.getName(),stringClassSet=self.__stringClassSet), self.getConstructorBodyCXX(), JNIFrameWork().getSynchronizeMethod(self.getName()) , JNIFrameWork().getEndSynchronizeMethod(self.getName()), self.getMethodsCXX("body"))

        def getClassNameProfile(self, JNIObjectName):
                return """
                static const std::string className()
                {
                return "%s";
                }
                """ % (JNIObjectName)

        def needCaching(self):

                for method in self.__methods:
                        for param in  method.getParameters():
                                if param.getType().isByteBufferBased() == True:
                                        return True

                return False


        def getStaticVariableDeclaration(self):

                str=""
                if self.needCaching():
                        str="""
                // Cache of the bytebuffer stuff
                jclass ByteBufferSync::ByteOrderClass = NULL;
                jmethodID ByteBufferSync::nativeOrderID = NULL;
                jobject ByteBufferSync::nativeOrder = NULL;
                jmethodID ByteBufferSync::orderID = NULL;
                jclass ByteBufferSync::bbCls = NULL;
                jmethodID ByteBufferSync::asdbID = NULL;"""

                return str

        def getCacheBuffer(self):
                str=""
                if self.needCaching():
                        str="""
                // Cache of the bytebuffer stuff
                static jclass ByteOrderClass;
                static jmethodID nativeOrderID;
                static jobject nativeOrder;
                static jmethodID orderID;
                static jclass bbCls;
                static jmethodID asdbID;
                """
                return str
