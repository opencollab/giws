#include <iostream>
#include "example.hxx"
#include <jni.h>

JavaVM* create_vm() {
	JavaVM* jvm;
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];
	
	/* There is a new JNI_VERSION_1_4, but it doesn't add anything for the purposes of our example. */
	args.version = JNI_VERSION_1_6;

	args.nOptions = 2;
	options[0].optionString = "-Djava.class.path=.";
	options[1].optionString = "-Xcheck:jni";
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;
	
	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

using namespace example;
using namespace std;

int main(){
  	JavaVM* jvm = create_vm();
	MyObject *plop = new MyObject(jvm);
	cout << "A string from Java :" << plop->getMyString() <<endl;
	plop->doNothingPleaseButDisplay(23);
	cout << "Hashcode of my two strings " << plop->giveMeTheHashCodePlease("plop", "plop2") << endl;
	return 0;	
}
