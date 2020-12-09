public class CArrayList<T> implements Clist<T> {

    //Instance variables
    //Array of items;
    //Private make sit unmodifiable by everyone else 
    /**
     * The iteem in this CArrayList
     */
    private Objects [] items;
    //firstEmptyIndex;
    /**
     * The index of the first empty slot in the CArrayList
     */
    private int firstEmptyslot; 
    
    public CArrayList (){

        items = new Object[10];
        firstEmptySlot = 0;

    }

    @Override
    //add (append)
    public T add(T newItem){
        if (size() == items.length){
            //Make a new array of double size
            //*2 has to do with the memory usage tradeoff. What gives us "wiggle room." Copying is expensive so we want to minimize the amount of processing.
            //Doubling just works well. 
            Object [] objs = new Object [items.length*2];
            //Copy elemtens of old array
            for (int i = 0; i<items.length; i++){
                objs[i] = items[i];
            }
            items = objs;
        }
        items[firstEmptyslot] = newItem; 
        firstEmptyslot++;
    }
    @Override
    //set (set a given index)
    public T set(int indexToSet, T newItem){
        items[indexToSet] = newItem; 
    }
    @Override
    @SuppressWarnings("Unchecked")
    //remove (an index) Or shift all of the values to the left
    public T remove(int index){
        //Save the item we want to return
        T toReturn = (T)items[index];
        //Shift all items to the lefts, overwritting the removed item
        for (int i = index; i<size() - 1; i++)
        {
            items[i] = items[i+1];
        }
        //Decrement the firstEmptySlot index
        firstEmptyslot--;
        //Return the index to be removed
        return toReturn; 
    }
    @Override
    @SuppressWarnings ("unchecked")
    //get (an index)
    public T get(int index) {
        return (T) items[index];
    }

    @Override 
    public int size(){
        return firstEmptyslot;
    }

}