package bytebuffer;

public class MyObj {
	
	public MyObj(){
		System.out.println("Constructor");
	}

    static public void bar(java.nio.DoubleBuffer aze) {

    }

	public String[] getMyString(){
		String[] arrayOfString={ "I do love Scilab","Don't you ?" };
		return arrayOfString;
	}
	

	public int[] getMyInts(){
		int[] arrayOfInt={1,42,2};
		return arrayOfInt;
	}

	public void doNothingPleaseButDisplay(int[] a, short[] b){
		System.out.println("Your first array has a size of "+a.length+" elements and the second " +b.length);
        for(int i=0; i<a.length; i++)
			System.out.println("I did display some very interesting things like the int Array : "+a[i]);
        for(int i=0; i<b.length; i++)
			System.out.println("I did display some very uninteresting things like the short Array : "+b[i]);
	}

	public void setMyStrings(String[] a){
        for(int i=0; i<a.length; i++){
			System.out.println("Setting "+a[i]);
		}
	}


	public boolean[] dealingWithBooleans(boolean[] a){
        for(int i=0; i<a.length; i++){
			a[i]=!a[i];
		}
		return a;
	}


	public static void main(String []args){
		MyObj plop = new MyObj();
		plop.getMyString();
	}
}

