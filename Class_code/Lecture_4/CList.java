public interface CList<T>{
    
    /**
     * Appends the item to the list
     * @param newItem The item to append to the list
     */
    public void add(T newItem);

    /**
     * Sets the item at the specified index in the list to the item given
     * @param indexToSet The index of the item to set
     * @param newItem The item to put at the specified index
     */
    public void set(int indexToSet, T newItem);

    /**
     * Inserts an item before the index specified (the new item becomes 
     * the item at the specified index)
     * @param indexToInsert The index to insert the new item at
     * @param newItem The item to insert at the given index
     */
    public void insert(int indexToInsert, T newItem);

    /**
     * Removes and returns the item at the specified index
     * @param index The index of the item to remove
     * @return The item at the specified index, which has been removed from the list
     */
    public T remove(int index);

    /**
     * Returns the item in the list at the specified index
     * @param index The index in the item of the list to get
     * @return The item at the specified index in the list
     */
    public T get(int index);

    /**
     * Gets the number of items in the list
     * @return The number of items in the list
     */
    public int size();
}