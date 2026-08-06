package bug_nonstatic_exception;

public class MyThrowingObject {

	public void alwaysThrows() {
		throw new IllegalStateException("thrown from a non-static method");
	}
}
