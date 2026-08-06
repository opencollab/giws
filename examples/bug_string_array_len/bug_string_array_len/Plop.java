package bug_string_array_len;

public class Plop {
    /* Returns null on purpose: the length out-parameter of the generated
     * wrapper must be set to 0 in this case (issue #10). */
    public static String[] getStrings() {
        return null;
    }
}
