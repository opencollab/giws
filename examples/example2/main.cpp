#include <iostream>
#include "example2.hxx"
#include <jni.h>

JavaVM* create_vm() {
	JavaVM* jvm;
	JNIEnv* env;
	JavaVMInitArgs args;
	JavaVMOption options[2];
	
	/* There is a new JNI_VERSION_1_4, but it doesn't add anything for the purposes of our example. */
	args.version = JNI_VERSION_1_4;

	args.nOptions = 2;
	options[0].optionString = "-Djava.class.path=.";
	options[1].optionString = "-Xcheck:jni";
	args.options = options;
	args.ignoreUnrecognized = JNI_FALSE;

	JNI_CreateJavaVM(&jvm, (void **)&env, &args);
	return jvm;
}

using namespace example2;
using namespace std;

int main(){
	int sizeArray=3;
  	JavaVM* jvm = create_vm();
	MyObjectWithArray *plop = new MyObjectWithArray(jvm);
	long myArrayOfLong[sizeArray];
	myArrayOfLong[0]=42;
	myArrayOfLong[1]=69;
	myArrayOfLong[2]=12;
	short myArrayOfShort[sizeArray+1];
	myArrayOfShort[0]=4;
	myArrayOfShort[1]=6;
	myArrayOfShort[2]=1;
	myArrayOfShort[3]=1;
	plop->doNothingPleaseButDisplay(myArrayOfLong,sizeArray,myArrayOfShort, sizeArray+1 );

	char ** myString=plop->getMyString();
	cout << "The first string from Java : " << myString[0]  <<endl;
	cout << "The second string from Java : " << myString[1]  <<endl;

	long *myInts=plop->getMyInts();
	cout << "The first int from Java : " << myInts[0]  <<endl;
	cout << "The second int from Java : " << myInts[1]  <<endl;
	cout << "The third int from Java : " << myInts[2]  <<endl;

	return 0;	
}
