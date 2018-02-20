//
// Created by misakawa on 18-2-20.
//

#ifndef CFLOWERQ_LIST_H
#ifndef CFLOWERQ_TUPLE_H

#include "Tuple.hpp"

#endif

#define CFLOWERQ_LIST_H


#include <functional>
#include <iostream>


namespace cfarfar {

    template<typename T>
    class List {
    public:
        explicit List(T v) {
            value = v;
        };

        void _set_length(int len) {
            _length = len;
        }

        template<typename... Args>
        static List<T> *_new_ptr(int &count, T value, Args... varargs) {
            auto list_ptr = new List<T>(value);
            list_ptr->Next = _new_ptr(++count, varargs...);
            return list_ptr;
        }

        static List<T> *_new_ptr(int &count, T value) {
            ++count;
            auto list_ptr = new List<T>(value);
            list_ptr->Next = nullptr;
            return list_ptr;
        }


        List() {
            _length = 0;
        };


        union {
            T value;
            int _length{};
        };

        int len() {
            return _length;
        }

        List<T> *Next;

        T head() {
            // raise error if the len of list is less than 1;
            return this->Next->value;
        }

        List<T> tail() {
            auto new_list = List<T>();
            auto src_list_length = this->len();
            if (src_list_length == 0) {
                new_list.Next = nullptr;
                new_list._set_length(0);
                return new_list;
            }
            new_list.Next = this->Next->Next;
            new_list._set_length(this->len() - 1);
            return new_list;
        }

        Tuple<T, List<T>> destruct() {
            return tuple::create(head(), tail());
        };

        void forEach(std::function<void(T)> action) {
            List<T> *list_ptr = this;
            list_ptr = list_ptr->Next;
            while (list_ptr != nullptr) {
                action(list_ptr->value);
                list_ptr = list_ptr->Next;
            }
        }


        List<T> filter(std::function<bool(T)> predicate) {
            List<T> new_list = List<T>();

            List<T> *new_list_ptr = &new_list;
            List<T> *src_list_ptr = this;

            int length = 0;
            src_list_ptr->forEach([&](T e) {
                if (predicate(e)) {
                    ++length;
                    new_list_ptr->Next = new List<T>(e);
                    new_list_ptr = new_list_ptr->Next;
                }
            });

            new_list_ptr->Next = nullptr;
            new_list._set_length(length);
            return new_list;
        }

        template<typename G>
        List<G> map(std::function<G(T)> fn) {
            auto new_list = List<T>();

            List<T> *new_list_ptr = &new_list;
            List<T> *src_list_ptr = this;

            src_list_ptr->forEach([&](T e) {
                new_list_ptr->Next = new List<T>(fn(e));
                new_list_ptr = new_list_ptr->Next;
            });

            new_list_ptr->Next = nullptr;
            new_list._set_length(this->len());
            return new_list;
        }

        template<typename G>
        G reduce(std::function<G(G, T)> fold_fn, G start_elem) {
            this->forEach([=, &start_elem](int e) {
                start_elem = fold_fn(start_elem, e);
            });
            return start_elem;
        }

        template<typename G>
        List<Tuple<T, G>> zip(List<G> traversal) {
            List<Tuple<T, G>> new_list = List<Tuple<T, G>>();

            List<T> *other_list_ptr = &traversal, *src_list_ptr = this;
            List<Tuple<T, G>> *new_list_ptr = &new_list;

            while ((src_list_ptr = src_list_ptr->Next) != nullptr &&
                   (other_list_ptr = other_list_ptr->Next) != nullptr) {
                new_list_ptr->Next = new List<Tuple<T, G>>(
                        tuple::create(src_list_ptr->value, other_list_ptr->value));
                new_list_ptr = new_list_ptr->Next;
            }

            new_list_ptr->Next = nullptr;
            new_list._set_length(std::max(this->len(), traversal.len()));
            return new_list;
        };


        static List<T> create() {
            List<T> new_list = List<T>();
            new_list.Next = nullptr;
            new_list._set_length(0);
            return new_list;
        }


        static List<T> create(T value) {
            auto new_list = List<T>(value);
            new_list.Next = nullptr;
            return new_list;
        }

        template<typename... Args>
        static List<T> create(T value, Args... varargs) {
            auto new_list = List<T>::create();
            int count = 0;
            new_list.Next = _new_ptr(count, value, varargs...);
            new_list._set_length(count);
            return new_list;
        }
    };

//        void forEach(void action(int)) {
//            List<T> *list_ptr = this;
//            list_ptr = list_ptr->Next;
//            while (list_ptr != nullptr) {
//                action(list_ptr->value);
//                list_ptr = list_ptr->Next;
//            }
//        }

//        List<T> filter(bool predicate(T)) {
//            List<T> new_list = List<T>();
//
//            List<T> *new_list_ptr = &new_list;
//            List<T> *src_list_ptr = this;
//
//            int len = 0;
//            src_list_ptr->forEach([&](T e) {
//                if (predicate(e)) {
//                    ++len;
//                    new_list_ptr->Next = new List<T>(e);
//                    new_list_ptr = new_list_ptr->Next;
//                }
//            });
//
//            new_list_ptr->Next = nullptr;
//            new_list._set_length(len);
//            return new_list;
//        }


//        template<typename G>
//        List<G> map(G fn(T)) {
//            auto new_list = List<T>();
//
//            List<T> *new_list_ptr = &new_list;
//            List<T> *src_list_ptr = this;
//
//            src_list_ptr->forEach([&](T e) {
//                new_list_ptr->Next = new List<T>(fn(e));
//                new_list_ptr = new_list_ptr->Next;
//            });
//
//            new_list_ptr->Next = nullptr;
//            new_list._set_length(this->len());
//            return new_list;
//        }



    template<typename T>
    static void del(List<T> &list) {
        del(list.Next);
        list.Next = nullptr;
    }

    template<typename T>
    static void del(List<T> *list_ptr) {
        if (list_ptr == nullptr)
            return;
        List<T> *next_ptr = list_ptr->Next;
        delete list_ptr;
        del(next_ptr);
    }

    namespace list {

        template<typename T>
        List<T> create() {
            return List<T>::create();
        }

        template<typename T>
        static List<T> create(T value) {
            return List<T>::create(value);
        }

        template<typename T, typename... Args>
        static List<T> create(T value, Args... varargs) {
            return List<T>::create(value, varargs...);
        }
    }

//    template <typename T>
//    static List<T> cons(T v, List<T> list){
//        List<T> new_list = cfarfar::List<T>::Empty<T>();
//
//
//    }
}

#endif
