package com.myapp;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UtilTest {

    @Test
    public void testAdd() {
        int result = Util.add(2, 3);
        assertEquals(5, result);
    }

    @Test
    public void testSubtract() {
        int result = Util.subtract(5, 3);
        assertEquals(2, result);
    }

    @Test
    public void testMultiply() {
        int result = Util.multiply(2, 3);
        assertEquals(6, result);
    }

    @Test
    public void testDivide() {
        int result = Util.divide(6, 3);
        assertEquals(2, result);
    }
}