package bytebuffer;

public class ByteBufferSync {
	
	public ByteBufferSync(){
		System.out.println("Constructor");
	}

    static public void bar(java.nio.DoubleBuffer aze) {
        System.out.println("Into bar(java.nio.DoubleBuffer)");
        System.out.println("The input argument: "+ aze);

    }

    public static java.nio.DoubleBuffer myfun() {
        java.nio.DoubleBuffer buf = java.nio.ByteBuffer.allocateDirect(2 * 8).order(java.nio.ByteOrder.nativeOrder()).asDoubleBuffer();
        buf.put(new double[]{3.14159, 2.71828});
        return buf;
    }
}

