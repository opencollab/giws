#!/usr/bin/python -u
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
#
# This software is a computer program whose purpose is to generate C++ wrapper#!/usr/bin/python -u
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
#
# This software is a computer program whose purpose is to generate C++ wrapper
# for Java objects/methods.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software. You can  use,
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

""" Engine to create the C++/JNI exception files """
from licenseWrapper import licenseWrapper
from JNIFrameWork import JNIFrameWork
from outputWriter import outputWriter


class CXXException:

    package = None

    def getDescriptionHeader(self, config):
        return """/* Generated by GIWS (version %s) */	""" % (config.getVersion())

    # Header of the Exception file
    def getCXXHeader(self, config, objectName=""):
        defineHeader = config.getExceptionFileName()
        return """%s
		%s
		%s#include <exception>

		%s

		namespace %s {
		""" % (self.getDescriptionHeader(config), licenseWrapper().getLicense(), JNIFrameWork().getHeader(defineHeader), JNIFrameWork().getDLLExportSyntax(), config.getExceptionFileName())

    # Build the whole code of the C++ Exception header
    def generateCXXHeader(self, config):
        strCommonEnd = """
		}
		#endif
		"""
        strHeader = """

		/**
		* Parent class for exceptions which may occure in JNI code.
		*/
		class GIWSEXPORT JniException : public std::exception
		{

			/** Error message to display */
			std::string m_oErrorMessage;

			/** Java description of the exception*/
			std::string m_oJavaMessage;

			/** Java stackTrace when the exception occurred */
			std::string m_oJavaStackTrace;

			/** Name of the exception (ie class name).*/
			std::string m_oJavaExceptionName;

			/** The exception itself ... we store as a member otherwise JNI
			complains about 'WARNING in native method: JNI call made with
			exception pending' */
			jthrowable javaException;

			public:

			/**
			* Each subclass of JniExcpetion should call the super constructor
			* and the setErrorMessage function to set the message.
			* @param curEnv java environment where the exception occurred.
			*/
			JniException(JNIEnv * curEnv) throw() ;
			JniException() throw() : exception() { };


			virtual ~JniException(void) throw();

			/**
			* @return a description of the exception
			* @deprecated This function could lead to side effect error. Please use whatStr
			*/
			virtual const char * what(void) const throw();

			/**
			* @return a description of the exception
			*/
			virtual std::string whatStr(void) const throw();

			/**
			* @return Java description of the exception.
			*/
			std::string getJavaDescription(void) const throw();

			/**
			* @return Java stack trace where the exception occurred.
			*/
			std::string getJavaStackTrace(void) const throw();

			/**
			* Get the name of the exception (ie its class name).
			*/
			std::string getJavaExceptionName(void) const throw();

			protected:

			/**
			* Set the error message that the exception should print.
			*/
			void setErrorMessage(const std::string & errorMessage);

			/**
			* Get the message that the exception will print.
			*/
			std::string getErrorMessage(void) const;

			private:
			  /**
			* @return error message of the exception.
			*/
			std::string retrieveExceptionMessage(JNIEnv * curEnv);
			/**
			* @return full stack trace when the exception occurred.
			*/
			std::string retrieveStackTrace(JNIEnv * curEnv);

			/**
			* @return string containing the name of the exception (ie its class name).
			*/
			std::string retrieveExceptionName(JNIEnv * curEnv);
			/**
			* To be called when all the information about the exceptions have been
			* retrieved.
			* Remove the exception from the environment.
			*/
			void closeException(JNIEnv * curEnv);

			/**
			* Convert a Java string (jstring) into a C++ string
			*/
			std::string convertJavaString(JNIEnv * curEnv, jstring javaString);
			};

			/**
			* Exception that should be thrown when allocation of Java resources from C++
			* code fails (sur as NewDoubleArray or NewStringUTF).
			*/
			class GIWSEXPORT JniBadAllocException : public JniException
			{
			public:

			JniBadAllocException(JNIEnv * curEnv) throw();
			virtual ~JniBadAllocException(void) throw();
			};

			/**
			* Exception that should be thrown when a call to a Java method
			* using Jni throw an exception.
			* If possible, user should try to avoid this sitution because of the loss
			* of information.
			*/
			class GIWSEXPORT JniCallMethodException : public JniException
			{
			public:

			  /**
			   * @param curEnv java envirnonment where the exception occurred.
			   */
			  JniCallMethodException(JNIEnv * curEnv) throw();

			  virtual ~JniCallMethodException(void) throw();
			};

			/**
				* Exception that should be thrown when Jni code could not find a Java class
				*/
			class GIWSEXPORT JniClassNotFoundException : public JniException
			{
			public:

			/**
			* @param className name of the class which haven't been found
			*/
			JniClassNotFoundException(JNIEnv * curEnv, const std::string & className) throw();

			virtual ~JniClassNotFoundException(void) throw();

			};

			/**
			* Exception that should be thrown when Jni code could not find a Java method
			*/
			class GIWSEXPORT JniMethodNotFoundException : public JniException
			{
			public:

			/**
			* @param className name of the method which haven't been found
			*/
			JniMethodNotFoundException(JNIEnv * curEnv, const std::string & methodName) throw();
			virtual ~JniMethodNotFoundException(void) throw();

			};

			/**
			* Exception that should be thrown when a call to a Java method
			* using Jni throw an exception.
			* If possible, user should try to avoid this sitution because of the loss
			* of information.
			*/
			class GIWSEXPORT JniObjectCreationException : public JniException
			{
			public:

			/**
			* @param curEnv java envirnonment where the exception occurred.
			*/
			JniObjectCreationException(JNIEnv * curEnv, const std::string & className) throw();
			virtual ~JniObjectCreationException(void) throw();

			};


			/**
			* Exception that should be thrown when a call to the Java monitor
			* failed
			*/
			class GIWSEXPORT JniMonitorException : public JniException
			{
			public:

			/**
			* @param curEnv java envirnonment where the exception occurred.
			*/
			JniMonitorException(JNIEnv * curEnv, const std::string & className) throw();
			virtual ~JniMonitorException(void) throw();

			};
		"""

        str = """%s
		%s
		%s
		""" % (self.getCXXHeader(config), strHeader, strCommonEnd)
        fileName = config.getExceptionFileName(
        ) + config.getCPPHeaderExtension()
        outputWriter().writeIntoFile(config.getOutput(), fileName, str)
        print(("%s generated ..." % fileName))

    # Build the whole code of the C++ Exception Body
    def generateCXXBody(self, config):
        strCommon = """%s
		%s
		%s
		namespace %s {
		""" % (self.getDescriptionHeader(config), licenseWrapper().getLicense(), """#include "%s" """ % (config.getExceptionFileName() + config.getCPPHeaderExtension()), config.getExceptionFileName())

        strCommonEnd = """
		}
		"""

        strBody = """

		/**
		* Each subclass of JniExcpetion should call the super constructor
		* and the setErrorMessage function to set the message.
		* @param curEnv java envirnonment where the exception occurred.
		*/
		JniException::JniException(JNIEnv * curEnv) throw() : exception()
		{
		// retrieve information about the exception
		javaException = curEnv->ExceptionOccurred();
		/* Clear the Java Exception to avoid calling it again & again */
		curEnv->ExceptionClear();
		m_oJavaMessage = this->retrieveExceptionMessage(curEnv);
		m_oJavaStackTrace = this->retrieveStackTrace(curEnv);
		m_oJavaExceptionName = this->retrieveExceptionName(curEnv);

		// by default JniExceptions display the stack trace
		setErrorMessage(m_oJavaMessage + "\\n" + m_oJavaStackTrace);
		curEnv->DeleteLocalRef(javaException);
		closeException(curEnv);
		}

		JniException::~JniException(void) throw()
		{
		m_oErrorMessage.clear();
		}

		/**
		* @return a description of the exception
		* @deprecated This function could lead to side effect error. Please use whatStr
		*/
		const char * JniException::what(void) const throw()
		{
		return m_oErrorMessage.c_str();
		}

		/**
		* @return a description of the exception
		*/
		std::string JniException::whatStr(void) const throw()
		{
		return m_oErrorMessage;
		}

		/**
		* @return Java description of the exception.
		*/
		std::string JniException::getJavaDescription(void) const throw()
		{
		return m_oJavaMessage;
		}

		/**
		* @return Java stack trace where the exception occurred.
		*/
		std::string JniException::getJavaStackTrace(void) const throw()
		{
			return m_oJavaStackTrace;
			}

		/**
		* Get the name of the exception (ie its class name).
		*/
		std::string JniException::getJavaExceptionName(void) const throw()
		{
			return m_oJavaExceptionName;
			}


		/**
		* Set the error message that the exception should print.
		*/
		void JniException::setErrorMessage(const std::string & errorMessage)
		{
			m_oErrorMessage = errorMessage;
			}

		/**
			* Get the message that the exception will print.
		*/
		std::string JniException::getErrorMessage(void) const
		{
			return m_oErrorMessage;
			}

		/**
		* @return error message of the exception.
		*/
		std::string JniException::retrieveExceptionMessage(JNIEnv * curEnv)
		{
			// return the result of the getLocalizedMessage method

			// retrieve information from the exception.
			// get method id
			jmethodID getLocalizedMessageId = curEnv->GetMethodID(curEnv->GetObjectClass(javaException),
											   "getLocalizedMessage",
											   "()Ljava/lang/String;");

			// call getLocalizedMessage
			jstring description = (jstring) curEnv->CallObjectMethod(javaException, getLocalizedMessageId);

	if (description == NULL)
	{
	  return "";
	}

	std::string res = convertJavaString(curEnv, description);

	// release java resources
	curEnv->DeleteLocalRef(description);

	return res;
  }

  /**
   * @return full stack trace when the exception occurred.
   */
  std::string JniException::retrieveStackTrace(JNIEnv * curEnv)
  {


	// return the result of the getStackTrace method

	// retrieve information from the exception.
	// get method id
	// getStackTrace returns an array of StackTraceElement
	jmethodID getStackTraceId = curEnv->GetMethodID(curEnv->GetObjectClass(javaException),
													"getStackTrace",
													"()[Ljava/lang/StackTraceElement;");

	// call getStackTrace
	jobjectArray stackTrace = (jobjectArray) curEnv->CallObjectMethod(javaException, getStackTraceId);

	if (stackTrace == NULL)
	{
	  return "";
	}

	// get length of the array
	jsize stackTraceLength = curEnv->GetArrayLength(stackTrace);
	std::string res = "";

	// get toString methodId of StackTraceElement class
	jclass stackTraceElementClass = curEnv->FindClass("java/lang/StackTraceElement");
	jmethodID toStringId = curEnv->GetMethodID(stackTraceElementClass, "toString", "()Ljava/lang/String;");

	for (jsize i = 0; i < stackTraceLength; i++)
	{
	  // add the result of toString method of each element in the result
	  jobject curStackTraceElement = curEnv->GetObjectArrayElement(stackTrace, i);

	  // call to string on the object
	  jstring stackElementString = (jstring) curEnv->CallObjectMethod(curStackTraceElement, toStringId);

	  if (stackElementString == NULL)
	  {
		curEnv->DeleteLocalRef(stackTraceElementClass);
		curEnv->DeleteLocalRef(stackTrace);
		curEnv->DeleteLocalRef(curStackTraceElement);
		return res;
	  }

	  // add a line to res
	  res += " at " + convertJavaString(curEnv, stackElementString) + "\\n";

	  curEnv->DeleteLocalRef(curStackTraceElement);
	  curEnv->DeleteLocalRef(stackElementString);
	}

	// release java resources
	curEnv->DeleteLocalRef(stackTraceElementClass);
	curEnv->DeleteLocalRef(stackTrace);


	return res;
  }

  /**
   * @return string containing the name of the exception (ie its class name).
   */
  std::string JniException::retrieveExceptionName(JNIEnv * curEnv)
  {

	// then get its class
	jclass exceptionClass = curEnv->GetObjectClass(javaException);

	// get the Class class
	// we could also use curEnv->FindClass("Class");
	jclass classClass = curEnv->GetObjectClass(exceptionClass);

	// get the getName method
	jmethodID getNameId = curEnv->GetMethodID(classClass, "getName", "()Ljava/lang/String;");

	// call the getName function
	jstring javaName = (jstring) curEnv->CallObjectMethod(exceptionClass, getNameId);

	if (javaName == NULL)
	{
	  return "";
	}

	std::string res = convertJavaString(curEnv, javaName);

	// release java resources
	curEnv->DeleteLocalRef(exceptionClass);
	curEnv->DeleteLocalRef(classClass);
	curEnv->DeleteLocalRef(javaName);

	return res;
  }

  /**
   * To be called when all the information about the exceptions have been
   * retrieved.
   * Remove the exception from the environment.
   */
  void JniException::closeException(JNIEnv * curEnv)
  {
	// remove the exception from the environment
	// Beware, the exception is no longer reachable
	curEnv->ExceptionClear();
  }

  /**
   * Convert a Java string (jstring) into a C++ string
   */
  std::string JniException::convertJavaString(JNIEnv * curEnv, jstring javaString)
  {
	// get a pointer on a C string
	const char * tempString = curEnv->GetStringUTFChars(javaString, 0);

	// convert the C string into a C++ string
	std::string res(tempString);

	// release pointer
	curEnv->ReleaseStringUTFChars(javaString, tempString);

	return res;
  }


  /**
  * Exception that should be thrown when allocation of Java resources from C++
  * code fails (sur as NewDoubleArray or NewStringUTF).
  */

  JniBadAllocException::JniBadAllocException(JNIEnv * curEnv) throw() : JniException()
  {
  std::string message = "Error no more memory.";
  setErrorMessage(message);
  }

  JniBadAllocException::~JniBadAllocException(void) throw() {}


  /**
  * Exception that should be thrown when a call to a Java method
  * using Jni throw an exception.
  * If possible, user should try to avoid this sitution because of the loss
  * of information.
  */

  /**
  * @param curEnv java environment where the exception occurred.
  */
  JniCallMethodException::JniCallMethodException(JNIEnv * curEnv) throw() : JniException(curEnv)
  {
  std::string errorMessage = "Exception when calling Java method : ";
  errorMessage += getJavaDescription() + "\\n" + getJavaStackTrace();
  errorMessage += what();
  setErrorMessage(errorMessage);
  }

  JniCallMethodException::~JniCallMethodException(void) throw() {}
  /**
  * @param className name of the class which haven't been found
  */
  JniClassNotFoundException::JniClassNotFoundException(JNIEnv * curEnv, const std::string & className) throw() : JniException(curEnv)
			  {
				std::string errorMessage = "Could not get the Class " + className + ".";
				setErrorMessage(errorMessage);
			  }

			  JniClassNotFoundException::~JniClassNotFoundException(void) throw() {}

			  /**
			   * @param className name of the method which haven't been found
			   */
			  JniMethodNotFoundException::JniMethodNotFoundException(JNIEnv * curEnv, const std::string & methodName) throw() : JniException(curEnv)
			  {
				std::string errorMessage = "Could not access to the method " + methodName + ".";
				setErrorMessage(errorMessage);
			  }

			  JniMethodNotFoundException::~JniMethodNotFoundException(void) throw() {}

			  /**
			   * @param curEnv java envirnonment where the exception occurred.
			   */
			  JniObjectCreationException::JniObjectCreationException(JNIEnv * curEnv, const std::string & className) throw() : JniException(curEnv)
			  {
				std::string errorMessage = "Could not instantiate the object " + className + ".";
				setErrorMessage(errorMessage);
			  }

			  JniObjectCreationException::~JniObjectCreationException(void) throw() {}

			  /**
			   * @param curEnv java envirnonment where the exception occurred.
			   */
			  JniMonitorException::JniMonitorException(JNIEnv * curEnv, const std::string & className) throw() : JniException(curEnv)
			  {
				std::string errorMessage = "Error in the access (Enter or exit) or a Java env monitor of class " + className + ".";
				setErrorMessage(errorMessage);
			  }

			  JniMonitorException::~JniMonitorException(void) throw() {}

			"""

        str = """%s
		%s
		%s
		""" % (strCommon, strBody, strCommonEnd)

        fileName = config.getExceptionFileName() + config.getCPPBodyExtension()
        outputWriter().writeIntoFile(config.getOutput(), fileName, str)
        print(("%s generated ..." % fileName))
