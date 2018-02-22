/*
#ifndef FLOWERQ_LIST
    #include "List.hpp"
#endif
*/
#ifndef FLOWERQ_LIST
#define FLOWERQ_LIST


#include "Macro.hpp"
#include "IO.hpp"
#include "Match.hpp"
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


    template<typename A, typename B>
    static List<std::tuple<A, B>> zip(List<A> list1, List<B> list2);

    namespace list{
        template<typename A>
        static List<A> create();

        template<typename A>
        static List<A> create(A value);

        template<typename A, typename ...VARARGS>
        static List<A> create(A value, VARARGS... varargs);

        template<typename A>
        static List<A> cons(A value, List<A> list);
    }
    #pragma endregion



    template<typename T>
    class List{

    protected:
        Node<T>* head_ptr; // the head ptr does not contain values but the length of list.
    public:

        int length(){
            return head_ptr->size;
        }

        T at(int idx){
            Node<T> *list_ptr = this->head_ptr->Next;
            int i = 0;
            while(i++ < idx){
                if (list_ptr == nullptr){
                    const char* err_info = "Runtime IndexError: List ended before found the index.";
                    printf("%s\n", err_info);
                    const auto err = std::runtime_error(err_info);
                    throw err;
                }
                list_ptr = list_ptr->Next;
            }
            return list_ptr->value;
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

        #include "List.BaseMethods.hpp"

        StringBuff toString(){

            const int n = length();
            if (n == 0){
                return rstr("List<0>[]");
            }

            T head;
            List<T> tail;
            auto tp = destruct();
            pattern::match(tp, head, tail);
            
            StringBuff res = rstr("List<") + to_string(n) + rstr(">[") + IO::inspect(head);
            
            tail.forEach([=, &res](T e) {
                res += rstr(", ") + IO::inspect(e);
            });
            return res + rstr("]"); 
        }


        template<typename A>
        friend List<A> list::create();

        template<typename A>
        friend List<A> list::create(A value);

        template<typename A, typename ...VARARGS>
        friend List<A> list::create(A value, VARARGS... varargs);

        template<typename A>
        friend List<A> list::cons(A value, List<A> list);

        template<typename A>
        friend void del(List<A>* list_ptr);

        template<typename A>
        friend void del(List<A> &list);

        template<typename A, typename B>
        friend List<std::tuple<A, B>> zip(List<A> list1, List<B> list2);
    };


    template<typename A, typename B>
    List<std::tuple<A, B>> zip(List<A> list1, List<B> list2){
        const int len = std::min(list1.length(), list2.length());
        List<std::tuple<A, B>> new_list;
        auto h = new_list.head_ptr = Node<std::tuple<A, B>>::_new_head(len);

        Node<A> *h1 = list1.head_ptr->Next;
        Node<B> *h2 = list2.head_ptr->Next;
        for(int i=0; i < len; ++i){
            h -> Next = new Node<std::tuple<A, B>>(std::make_tuple(h1->value, h2->value));
            h = h->Next;
        }
        h -> Next = nullptr;
        return new_list;
    }
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
