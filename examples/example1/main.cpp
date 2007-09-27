#include <iostream>
#include "example.hxx"
#include <jni.h>

JNIEnv* create_vm() {
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
	return env;
}

using namespace example;
using namespace std;

int main(){
  	JNIEnv* env = create_vm();
	MyObject *plop = new MyObject(env);
	cout << "A string from Java :" << plop->GetMyString() <<endl;
	plop->DoNothingPleaseButDisplay(23);

	return 0;	
}
