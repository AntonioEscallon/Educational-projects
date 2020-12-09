import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;


public class DateTest {
   // Two dates we are going to test with our Lilian date implementation!
   private Date date1;
   private Date date2;

   // We will run this method each time we run a test.
   @Before
   public void setUp() {
      date1 = new Date(4, 13, 1976);
      date2 = new Date(4, 13, 2020);
   }

   @Test
   public void numberOfDaysBetweenTest() {
      Assert.assertEquals("The number of days between " +
                          date1 + " and " + date2 + " must be 16071", 
                          Math.abs(date1.lilian() - date2.lilian()), 16071);
   }
}
