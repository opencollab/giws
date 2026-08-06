/*
Regression test: before giws 3.1.0, the exception check after the Java
call was only generated for static methods. The Java exception thrown
by this non-static method was never converted into a C++ exception, so
the try/catch below did not catch anything and the program fell through
to the failure branch.
*/

#include <iostream>
#include <jni.h>
#include "bug_nonstatic_exception.hxx"
#include "GiwsException.hxx"

JavaVM* create_vm() {
	JavaVM* jvm;
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];

	args.version = JNI_VERSION_1_4;

	args.nOptions = 2;
	options[0].optionString = const_cast<char*>("-Djava.class.path=.");
	options[1].optionString = const_cast<char*>("-Xcheck:jni");
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;

	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

using namespace bug_nonstatic_exception;
using namespace std;

int main(){
	JavaVM* jvm = create_vm();
	MyThrowingObject *obj = new MyThrowingObject(jvm);

	try {
		obj->alwaysThrows();
	} catch (GiwsException::JniException & e) {
		cout << "Exception caught from a non-static method: "
		     << e.getJavaDescription() << endl;
		cout << "Exception name: " << e.getJavaExceptionName() << endl;
		delete obj;
		return 0;
	}

	cerr << "FAILED: the Java exception was not converted into a C++ exception" << endl;
	delete obj;
	return 1;
}
