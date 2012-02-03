
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
    long long arrL[2]={2.2, 42};
    plop->bar(jvm, arr, 2, arrL, 2);

    int size = 0;
    double * ret = plop->myfun(jvm, &size);
    printf("C/C++ display: size=%d, ret[0]=%f, ret[1]=%f\n",size,ret[0],ret[1]);
    long long * retL = plop->myfunLong(jvm, &size);
    cout << "C/C++ display: size=" << size << "  retL[0]=" << retL[0] << " retL[1]="  << retL[1] << " retL[2]=" << retL[2] << endl;
    return 0;
}
