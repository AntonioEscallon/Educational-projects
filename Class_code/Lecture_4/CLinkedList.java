public class CLinkedList<T> implements CList<T> {

    private Node<T> head;
    private Node<T> tail;
    private int size;

    public CLinkedList(){
        head = null;
        tail = null;
        size = 0;
    }

    @Override
    public void add(T newItem) {
        Node<T> nodeToAdd = new Node<T>(newItem);
        // If the list is empty
        if(size() == 0){
            head = nodeToAdd;
            tail = nodeToAdd;
        } else {
            // Set the new last item
            tail.setNext(nodeToAdd);
            // Update the tail to the new last item
            tail = tail.getNext();
        }
        // increment size
        size++;
    }

    @Override
    public void set(int indexToSet, T newItem) {
        getNode(indexToSet).setData(newItem);
    }

    @Override
    public void insert(int indexToInsert, T newItem) {
        // If we're trying to insert at the end, just add. 
        if(indexToInsert == size()){
            add(newItem);
            return;
        }
        // The node containing the data we want to add
        Node<T> nodeToAdd = new Node<T>(newItem);
        // If we insert a new head
        if(indexToInsert == 0){ 
            nodeToAdd.setNext(head);
            head = nodeToAdd;
        } else { // Inserting anywhere else
            // The node before the index we want to insert at
            Node<T> temp = getNode(indexToInsert-1);
            nodeToAdd.setNext(temp.getNext());
            temp.setNext(nodeToAdd);
        }
        size++;
    }

    @Override
    public T remove(int index) {
        if(index > size()-1){
            throw new IndexOutOfBoundsException("Index " + index + " is out of bounds for length " + size);
        }
        // If we're removing the first item in the list
        T value;
        if(size() == 1){ // Removing head and tail
            value = head.getData();
            head = null;
            tail = null;
        } else if(index == 0){ // Removing head
            value = head.getData();
            head = head.getNext();
        } else if(index == size() -1) { // Removing tail
            Node<T> temp = getNode(index-1);
            value = temp.getNext().getData();
            tail = temp;
            temp.setNext(null);
        } else {
            Node<T> temp = getNode(index-1);
            value = temp.getNext().getData();
            temp.setNext(null);
        }
        size--;
        return value;
    }

    @Override
    public T get(int index) {
        Node<T> temp = getNode(index);
        // Return the value of the node
        return temp.getData();
    }

    @Override
    public int size() {
        return size;
    }

    /**
     * Returns the index'th node from the linked list. Throws an
     * IndexOutOfBoundsException if the index is out of range
     * @param index The index of the item to get
     * @return The node with the given index
     */
    private Node<T> getNode(int index){
        if(index > size()-1 || index < 0){
            throw new IndexOutOfBoundsException("Index " + index + " is out of bounds for length " + size);
        }
        // Create a copy of the head reference as to not screw up head
        Node<T> temp = head;
        // Loop through and find the 'index'th item
        for(int i = 0; i < index; i++){
            temp = temp.getNext();
        }
        return temp;
    }
}
