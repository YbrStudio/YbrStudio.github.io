# 内置类型
Cyan语言提供了许多的**内置类型（Builtin Type）**，可以大致分为以下三类：

+ **基本类型**
    + `int` 整数类型
    + `float` 浮点数类型
    + `str` 字符串类型
    + `bool` 布尔类型
+ **容器类型**
    + `tuple` 元组类型
    + `list` 列表类型
    + `dict` 字典类型
    + `set` 集合类型
+ **枚举类型**
    + `Optional` 可选类型
    + `Result` 结果类型

## 数字类型
### 整数类型
Cyan语言中的整数正常情况下底层使用`long long`实现，在64位系统上表达范围为`[-2^63, 2^63-1]`。一旦在编译时发现了超出这个范围的常量，或者在运行时运算结果出现了溢出，Cyan会自动将该`int`对象转换为高精度实现。转换为高精度的实现后数据表达范围理论上将没有限制。总的来说，**Cyan中的整数类型的表达范围没有限制**。
```Cyan
let a: int = 2 ** 128;  // OK
let b: int = 2 ** 128 + 1;  // OK
let c: int = a * b;  // OK
```

### 浮点数类型
Cyan语言中浮点数使用`double`实现，并且没有类似`int`的高精度支持，这导致**浮点数的表达范围是有限的**（与`C/C++`中`double`相同）。当浮点数在编译期溢出(1)时，会引发编译错误；而当运行期溢出时，会返回`inf`或`-inf`，并抛出一个警告。
{.annotate}

1. 编译期溢出是指编译期能确定的常量表达式中出现的浮点数运算结果溢出的情况。例如`let a = 2.0 ** 1024;`

<!-- 让我借用一下C的代码块，不然inline-annotation识别不到 -->
```c
let a = 2.0 ** 1024;  // 编译错误
let b = 2.0 ** 1023;
let c = b * 2;  // (1) 警告：发生了浮点数运算溢出，结果为`inf`
print(c);  // inf
```

1. 如果在编译时开启了**极限常量优化**，编译器会自动检测到`b`的值与外界输入无关，所以在编译期将`b * 2`展开为`2.0 ** 1024`，导致结果并非是运行时警告，而是编译错误。

### 整数和浮点数的转换
在[静态类型变量](./STV.md)中我们提到，静态类型变量只能保存一种类型的对象。但`float`类型的静态类型变量可以保存`int`类型的对象，反之不能 (1)。如果要将`float`对象赋值给`int`类型的静态类型变量，需要使用`as`关键字进行类型转换。同时要注意的是，当`int`对象被赋值给`float`类型的静态类型变量时，该类型实际储存的对象的类型仍是`int`，这个过程中没有新对象产生。
{.annotate}

1. 之所以允许`float`类型的静态类型变量保存`int`类型的对象，是因为`float`类型兼容`int`类型，详见[类型兼容性](./type_compatibility.md)。

```Cyan
let mut a: int = 42;
let mut b: float = 3.14;

b = a;  // OK
a = b;  // 编译错误
a = b as int;  // OK
```

```Cyan
let mut a: int = 42;
let mut b: float = 3.14;

b = a;
print(typeof(b));  // int
print(a is b);  // true
```

### 不合法的数字运算
在Cyan语言中，当出现了数学上不合法的运算时，会产生错误`MathError`，无论是在编译期还是运行期。

<!-- 让我借用一下C的代码块，不然inline-annotation识别不到 -->
```c
from math import sqrt;

let a = 1 / 0;  // 编译错误

let b = 0;
let c = 1 / b;  // 运行时错误 (1)

let d = sqrt(-1);  // 运行时错误
```

1. 假设没有开启极限常量优化


## 字符串类型
Cyan中的字符串完全支持Unicode字符集。底层根据字符串内容自动选择`Latin-1`、`UCS-2`或`UCS-4`编码。

字符串支持Unicode字符的`O(1)`级别随机访问和长度获取。此外还支持切片、负数索引等操作。
```Cyan
let string: str = "Hello,世界🌏";
print(len(string));  // 9
print(string[6]);  // 你
print(string[6:8]);  // 世界
print(string[-1]);  // 🌏
```