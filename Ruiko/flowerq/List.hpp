/*
#ifndef FLOWERQ_LIST
    #include "List.hpp"
#endif
*/
#ifndef FLOWERQ_LIST
#define FLOWERQ_LIST

#ifndef FLOWERQ_IO
    #include "IO.hpp"
#endif

#ifndef FLOWERQ_MATCH
    #include "Match.hpp"
#endif

#include <functional>


namespace flowerq{

    // struct Node definition
    #include "List.Node.hpp"


    #pragma region declare
    template<typename T>
    class List;

    template<typename A>
    static void del(List<A>* list_ptr);

    template<typename A>
    static void del(List<A> &list);

    namespace list{
        template<typename A>
        static List<A> create();

        template<typename A>
        static List<A> create(A value);

        template<typename A, typename ...VARARGS>
        static List<A> create(A value, VARARGS... varargs);

        template<typename A>
        static List<A> cons(List<A> list, A value);

    }
    #pragma endregion



    template<typename T>
    class List{

    private:
        Node<T>* head_ptr; // the head ptr does not contain values but the length of list.

    public:

        int length(){
            return head_ptr->size;
        }

        T head(){
            return head_ptr->Next->value;
        }

        List<T> tail() {
            List<T> new_list;
            const int n = length();
            if (n == 0){
                new_list.head_ptr = Node<T>::_new_head(0);
                return new_list;
            }
            new_list.head_ptr = Node<T>::_new_head(n - 1, this->head_ptr->Next->Next);
            return new_list; 
        }

        std::tuple<T, List<T>> destruct() {
            return std::make_tuple(head(), tail());
        };

        void forEach(std::function<void(T)> action) {
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

            List<std::tuple<T, G>> new_list;

            auto new_head_ptr = new_list -> head_ptr = Node<std::tuple<T, G>>::_new_head(std::min(length(), traversal.length()));

            Node<T> *src_list_ptr = this->head_ptr, *other_list_ptr = traversal->head_ptr;

            while((src_list_ptr = src_list_ptr->Next) != nullptr &&
                   (other_list_ptr = other_list_ptr->Next) != nullptr) {
                new_head_ptr->Next = new Node<std::tuple<T, G>>(
                        std::make_tuple(src_list_ptr->value, other_list_ptr->value));
                new_head_ptr = new_head_ptr->Next;
            }
            new_head_ptr->Next = nullptr;
            return new_list;
        };

        std::string to_string(){

            const int n = length();
            if (n == 0){
                return "List<0>[]";
            }

            T head;
            List<T> tail;
            auto tp = destruct();
            pattern::match(tp, head, tail);
            
            std::string res = "List<" + std::to_string(n) + ">[" + IO::inspect(head);
            
            tail.forEach([=, &res](T e) {
                res += ", " + IO::inspect(e);
            });

            return res + "]";
        }


        template<typename A>
        friend List<A> list::create();

        template<typename A>
        friend List<A> list::create(A value);

        template<typename A, typename ...VARARGS>
        friend List<A> list::create(A value, VARARGS... varargs);

        template<typename A>
        friend List<A> list::cons(List<A> list, A value);

        template<typename A>
        friend void del(List<A>* list_ptr);

        template<typename A>
        friend void del(List<A> &list);

    };


    // define ways to construct list.
    #include "List.Constructor.hpp"

    template<typename A>
    void del(List<A>* list_ptr){
        del(list_ptr->head_ptr);
        delete list_ptr;
    }

    template<typename A>
    void del(List<A> &list){
        del(list.head_ptr);
    }

}
#endif
