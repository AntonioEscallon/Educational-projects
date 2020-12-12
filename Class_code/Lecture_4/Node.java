public class Node<T> {
    /**
     * The data this node will store
     */
    private T data;
    /**
     * The reference to the next node
     */
    private Node<T> next;

    /**
     * Creates the node unlinked to anything with the specified data
     * @param data The data this node will store
     */
    public Node(T data){
        this.data = data;
        next = null;
    }

    /**
     * Creates the node linked to the node passed in with the specified data
     * @param data The data this node will store
     * @param next The node this node should link to
     */
    public Node(T data, Node<T> next){
        this.data = data;
        this.next = next;
    }

    public void setData(T newData){
        data = newData;
    }

    public T getData(){
        return data;
    }

    public void setNext(Node<T> next){
        this.next = next;
    }

    public Node<T> getNext(){
        return next;
    }
}
