public abstract class Clist<T> {

    //add (append)
    /**
     * 
     * @param newItem
     */
    public abstract void add(T newItem); 

    //set (set a given index)

    /**
     * Sets the item in the specified index in the list to the item given 
     * @param indexToSet The index of the item to set 
     * @param newItem The item to put the specified index 
     */
    public abstract void set(int indexToSet, T newItem);

    /**
     * Removes and returns the item at the specified index
     * @param index The index of the item to remove
     * @return The itm at the specified index; which has been removed from the lsit 
     */
    //remove (an index) Return the item we are going to rmove
    public abstract T remove(int index); 

    //get (an index)
    /**
     * Returns the item in the list at the specified index 
     * @param index The index in the item of the lsit to get 
     * @return The item at the specified index in the list 
     */
    public abstract T get(int index); 

    /**
     * Gets the number of the items in the lsit 
     */
    public abstract size();
}
