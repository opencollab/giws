/*
Copyright or © or Copr. INRIA/Scilab - Sylvestre LEDRU
#
Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>

This software is a computer program whose purpose is to generate C++ wrapper 
for Java objects/methods.

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use, 
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info". 

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability. 

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or 
data to be ensured and,  more generally, to use and operate it in the 
same conditions as regards security. 

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

For more information, see the file COPYING
*/

#include <iostream>
#include <jni.h>
#include "example3.hxx"
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

using namespace example3;
using namespace std;

int main(){
	int sizeArray=3;
  	JavaVM* jvm = create_vm();
	MyObjectWhichReturnsExceptions *plop = new MyObjectWhichReturnsExceptions(jvm);

	int myInts = plop->getIntFromArrayOfSizeThree(0);
	cout << "Value from the Java with good pos : " << myInts << endl;

	cout << "========================" << endl;

	cout << "Exception catched:" << endl;
	try {
		int myIntsWithExceptionCatched = plop->getIntFromArrayOfSizeThree(22);
		
	}catch(GiwsException::JniException e) {
		cout << "getJavaDescription: " << e.getJavaDescription() << endl;
		cout << "getJavaStackTrace: " << e.getJavaStackTrace() << endl;
		cout << "getJavaExceptionName: " << e.getJavaExceptionName() << endl;
	}

	cout << "========================" << endl;

	cout << "Exception will be trigger. This will display the message of the exception" << endl;
	try {
		int value = plop->thisMethodWillFailWithMessage();
	}catch(GiwsException::JniException e) {
		cout << "getJavaDescription: " << e.getJavaDescription() << endl;
		cout << "getJavaStackTrace: " << e.getJavaStackTrace() << endl;
		cout << "getJavaExceptionName: " << e.getJavaExceptionName() << endl;
	}

	cout << "========================" << endl;

	cout << "Exception not catched:" << endl;
	int myIntsWithException = plop->getIntFromArrayOfSizeThree(223);
	cout << "Value from the Java with good pos : " << myInts  <<endl;

	return 0;	
}
