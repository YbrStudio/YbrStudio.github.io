# C++黑魔法之基于返回值的函数重载

!!! tip "阅读建议"
    阅读难度：中

!!! note "本文所有代码运行结果均在Windows 11 & g++ 11.2.0环境下通过实际编译运行进行了验证"

## 函数重载
我们都知道，C++中的函数重载是很重要的特性之一，编译器会根据函数的参数列表来判断调用的函数。如：
```cpp
#include <iostream>

void f() {
    std::cout << "f()" << std::endl;
}

void f(int) {
    std::cout << "f(int)" << std::endl;
}

int main() {
    f();
    f(1);

    return 0;
}
```
输出：
```output
f()
f(int)
```

但是，函数重载只能根据参数列表来区分所调用的函数，而不能根据返回值来区分所调用的函数，即使接受返回值的变量提供了相关的类型信息。如：
```cpp
#include <iostream>

void f() {
    std::cout << "void f()" << std::endl;
}

int f() {
    std::cout << "int f()" << std::endl;
    return 0;
}

int main() {
    f();
    int ret = f();

    return 0;
}
```
编译以上代码会报错：
```output
source.cpp:7:5: error: ambiguating new declaration of 'int f()'
    7 | int f() {
      |     ^
source.cpp:3:6: note: old declaration 'void f()'
    3 | void f() {
      |      ^
source.cpp: In function 'int main()':
source.cpp:14:16: error: void value not ignored as it ought to be
   14 |     int ret = f();
      |               ~^~
```

## 基于返回值的函数重载
尽管C++不支持基于返回值的函数重载，但是我们可以通过一些黑魔法来**模拟**实现这个功能（众所周知C++的黑魔法是格外的多）。说是黑魔法，其实只是利用了重载类型转换方法的技巧。先来看代码：
```cpp
#include <iostream>
#include <string>

class Bool {
public:
    Bool(bool value) : __value(value) {}

    class _RetT {
    public:
        _RetT(const Bool& obj) : __bool_obj(obj) {}

        operator bool() const {
            printf("bool-return overload\n");
            return this->__bool_obj.__value;
        }

        operator std::string() const {
            printf("string-return overload\n");
            return this->__bool_obj.__value ? "true" : "false";
        }

    private:
        const Bool& __bool_obj;
    };

    [[nodiscard]]
    _RetT get_value() const {
        return *this;
    }

private:
    bool __value;
};

int main() {
    auto bool_obj = Bool(true);
    bool b_ret = bool_obj.get_value();
    std::string str_ret = bool_obj.get_value();
    auto auto_ret = bool_obj.get_value();
}
```
输出：
```output
bool-return overload
string-return overload
```
上面的代码应该不是很难读。`Bool::get_value()`返回值的类型是一个内部定义的类型`_RetT`，而这个类型的对象持有`Bool`对象的引用，并且可以隐式转换为`bool`类型和`std::string`的对象。那么在`Bool::get_value()`返回的对象被不同类型的变量接收时，就会根据接收变量类型的不同来调用不同的类型转换函数，而在不同的类型转换函数中，可以模拟对于不同返回值的函数重载。

当用标记为`auto`的变量去接收这个返回值时，`auto`会被推导为`Bool::_RetT`，并且不会调用任何类型转换函数。如果忽略返回值，也是同样的效果。