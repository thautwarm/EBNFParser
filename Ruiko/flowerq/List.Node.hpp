/*

*/

template<typename T>
struct Node{

public:
    union{
        T value;
        int size;
    };
    Node<T>* Next = nullptr;


    Node(){}
    Node(T v) {
        value = v;
    };

    template<typename... Args>
    static Node<T> *_new_ptr(int &count, T value, Args... varargs) {
        auto list_ptr = new Node<T>(value);
        list_ptr->Next = _new_ptr(++count, varargs...);
        return list_ptr;
    }

    static Node<T> *_new_ptr(int &count, T value) {
        ++count;
        auto list_ptr = new Node<T>(value);
        list_ptr->Next = nullptr;
        return list_ptr;
    }

    static Node<T> *_new_ptr(T value) {
            auto list_ptr = new Node<T>(value);
            list_ptr->Next = nullptr;
            return list_ptr;
    }

    static Node<T> *_new_head(int size, Node<T>* next) {
            auto head_ptr = new Node<T>;
            head_ptr -> size = size;
            head_ptr -> Next = next;
            return head_ptr;
    }

    static Node<T> *_new_head(int size) {
            auto head_ptr = new Node<T>;
            head_ptr -> size = size;
            return head_ptr;
    }

    static Node<T> *_new_head() {
            auto head_ptr = new Node<T>;
            return head_ptr;
    }

};

    template<typename T>
    static void del(Node<T> &list) {
        del(list.Next);
        list.Next = nullptr;
    }

    template<typename T>
    static void del(Node<T> *list_ptr) {
        if (list_ptr == nullptr)
            return;
        Node<T> *next_ptr = list_ptr->Next;
        delete list_ptr;
        del(next_ptr);
    }
    