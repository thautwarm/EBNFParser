template<typename A>
static List<A> list::create() {
    List<A> new_list = List<A>();
    new_list.head_ptr = Node<A>::_new_head(0);
    new_list.head_ptr->Next = nullptr;
    return new_list;
}

template<typename A>
static List<A> list::create(A value) {
    List<A> new_list = List<A>();
    new_list.head_ptr = Node<A>::_new_head(1);
    new_list.head_ptr->Next = Node<A>::_new_ptr(value);
    return new_list;
}

template<typename A, typename ...VARARGS>
static List<A> list::create(A value, VARARGS... varargs){
    List<A> new_list = List<A>();
    int count = 0;
    auto src_ptr = Node<A>::_new_ptr(count, value, varargs...);
    new_list.head_ptr = Node<A>::_new_head(count, src_ptr);
    return new_list;
}

template<typename A>
static List<A> list::cons(A value, List<A> list){
    List<A> new_list;
    auto node = Node<A>::_new_ptr(value);
    node -> Next = list.head_ptr->Next;
    new_list.head_ptr = Node<A>::_new_head(list.length() + 1, node);    
    return new_list;
}