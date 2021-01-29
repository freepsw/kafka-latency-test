package com.pgx.java.socket;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
public class MyFileReader {
    public byte[] readFile(String fileName) throws IOException {
        File file = new File(fileName);
        byte[] fileData = new byte[(int)file.length()];
        BufferedInputStream br = new BufferedInputStream(new FileInputStream(file));

        int bytesRead = 0;
        int b;
        while ((b = br.read()) != -1) {
            fileData[bytesRead++] = (byte)b;
        }

        br.close();
        return fileData;
    }

    /**
     * For testing:
     *    args[0] = Name of binary file to read into memory.
     */
    public static void main(String[] args) throws IOException {
        //
        // Read file into byte array and print its size
        //
        byte[] data = new MyFileReader().readFile(args[0]);
        System.out.println("size: " + data.length);
    }
}