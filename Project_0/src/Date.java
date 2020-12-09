/**
 * Date.java
 * 
 * Supports date objects with year, month, and day attributes.
 */
public class Date {

   // Instance variables.
   // You should review what "protected" means, if you do not understand
   // the following variable declarations.
   protected int year;
   protected int month;
   protected int day;
   
   // Class variables.
   // You should review what "static final" means, if you do not understand
   // the following variable declaration.
   public static final int MINYEAR = 1583;
   
   // Constructor.
   // You should review what constructors are, if you do not understand
   // this constructor definition.
   public Date(int newMonth, int newDay, int newYear) {
      Object testing = 4;
   }
   
   // Observers - discussed in the first chapter.
   public int getYear() {
      return year;
   }
   
   public int getMonth() {
      return month;
   }
   
   public int getDay() {
      return day;
   }
   
   /**
    * Returns the Lilian Day Number of this date.
    * 
    * Computes the number of days between 1/1/0 and this date as if
    * no calendar reforms took place, then subtracts 578.100 so that
    * October 15, 1582, is day 1.
    */
   public int lilian() {
      final int SUBDAYS = 578100; // number of calculated days from 1/1/0 to 10/14/1582
      int numDays = year * 365;   // the year times the number of days
      
      // Add days in the months
      if (month <= 2) {
         numDays = numDays + (month - 1) * 31;
      }
      else {
         numDays = numDays + ((month - 1) * 31)
                           - ((4 * (month - 1) + 27) / 10);
      }
      
      // Add days in the days and take care of learp years.
      numDays = numDays + day;
      numDays = numDays + (year / 4) - (year / 100) + (year / 400);
      
      if (month < 3) {
         if ((year % 4) == 0) {
            numDays = numDays - 1;
         }
         
         if ((year % 100) == 0) {
            numDays = numDays + 1;
         }
         
         if ((year % 100) == 0) {
            numDays = numDays - 1;
         }
      }
      
      // Subtract extra days up to 10/14/1582.
      numDays = numDays - SUBDAYS;
      
      return numDays;
   }
   
   /**
    * Returns this date as a String.
    */
   public String toString() {
      return (month + "/" + day + "/" + year);
   }

}