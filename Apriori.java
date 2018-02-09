import java.util.*;
import java.util.Map.Entry;
import java.io.File;
import java.io.FileNotFoundException;

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
//             APRIORI ALGORITHM IMPLEMENTATION BY YIBO WANG            //              
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
public class Apriori {

	public static List<int[]> database = new ArrayList<int[]>(); //List database stores the transaction database of itemsets
	public static List<int[]> combination = new ArrayList<int[]>(); //List of int[] that stores all combinations
	public static List<ArrayList<Integer>> arraylist = new ArrayList<ArrayList<Integer>>(); //List of int[] that stores all combinations
	public static HashMap<ArrayList<Integer>, Integer> map = new HashMap<ArrayList<Integer>, Integer>();  //HashMap stores the item set and frequency list
	public static Set<Integer> distinctSet = new HashSet<Integer>(); //Set which stores the distinct elements in the database
	
	//database:
	/*	1 2 3 4
		2 3
		2 4 5
		1 2 3 5 
		1 5 3
		2 3 5
	*/
    // ================================================================================================= //
    //                                          MAIN METHOD                                              //
    // ================================================================================================= //
	public static void main(String[] args) throws FileNotFoundException
	{
		File file = new File("/Users/yibowang/Desktop/data.txt"); //path of the file 
		readtext(file); 
		int[] distinct = getdistinctItem(); //make sure distinctSet has all the distinct items in the itemset
		
		getPowerSetArrayList(distinct);
		supportCount(database, 1);
	
	}
	
	// ================================================================================================= //
	// This method first reads a text file with numbers and adds the numbers to the List<int[]> database //
	// ================================================================================================= //	
		public static void readtext(File file) throws FileNotFoundException
		{
			Scanner input = new Scanner(file);
			
			while (input.hasNextLine()) 
			{
				String number = input.nextLine(); //stores the line in the text file e.g. 1 2 3 4
				String[] parts = number.split(" "); //splits the string number based on the spaces
				
				int[] intArray = new int[parts.length]; //creates an integer array to store the String numbers
				
				for(int n = 0; n < parts.length; n++) 
				{
				   intArray[n] = Integer.parseInt(parts[n]); //converts each String into a integer
				   //System.out.println("int array: " + intArray[n]);
				}
			    database.add(intArray); //adds the array to the database
			    
			}	
			
			  //Prints out the items in the database:
			for(int i =0; i<database.size(); i++)
			{
				int[] newArray = database.get(i);
				for(int j=0; j<newArray.length; j++)
				{
					//System.out.print(newArray[j]);
				}
				//System.out.println(" ");
			}
		}
	
	// ================================================================================================= //
	// This method stores all the distinct items in transaction database in the distinctSet              //
	// ================================================================================================= //
		
		//Goes through the list database and stores all the unique items
		public static int[] getdistinctItem()
		{
			for(int i = 0; i<database.size(); i++)
			{
				int[] newArray = database.get(i);
				for(int j=0; j<newArray.length; j++)
				{
					if(!distinctSet.contains(newArray[j]))
					{
								distinctSet.add(newArray[j]);
					}
				}
			}
			//System.out.println("set " + distinctSet.toString());
					
			int[] distinct = new int[distinctSet.size()];
			int index = 0;
					
			Iterator<Integer> SetIterator = distinctSet.iterator(); //Iterator for the powerset
					
			while(SetIterator.hasNext()){
				Integer currentInt = SetIterator.next();
				distinct[index] = currentInt;
				index++;
			}
					
			for(int i =0; i <distinct.length; i++)
			{
				//System.out.println("distinct "+distinct[i]);
			}
					
			return distinct;
		}
		
	// ================================================================================================= //
	// This method generates the power set for an input int[] set 
	// ================================================================================================= //	
		public static List<ArrayList<Integer>> getPowerSetArrayList(int[] set)
		{
			int power_setSize = (int) Math.pow(2.0, set.length);//stores size of the power set of a set = 2^n
			//ArrayList<Integer> list = new ArrayList<Integer>();
			
			for(int counter = 0; counter < power_setSize; counter++)
			{
				ArrayList<Integer> list = new ArrayList<Integer>();
				//System.out.print("[ ");
				for(int j = 0; j < set.length; j++)
				{
					// (1<<j) is a number with jth bit 1 so when we 'and' them with the
	                // subset number it gets which numbers are present and which  are not 
	                if ((counter & (1 << j)) > 0)
	                {
	                	//System.out.print(set[j] +" ");
	                	Integer currentInt = set[j];
	                	list.add(currentInt);
	                 }   
				}
				if(list.size() > 0){
					arraylist.add(list);
				}
				//System.out.print("]");	
			}
//			for(int i =0; i<arraylist.size(); i++){
//				ArrayList<Integer> array = arraylist.get(i);
//				for(int j=0; j<array.size(); j++){
//						//System.out.print(array.get(j));
//						
//				}
//				//System.out.println("");
//			}
			
			return arraylist;	
		}
	
	// ================================================================================================= //
	// Checks to see if an series of numbers in a ArrayList<Integer> is a subset of an int[] array 
	// https://www.geeksforgeeks.org/find-whether-an-array-is-subset-of-another-array-set-1/
	// ================================================================================================= //	
	public static boolean isSubsetSet(int[] arr1, ArrayList<Integer> arr2){
	
		int i = 0; 
		int j = 0; 
		
		for(i =0; i < arr2.size(); i++)
		{
			for(j =0; j<arr1.length; j++)
			{
				
				if(arr2.get(i) == arr1[j])
				{    break;
				}
			}
				
			if(j == arr1.length)
			{ //If the above for loop was not broken, then arr2[i] is not present in arr1 so arr2 is not a subset
					return false; 
			}
			
		}
		return true;
	}
	
		
// ================================================================================================= //
// This method creates a frequency item list by storing the list in a HashMap
// ================================================================================================= //	
	public static void supportCount(List<int[]> database, int supportCount){
		
		for(int j=0; j<arraylist.size(); j++)
		{
			ArrayList<Integer> combArray = arraylist.get(j); //IMPORTANT
			
			int count = 0;
			
				for(int i =0; i<database.size(); i++)
				{			
					int[] newArray = database.get(i); ////IMPORTANT
					
					if (isSubsetSet(newArray, combArray) == true)
					{
						count++;
					}		
				}
			if (count >= supportCount)
			{
					map.put(combArray, count);
			}
		}
		
		for(Entry<ArrayList<Integer>, Integer> entry : map.entrySet())
		{
			ArrayList<Integer> list = entry.getKey();
			for(int i =0; i <list.size(); i++)
			{
				System.out.print(list.get(i) + " ");
			}
			System.out.println(" (" + entry.getValue() + ")");
			//System.out.println(entry.getKey().toString() + " (" + entry.getValue() + ")");
		}
	}
			
}
