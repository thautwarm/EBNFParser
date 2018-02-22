void forEach(std::function<void(T&)> action) {
    Node<T> *list_ptr = this->head_ptr->Next;
    while (list_ptr != nullptr) {
        action(list_ptr->value);
        list_ptr = list_ptr->Next;
    }
}

template<typename G>
List<G> map(std::function<G(T)> fn){
    
    const int n = length();
    List<G> new_list;
    Node<G>* src_list_ptr = new_list.head_ptr = Node<G>::_new_head(n);
    if (n == 0){
        src_list_ptr -> Next = nullptr;
        return new_list;
    }
    this->forEach([&](T e){
        src_list_ptr->Next = new Node<G>(fn(e));
        src_list_ptr = src_list_ptr -> Next;
    });
    src_list_ptr -> Next = nullptr;
    return new_list;
}

List<T> filter(std::function<bool(T)> predicate){
    const int n = length();
    List<T> new_list;
    Node<T>* src_list_ptr = new_list.head_ptr = Node<T>::_new_head();
    if (n == 0){
        src_list_ptr -> Next = nullptr;
        return new_list;
    }
    int length = 0;
    this->forEach([&](T e){
        if (predicate(e)){
            ++ length;
            src_list_ptr->Next = new Node<T>(e);
            src_list_ptr = src_list_ptr -> Next;
        }
    });
    src_list_ptr -> Next = nullptr;
    new_list.head_ptr->size = length;
    return new_list;
}

template<typename G>
G reduce(std::function<G(G, T)> fold_fn, G start_elem) {
    this->forEach([&](int e) {
        start_elem = fold_fn(start_elem, e);
    });
    return start_elem;
}

template<typename G>
List<std::tuple<T, G>> zip(List<G> traversal) {
    return flowerq::zip(*this, traversal);
}