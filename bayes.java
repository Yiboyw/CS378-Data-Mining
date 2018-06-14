import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/////////////////////////////////////////////////////////////////////////
//   NAIVE BAYESIAN CLASSIFIER ALGORITHM IMPLEMENTATION BY YIBO WANG
//   EMORY ID: ywan738
//   EMORY EMAIL: yibo.wang@emory.edu
//  I WORKED ON THIS PROJECT ALONE SO +5 BONUS POINTS TO THIS ASSIGNMENT
//////////////////////////////////////////////////////////////////////////

public class bayes {
	
	public static List<String[]> dataTraining = new ArrayList<String[]>(); //store the mushroom attributes for the training set
	public static List<String[]> dataTest = new ArrayList<String[]>(); //store the mushroom attributes for the testing set
	public static HashMap<String, Double> mapE = new HashMap<String, Double>();  //HashMap stores frequency list for mushroom attributes with class e
	public static HashMap<String, Double> mapP = new HashMap<String, Double>();  //HashMap stores frequency list for mushroom attributes with class p
	
    // ================================================================================================= //
    //                                          MAIN METHOD                                              //
    // ================================================================================================= //
    public static void main(String[] args) throws FileNotFoundException {
    		File training = new File(args[0]); //sets path file to training data set - "/Users/yibowang/Desktop/mushroom.training")	
    		File test = new File(args[1]);  //sets path file to testing data set - "/Users/yibowang/Desktop/mushroom.test")
    		
    		PrintStream program = new PrintStream(new File(args[2])); //the third command line argument is the name of output file
    		System.setOut(program); 
        
    		readtext(training);
        readtextTest(test);
        
        probability(dataTraining); //gets probability from the training set to predict testing set
        
        double accuracyCounter = 0;
        
        for(int j = 0; j < dataTest.size(); j++) {
    			String[] attribute = dataTest.get(j);
    			String result = classify(mapE, mapP, attribute);
    			
    			if(result.equals(attribute[0])){
    				accuracyCounter += 100;
    			}
    			program.println(classify(mapE, mapP, attribute));
    			//System.out.println(classify(mapE, mapP, attribute));
        }
        
        accuracyCounter = accuracyCounter/dataTest.size();
       	program.println("Accuracy " + accuracyCounter);
        //System.out.println("Accuracy " + accuracyCounter);
        
    }
    
    // ================================================================================================= //
 	// This method reads the mushroom text file and stores the attributes to the List<String[]> dataTraining //
 	// ================================================================================================= //	
 		public static void readtext(File file) throws FileNotFoundException
 		{
 			Scanner input = new Scanner(file);
 			
 			while (input.hasNextLine()) 
 			{
 				String attribute = input.nextLine(); //stores the line in the text file e.g. a b c d	
 				String[] parts = attribute.split("\t"); //splits the string number based on the tab space
 				
 				dataTraining.add(parts); //adds the array to the attributes    
 			}	
 		}
 		
 		// ================================================================================================= //
 	 	// This method reads the mushroom text file and stores the attributes to the List<String[]> dataTest //
 	 	// ================================================================================================= //	
 	 		public static void readtextTest(File file) throws FileNotFoundException
 	 		{
 	 			Scanner input = new Scanner(file);
 	 			
 	 			while (input.hasNextLine()) 
 	 			{
 	 				String attribute = input.nextLine(); //stores the line in the text file e.g. a b c d	
 	 				String[] parts = attribute.split("\t"); //splits the string number based on the tab space
 	 				
 	 				dataTest.add(parts); //adds the array to the attributes    
 	 			}	
 	 		}
 		
 		// ================================================================================================= //
 	 	// This method reads the mushroom text file and calculates the conditional probabilities             //
 	 	// ================================================================================================= //	
 		public static void probability(List<String[]> data) {
 			double count = 1;
 			int countP = 0; // count number of times the p class is used in the mushroom data set
 			int countE = 0; // count number of times the e class is used in the mushroom data set
 		 
 			//count the number of times each attribute appears
 			for(int i = 0; i < 22; i++) { 
 				for(int j =0; j< data.size(); j++) { 
 					
	    			String[] newString = data.get(j);
	    			String attribute = newString[i];
	    			
	    			String mushroomClass = newString[0];
	    			
	    			if(mushroomClass.equals("p")) {
	    				countP++;
	    				if(!mapP.containsKey(attribute)) {
	    					mapP.put(attribute, count);
	    				}
	    				
	    				else if(mapP.containsKey(attribute)) {
	    					double value = mapP.get(attribute);
	    					value++;
	    					mapP.put(attribute, value);
	    				}
	    			}
	    			
	    			else if (mushroomClass.equals("e")) {
	    				countE++;
	    				if(!mapE.containsKey(attribute)) {
	    					mapE.put(attribute, count);
	    				}
	    				
	    				else if(mapE.containsKey(attribute)) {
	    					double value = mapE.get(attribute);
	    					value++;				
	    					mapE.put(attribute, value);
	    				}
	    			}
	    			
 				}	
 			}	
 			//calculates the conditional probabilities of each attribute by dividing by the countE
 			for (Map.Entry<String, Double> entry : mapE.entrySet()) {     		
 	            String key = entry.getKey();
 	            double val = entry.getValue();
 	            double result = (val/countE);
 	            mapE.put(key, result);
 	        }
 			
 			//calculates the conditional probabilities of each attribute by dividing by the countP
 			for (Map.Entry<String, Double> entry : mapP.entrySet()) {     		
 	            String key = entry.getKey();
 	            double val = entry.getValue();
 	            double result = (val/countP);
 	            mapP.put(key, result);
 	        }
 		}
 		
 		// ================================================================================================= //
 	 	// This method classifies a mushroom attribute set and returns the mushroom class for the set       //
 	 	// ================================================================================================= //	
 		public static String classify(HashMap<String, Double> mapE, HashMap<String, Double> mapP, String[] attributes) {		
 			double eResult = 1;
 			double pResult = 1; 
 			
 			for(int i = 0; i < attributes.length; i++) {
 				eResult = eResult * mapE.get(attributes[i]);
 				pResult = pResult * mapP.get(attributes[i]);
 			}
 			
 			if (eResult > pResult ) {
 				return "e";
 			}
 			else  {
 				return "p";
 			}
 		}
}
