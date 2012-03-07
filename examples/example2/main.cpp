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
	options[0].optionString = const_cast<char*>("-Djava.class.path=.");
	options[1].optionString = const_cast<char*>("-Xcheck:jni");
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
	int myArrayOfLong[sizeArray];
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

	int *myInts=plop->getMyInts();
	cout << "The first int from Java : " << myInts[0]  <<endl;
	cout << "The second int from Java : " << myInts[1]  <<endl;
	cout << "The third int from Java : " << myInts[2]  <<endl;

	char *myStrings[]={(char*)"tic", (char*)"tac", (char*)"toc", (char*)"plop"};
	plop->setMyStrings(myStrings,4);

	bool arrayOfBool[]={true, false, true, true};
	bool *boolReturned = plop->dealingWithBooleans(arrayOfBool, 4);
	
	for (int i=0; i < 4; i++){
		cout << "Value " << i << " : " << boolReturned[i] << " (was " << arrayOfBool[i] << ")" << endl;
	}
	return 0;	
}
