
# deprecated cimport for backwards compatibility:
from libc.string cimport const_char


cdef extern from "<string>" namespace "std" nogil:

    # hack for templated members returning a reference type
    ctypedef string& string_ref

    size_t npos = -1

    cdef cppclass string:

        cppclass iterator:
            char& operator*()
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
            char& operator*()
            reverse_iterator operator++()
            reverse_iterator operator--()
            reverse_iterator operator+(size_t)
            reverse_iterator operator-(size_t)
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator>=(reverse_iterator)

        string() except +                                                           # (1)
        string(size_t, char) except +                                               # (2)
        string(const string&, size_t, size_t) except +                              # (3)
        string(const char*, size_t) except +                                        # (4)
        string(const char*) except +                                                # (5)
        # return type is a hack to allow the code to compile
        string_ref string[input_iterator](input_iterator, input_iterator) except +  # (6)
        string(const string&) except +                                              # (7)

        #string& operator= (string&)
        #string& operator= (char*)
        #string& operator= (char)

        string& assign(size_t, char) except +                                       # (1)
        string& assign(const string&) except +                                      # (2)
        string& assign(const string&, size_t, size_t) except +                      # (3)
        string& assign(const char*, size_t) except +                                # (5)
        string& assign(const char*) except +                                        # (6)
        string_ref assign[input_iterator](input_iterator, input_iterator) except +  # (7)

        # Element access
        char& at(size_t) except +
        char& operator[](size_t)
        char& front()  # C++11
        char& back()   # C++11
        const char* data()
        const char* c_str()

        # Iterators
        iterator begin()
        iterator end()
        reverse_iterator rbegin()
        reverse_iterator rend()

        # Capacity
        bint empty()
        size_t size()
        size_t length()
        size_t max_size()
        void reserve(size_t) except +
        size_t capacity()
        void shrink_to_fit()  # C++11

        # Operations
        void clear()

        string& insert(size_t, size_t, char) except +                   # (1)
        string& insert(size_t, const char*) except +                    # (2)
        string& insert(size_t, const char*, size_t) except +            # (3)
        string& insert(size_t, const string&) except +                  # (4)
        string& insert(size_t, const string&, size_t, size_t) except +  # (5)
        iterator insert(iterator, char) except +                        # (6)
        iterator insert(iterator, size_t, char) except +                # (7)
        # crashes the compiler
        #iterator insert[input_iterator](iterator, input_iterator, input_iterator) except +

        string& erase()                              # (1)
        string& erase(size_t) except +               # (1)
        string& erase(size_t, size_t) except +       # (1)
        iterator erase(iterator) except +            # (2)
        iterator erase(iterator, iterator) except +  # (3)

        void push_back(char c) except +
        void pop_back()  # C++11

        string& append(size_t, char) except +                                       # (1)
        string& append(string&) except +                                            # (2)
        string& append(string&, size_t, size_t) except +                            # (3)
        string& append(char*, size_t) except +                                      # (4)
        string& append(char*) except +                                              # (5)
        string_ref append[input_iterator](input_iterator, input_iterator) except +  # (6)

        int compare(const string&)                                           # (1)
        int compare(size_t, size_t, const string&) except +                  # (2)
        int compare(size_t, size_t, const string&, size_t, size_t) except +  # (3)
        int compare(const char*) except +                                    # (4)
        int compare(size_t, size_t, const char*) except +                    # (5)
        int compare(size_t, size_t, const char*, size_t) except +            # (6)

        string& replace(size_t, size_t, const string&) except +                  # (1)
        string& replace(size_t, size_t, const string&, size_t, size_t) except +  # (2)
        string& replace(size_t, size_t, const char*, size_t) except +            # (4)
        string& replace(size_t, size_t, const char*) except +                    # (5)
        string& replace(size_t, size_t, size_t, char) except +                   # (6)

        string substr()
        string substr(size_t) except +
        string substr(size_t, size_t) except +

        size_t copy(char*, size_t)
        size_t copy(char*, size_t, size_t) except +

        void resize(size_t) except +        # (1)
        void resize(size_t, char) except +  # (2)

        void swap(string&) except +

        # Search
        size_t find(const string&)                # (1)
        size_t find(const string&, size_t)        # (1)
        size_t find(const char*, size_t, size_t)  # (2)
        size_t find(const char*)                  # (3)
        size_t find(const char*, size_t)          # (3)
        size_t find(char)                         # (4)
        size_t find(char, size_t)                 # (4)

        size_t rfind(const string&)
        size_t rfind(const string&, size_t)
        size_t rfind(const char*, size_t, size_t)
        size_t rfind(const char*)
        size_t rfind(const char*, size_t)
        size_t rfind(char)
        size_t rfind(char, size_t)

        size_t find_first_of(const string&)
        size_t find_first_of(const string&, size_t)
        size_t find_first_of(const char*, size_t, size_t)
        size_t find_first_of(const char*)
        size_t find_first_of(const char*, size_t)
        size_t find_first_of(char)
        size_t find_first_of(char, size_t)

        size_t find_first_not_of(const string&)
        size_t find_first_not_of(const string&, size_t)
        size_t find_first_not_of(const char*, size_t, size_t)
        size_t find_first_not_of(const char*)
        size_t find_first_not_of(const char*, size_t)
        size_t find_first_not_of(char)
        size_t find_first_not_of(char, size_t)

        size_t find_last_of(const string&)
        size_t find_last_of(const string&, size_t)
        size_t find_last_of(const char*, size_t, size_t)
        size_t find_last_of(const char*)
        size_t find_last_of(const char*, size_t)
        size_t find_last_of(char)
        size_t find_last_of(char, size_t)

        size_t find_last_not_of(const string&)
        size_t find_last_not_of(const string&, size_t)
        size_t find_last_not_of(const char*, size_t, size_t)
        size_t find_last_not_of(const char*)
        size_t find_last_not_of(const char*, size_t)
        size_t find_last_not_of(char)
        size_t find_last_not_of(char, size_t)

        string operator+ (const string&)
        string operator+ (const char*)

        bint operator==(const string&)
        bint operator==(const char*)

        bint operator!= (const string&)
        bint operator!= (const char*)

        bint operator< (const string&)
        bint operator< (const char*)

        bint operator> (const string&)
        bint operator> (const char*)

        bint operator<= (const string&)
        bint operator<= (const char*)

        bint operator>= (const string&)
        bint operator>= (const char*)
