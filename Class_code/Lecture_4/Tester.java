public class Tester{
    public static void main(String[] args){
        CList<String> myList = new CLinkedList<String>();

        myList.add("Hello");
        myList.add("Sup");

        System.out.println(myList.get(1));

        System.out.println(myList.remove(1));

        System.out.println(myList.get(0));

        System.out.println(myList.size());

        // Remove all items
        while(myList.size() > 0){
            myList.remove(0);
        }
        
        for(int i = 0; i < 30; i++){
            myList.insert(0, "Hello " + i);
        }

        System.out.println(myList.size());
        System.out.println(myList.get(15));
    }
}