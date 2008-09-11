package example3;

public class MyObjectWhichReturnsExceptions{
	
	public MyObjectWhichReturnsExceptions(){
		System.out.println("Constructor");
	}

	public int getIntFromArrayOfSizeThree(int pos){
		int[] arrayOfInt={42,12,69};
		return arrayOfInt[pos];
	}
	
	public static void main(String []args){
		MyObjectWhichReturnsExceptions plop = new MyObjectWhichReturnsExceptions();
		plop.getIntFromArrayOfSizeThree(23);
		plop.getIntFromArrayOfSizeThree(1);

	}
}
