public class Tester{

    public static void main(String[]args){
        CArrayList<String> myList = new CArrayList<String>();

        myList.add("Hello");
        myList.add("Sup");
        myList.add("This is a set string, please do not panic.")

        System.out.println(myList.get(2));

        System.out.println(myList.remove(1));

        System.out.println(myList.get(1));

        System.out..println(myList.size());
    }
}