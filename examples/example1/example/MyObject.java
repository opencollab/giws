package example;

public class MyObject{
	
	public MyObject(){
		System.out.println("Constructor");
	}

	public String getMyString(){
		return "I do love Scilab";
	}
	
	public void doNothingPleaseButDisplay(int a){
		System.out.println("I did display some very interesting things like the int : "+a);
	}

	public int giveMeTheHashCodePlease(String a, String b){
		return a.hashCode()+b.hashCode();
	}
}
