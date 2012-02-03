package bytebuffer;

public class ByteBufferSync {
	
	public ByteBufferSync(){
		System.out.println("Constructor");
	}

    static public void bar(java.nio.DoubleBuffer aze, java.nio.LongBuffer bze) {
        System.out.println("Into bar(java.nio.DoubleBuffer, java.nio.LongBuffer)");
        System.out.println("The input argument: "+ aze);
        System.out.println("The second input argument: "+ bze);

    }

    public static java.nio.DoubleBuffer myfun() {
        java.nio.DoubleBuffer buf = java.nio.ByteBuffer.allocateDirect(2 * 8).order(java.nio.ByteOrder.nativeOrder()).asDoubleBuffer();
        buf.put(new double[]{3.14159, 2.71828});
        return buf;
    }

    public static java.nio.LongBuffer myfunLong() {
        java.nio.LongBuffer buf = java.nio.ByteBuffer.allocateDirect(3 * 8).order(java.nio.ByteOrder.nativeOrder()).asLongBuffer();
        long[] array = new long[] {42, 6545555, 787867};
        buf.put(array);
        return buf;
    }
}

