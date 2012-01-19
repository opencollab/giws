
#include <iostream>
#include <jni.h>
#include "bytebuffer.hxx"
#include "GiwsException.hxx"

JavaVM* create_vm() {
	JavaVM* jvm;
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];
	
	/* There is a new JNI_VERSION_1_4, but it doesn't add anything for the purposes of our example. */
	args.version = JNI_VERSION_1_4;

	args.nOptions = 2;
	options[0].optionString = const_cast<char*>("-Djava.class.path=.");
	options[1].optionString = const_cast<char*>("-Xcheck:jni");
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;

	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

using namespace bytebuffer;

using namespace std;

int main(){
  	JavaVM* jvm = create_vm();
	ByteBufferSync *plop = new ByteBufferSync(jvm);
    double arr[2]={2.2, 42};
    plop->bar(jvm, arr, 2);
    return 0;
}
