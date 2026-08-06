#include <iostream>
#include "bug_string_array_len.hxx"
#include <jni.h>
/*
Regression test for issue #10: when a Java method returning String[]
returns null, the length out-parameter used to be left uninitialized.
It must be set to 0.
*/

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

using namespace bug_string_array_len;
using namespace std;

int main(){
	JavaVM* jvm = create_vm();

	/* Sentinel value: must be overwritten with 0 by the wrapper. */
	int lenRow = 42;
	char** res = Plop::getStrings(jvm, &lenRow);

	if (res != NULL) {
		cerr << "FAILED: expected a NULL result" << endl;
		return 1;
	}
	if (lenRow != 0) {
		cerr << "FAILED: lenRow not initialized to 0 (got " << lenRow << ")" << endl;
		return 1;
	}
	cout << "OK: NULL String[] returned with lenRow == 0" << endl;
	return 0;
}
