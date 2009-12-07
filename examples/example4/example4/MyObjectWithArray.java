/*
Copyright INRIA/Scilab - Sylvestre LEDRU
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

package example4;

public class MyObjectWithArray{
	
	public MyObjectWithArray(){
		System.out.println("Constructor");
	}

	public String[][] getMatrixString(){
		String[][] arrayOfString={{ "I do love Scilab","Don't you ?" },{"third","fourth"}};
		return arrayOfString;
	}
	

	public boolean[][] getArrayOfBoolean(){
		return new boolean[][]{{true,false,true},{false,true,false}};
	}

	public int[][] getMatrixInts(){
		int[][] arrayOfInt={{1,42,2},{2,84,4}};
		return arrayOfInt;
	}

	public void doNothingPleaseButDisplay(int[][] a){
		System.out.println("Your first array has a size of ["+a.length+","+a[0].length+"] elements");
        for(int i=0; i<a.length; i++) {
			for (int j=0; j<a[0].length; j++) {
				System.out.println("I did display some very interesting things like the int Array : "+a[i][j]);
			}
		}
	}

	public void displayMatrixOfString(String[][] a){
		System.out.println("Your first array has a size of ["+a.length+","+a[0].length+"] elements");
        for(int i=0; i<a.length; i++) {
			for (int j=0; j<a[0].length; j++) {
				System.out.println("I did display some very interesting things like the int Array : "+a[i][j]);
			}
		}
	}

}
