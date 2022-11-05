package com.gradescope.anagram; // DO NOT MODIFY PACKAGE NAME OR CLASS NAME

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;

public class Anagram {

  // The type of the dictionary variable can be of your choice.
  private ArrayList<String> dictionary;
	
  // Load dictionary.txt on class load
	public Anagram(String dictionaryFilename) {
    	this.dictionary = loadDictionary(dictionaryFilename);
	}
	
    // Read the dictionary file into some data structure of your choice. ArrayList is given as an example.
	public ArrayList<String> loadDictionary(String filename) {
		// You can use any other data structure as well, provided you build it from scratch 
		// or use some primitive data structure like list.
		ArrayList<String> dictionary = new ArrayList<String>();
		try {
			// Read the file here.
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return dictionary;
	}
	
	
	/**
   * Implement the algorithm here. Do not change the function signature.
   * The return type should be ArrayList<ArrayList<String>>, so that Gradescope can read your output.
   * Your output need not be sorted.
   * 
   * @returns - List of anagram classes, where each element in the list is a list of all the words in that anagram class.
	 */
	public ArrayList<ArrayList<String>> getAnagrams(){
		ArrayList<ArrayList<String>> anagrams = new ArrayList<ArrayList<String>>();

		return anagrams;
	}
	
	
	/**
   * You can use this method for testing and debugging if you wish.
	 */
	public static void main(String[] args) {
    	Anagram pf = new Anagram("dictionary.txt");
    	pf.getAnagrams();
	}

}
