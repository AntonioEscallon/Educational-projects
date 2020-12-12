public class CArrayList<T> implements CList<T>{
    /**
     * The items in this CArrayList
     */
    private Object[] items;
    /**
     * The index of the first empty slot in the CArrayList
     */
    private int firstEmptySlot;

    public CArrayList(){
        items = new Object[10];
        firstEmptySlot = 0;
    }

    @Override
    public void add(T newItem) {
        if(size() == items.length){
            // Make a new array of double size
            Object[] objs = new Object[items.length*2];
            // Copy elements of old array
            for(int i = 0; i < items.length; i++){
                objs[i] = items[i];
            }
            // Update the internal array
            items = objs;
        }
        items[firstEmptySlot] = newItem;
        firstEmptySlot++;
    }

    @Override
    public void set(int indexToSet, T newItem) {
        items[indexToSet] = newItem;
    }

    @Override
    public void insert(int indexToInsert, T newItem) {
        /* Copy the last item to the right (if one exists). This also handles extending the array,
         * if need be. Examples assume indexToInsert is zero. */
        if(size() > 0){
            add(get(size()-1)); // [1, 2, 3]  --> [1, 2, 3, 3, null, null]
        } else {
            firstEmptySlot++;
        }
        // Shift everything else right: [1, 2, 3, 3, null, null] --> [1, 1, 2, 3, null, null]
        for(int i = size() - 2; i > indexToInsert; i--){
            items[i] = items[i-1];
        }
        // Add the item at the specified index: [1, 1, 2, 3, null, null] --> [4, 1, 2, 3, null, null]
        items[indexToInsert] = newItem;
    }

    @Override
    @SuppressWarnings("unchecked")
    public T remove(int index) {
        // Save the item we want to return
        T toReturn = (T) items[index];
        // Shift all items left, overwriting the removed item
        for(int i = index; i < size() - 1; i++){
            items[i] = items[i+1];
        }
        // Decrememnt the firstEmptySlot index
        firstEmptySlot--;
        // Return the item removed
        return toReturn;
    }

    @Override
    @SuppressWarnings("unchecked")
    public T get(int index) {
        if(index > size()-1){
            throw new IndexOutOfBoundsException("Index " + index + " is out of bounds for length " + size());
        }
        return (T) items[index];
    }

    @Override
    public int size() {
        return firstEmptySlot;
    }
}