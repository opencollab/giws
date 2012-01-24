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
#include "example4.hxx"
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

using namespace example4;
using namespace std;

int main(){
	int sizeArray=3, sizeArrayCol = 2, i, j;
  	JavaVM* jvm = create_vm();
	MyObjectWithArray *plop = new MyObjectWithArray(jvm);
	int **myArrayOfLong= (int**)malloc(sizeof(int) * sizeArray);//[sizeArray][sizeArrayCol];
	for (i = 0; i <= sizeArray; i++) {
		myArrayOfLong[i]=(int*) malloc(sizeof(int) * sizeArrayCol);
		myArrayOfLong[i][0]=2*(i+1);
		myArrayOfLong[i][1]=3*(i+1);
	}

	plop->doNothingPleaseButDisplay(myArrayOfLong,sizeArray,sizeArrayCol);
	int lenRow, lenCol;
	char *** myString=plop->getMatrixString(&lenRow, &lenCol);
	cout << "Going to get a String[" << lenRow << "][" << lenCol << "]" << endl;
	for (i = 0; i < lenRow; i++) {
		for (j = 0; j < lenCol; j++) {
			cout << "String from Java [" << i << "," << j << "] : " << myString[i][j]  <<endl;
		}
	}
	

	int **myInts=plop->getMatrixInts(&lenRow, &lenCol);
	cout << "From Java [0,0] : " << myInts[0][0]  <<endl;
	cout << "From Java [0,1] : " << myInts[0][1]  <<endl;
	cout << "From Java [0,2] : " << myInts[0][2]  <<endl;
	cout << "From Java [1,0] : " << myInts[1][0]  <<endl;
	cout << "From Java [1,1] : " << myInts[1][1]  <<endl;
	cout << "From Java [1,2] : " << myInts[1][2]  <<endl;

	bool **myBool=plop->getArrayOfBoolean(&lenRow, &lenCol);
	cout << "Bool from Java [0,0] : " << myBool[0][0]  <<endl;
	cout << "Bool from Java [0,1] : " << myBool[0][1]  <<endl;
	cout << "Bool from Java [0,2] : " << myBool[0][2]  <<endl;
	cout << "Bool from Java [1,0] : " << myBool[1][0]  <<endl;
	cout << "Bool from Java [1,1] : " << myBool[1][1]  <<endl;
	cout << "Bool from Java [1,2] : " << myBool[1][2]  <<endl;


	char ***sendToJava = new char **[2];
	sendToJava[0] = new char *[2];
	sendToJava[0][0]=(char*)"string1";
	sendToJava[0][1]=(char*)"string2";
	sendToJava[1] = new char *[2];
	sendToJava[1][0]=(char*)"string3";
	sendToJava[1][1]=(char*)"Final string";
	plop->displayMatrixOfString(sendToJava,2,2);

	return 0;	
}
