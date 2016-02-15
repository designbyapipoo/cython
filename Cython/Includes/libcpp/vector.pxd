cdef extern from "<vector>" namespace "std" nogil:
    cdef cppclass vector[T]:

        cppclass iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(iterator)
            bint operator!=(iterator)
            bint operator<(iterator)
            bint operator>(iterator)
            bint operator<=(iterator)
            bint operator>=(iterator)

        cppclass reverse_iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator>=(reverse_iterator)

        cppclass const_iterator(iterator):
            pass

        cppclass const_reverse_iterator(reverse_iterator):
            pass

        vector() except +                                                     # (1)
        vector(size_t, const T&) except +                                     # (2)
        vector(size_t) except +                                               # (3)
        void vector[input_iterator](input_iterator, input_iterator) except +  # (4)
        vector(const vector&) except +                                        # (5)

        #vector& operator=(vector&)

        void assign(size_t, const T&)                                         # (1)
        void assign[input_iterator](input_iterator, input_iterator) except +  # (2)

        # Element access
        T& at(size_t) except +
        T& operator[](size_t)
        T& front()
        T& back()
        T* data()  # C++11

        # Iterators
        iterator begin()
        const_iterator const_begin "begin"()
        iterator end()
        const_iterator const_end "end"()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()

        # Capacity
        bint empty()
        size_t size()
        size_t max_size()
        void reserve(size_t) except +
        size_t capacity()
        void shrink_to_fit()  # C++11

        # Modifiers
        void clear()

        iterator insert(iterator, const T&) except +                                    # (1)
        void insert(iterator, size_t, const T&) except +                                # (3)
        void insert[input_iterator](iterator, input_iterator, input_iterator) except +  # (4)

        iterator emplace(iterator, ...) except +  # C++11

        iterator erase(iterator) except +            # (1)
        iterator erase(iterator, iterator) except +  # (2)

        void push_back(const T&) except +
        void emplace_back(...) except +  # C++11
        void pop_back()
        void resize(size_t) except +
        void resize(size_t, const T&) except +
        void swap(vector&)

        bint operator==(const vector&, const vector&)
        bint operator!=(const vector&, const vector&)
        bint operator<(const vector&, const vector&)
        bint operator<=(const vector&, const vector&)
        bint operator>(const vector&, const vector&)
        bint operator>=(const vector&, const vector&)
