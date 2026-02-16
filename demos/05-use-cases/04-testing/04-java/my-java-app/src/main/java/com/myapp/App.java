package com.myapp;

public class App {
    public static void main(String[] args) {
        System.out.println("java console started");        
        Util util = new Util();
        System.out.println("addition of 2 and 3 is: " + Util.add(2, 3));
    }
}