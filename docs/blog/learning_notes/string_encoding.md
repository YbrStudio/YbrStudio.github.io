# Unicode字符集、常见的编码与不同编程语言使用的编码策略

!!! note "写在前面"
    本文是半笔记半教学性质的文章，即这是作者在学习相关知识时为加深理解所作的笔记，希望对大家也能有所帮助。
    本文如有错误或不周全之处，欢迎指出，不胜感激。
    
!!! tip "阅读建议"
    阅读难度：中

## Unicode
**Unicode**是一个字符集，囊括了了世界上绝大部分的常用文字。

### 字符和字素群
Unicode 把**字符（characters）**定义为有语义的、可独立存在的最小书写单位。多个 Unicode 字符可以组合成视觉上的另一个字符，这种组合称为**字素群（grapheme clusters）**。例如，字素群 á 由两个字符组成：拉丁字母 a 和重音符 ´。出于兼容考虑，有些字素群也会被编码成单独的字符。这种组合设计使 Unicode 能表示各种各样的字素群，同时又保持字符集相对简单。

### 映射关系
Unicode规定了每个字符与一个二进制数的一一映射关系，这个二进制数的范围是 `0` ~ `1 0000 1111 1111 1111 1111`，用十六进制来表示就是 `0x0` ~ `0x10FFFF`。
如果你想查看具体的映射关系，在[此处](https://symbl.cc/cn/unicode/table/)查看。

我们将每个字符对应的二进制数称作**码点（code point）**，码点的表示方式是`U+`加上二进制数的十六进制表示，例如 `U+0061` 表示字符 `a`。

### 平面
每16位二进制数表示的范围被称作一个**平面**，第一个平面是**基本多语言平面**，用于与常用的字符对应。剩余十六个平面称为**辅助平面**，与一些辅助字符对应。

在基本多语言平面中，有两个范围没有对应字符，分别是 `1101 1000 0000 0000` ~ `1101 1011 1111 1111` 和 `1101 1100 0000 0000` ~ `1101 1111 1111 1111`，用十六进制表示为 `0xD800` ~ `0xDBFF` 和 `0xDC00` ~ `0xDFFF`，之所以没有对应字符，其实是为了保留给utf-16编码，前一个范围称为高位代理，后一个范围称为低位代理。这两个代理区域合在一起的十六进制表示的范围是 `0xD800` ~ `0xDFFF`。

## 支持Unicode的常见编码
需要注意的是，Unicode只是定义了字符和码点的映射关系，而不规定以何种方式存储码点。但在实际使用中，我们要考虑如何来储存码点，码点的存储方式称为**编码（encoding）**。

### utf-32
**utf-32（32-bit Unicode transformation format）**是32位的**定长编码**，**每个字符占4个字节**。

显然，3个字节就可以储存任何一个码点（如你忘了的话，码点范围：`0x0` ~ `0x10FFFF`），使用4个字节储存一个字符的码点的utf-32编码太过浪费空间。但是这是一种最简单、最直观的编码方式，而且操作起来的时间复杂度也最简单，因为utf-32是定长的。

### utf-16
那么如果使用3个字节来保存一个码点呢？实际上，位于辅助平面的字符很少被使用，为了保存辅助平面上的字符而把所有码点都用3个字节来储存，仍然很奢侈。于是我们可以使用一种变长的编码方式，用四个字节（之所以不用三个字节见后文）保存辅助平面上的码点，使用两个字节保存基本平面上的码点（如果你忘了的话，基本平面上的码点范围：`0x0` ~ `0xFFFF`）。这种编码方式就是**utf-16**。

但是这样还有一个问题，一旦我们使用了变长编码，我们就分不清一个字符是以四个字节表示还是以两个字节表示，那就势必要在Unicode中保留一些有特定前缀区域来作为区分，这就是上文提到的基本多语言平面的保留区域（如果你忘了的话：高位代理`1101 1000 0000 0000` ~ `1101 1011 1111 1111`，低位代理`1101 1100 0000 0000` ~ `1101 1111 1111 1111`）。具体的utf-16编码方式是这样的：

+ 如果 unicode编码 <= `0xFFFF`，直接用两个字节存unicode编码
+ 如果 unicode编码 > `0xFFFF`，先计算 U = unicode编码 - 0x10000，然后将 U（U的范围是`0x0` ~ `0xFFFFF`） 写成二进制形式，并从中间分成两部分（这里用`x`和`y`表示）：`xxxx xxxx xxyy yyyy yyyy` ，接着用4个字节这样存：`110110xx xxxxxxxx 110111yy yyyyyyyy`，这里的`110110yy`和`110111xx`其实就是分别位于高位代理和低位代理。

utf-16是一种巧妙的编码，但是由于它是变长编码，它的随机访问、获取字符串长度等操作的时间复杂度在不使用额外优化的情况下达不到常数级别。

### UCS-2编码
UCS-2是utf-16的简化版，或者说是子集。它是一种**定长编码**，只**使用两个字节储存一个字符**，这就不可避免地导致了UCS-2只能存储基本平面上的字符，也就是说**UCS-2不完全支持Unicode**，**不能正常存储辅助平面上的字符**。不过UCS-2仍能储存大部分的常用字符，而且随机访问、获取字符串长度等操作的时间复杂度在常数级别。

### utf-8编码
虽然utf-16已经很大程度地节约了空间，但是对于纯ASCII字符串，utf-16对每个字符的两个字节中都有一个是全0的，这也很浪费空间。**utf-8**编码是一种**变长编码**，使用1个、2个、3个或4个字节保存一个字符，并**兼容ASCII**。

utf-8编码的具体实现是这样的：

+ 对于ASCII字符（Unicode码点的范围是`0x0` ~ `0x7F`），直接用一个字节存储，该字节由0开头，后面的7位置保存码点数据。这和ASCII编码是完全兼容的。
+ 对于不能用ASCII编码表示的字符，按需使用2个、3个或4个字节来存储。对于使用n个字节储存的字符，每个字符的第一个字节由n个1和一个0开头，后面n-1个字节由`10`开头，剩下的位置保存码点数据。

这样看上去可能不太直观，那就看下面这个表格：

Unicode码点范围    | utf-8二进制格式
:-----------------|:---------------
0x0 ~ 0x7F        | 0xxxxxxx
0x80 ~ 0x7FF      | 110xxxxx 10xxxxxx
0x8000 ~ 0xFFFF   | 1110xxxx 10xxxxxx 10xxxxxx
0x10000 ~ 0x10FFFF| 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx


### UCS-4
**UCS-4**使用4个字节保存一个字符的码点，UCS-4与utf-32暂时是相同的。

### Latin-1
**Latin-1**使用一个字节保存一个字符，但是这个字符只能是一个字节表达范围内的字符，即`0x0` ~ `0xFF`，也就是说**Latin-1不完全支持Unicode**。在`0x00` ~ `0x7F`之间的Latin-1字符，都与ASCII编码兼容。

## 不同编程语言中的字符串编码策略
### C/C++
C中的字符串`char[]`，以及C++中的STL字符串`std::string`，实际上本质都是**字节序列**。这种结构天然符合ASCII/UCS-1编码，但是处理起Unicode字符就非常痛苦了。还有一点就是，C/C++中字符串字面量的编码取决于源码文件的编码。

```C++ title="以utf-8编码的C++源码文件"
#include <iostream>
#include <string>

using namespace std;

int main() {
    system("chcp 65001 > nul");  // 在windows上将控制台编码设置为utf-8

    string str = "你好";
    cout << str.length() << endl;
    cout << str[0] << endl;
    cout << str.substr(0, 3) << endl;
}
```

```output title="输出"
6
�
你
```
之所以第一行输出6，是因为C++字符串的长度是字节数，而不是Unicode字符的个数。大多数中文字符在utf-8编码中占3个字节。
而第二行输出错误（这是我在我的电脑上g++编译后的输出，在不同的平台和编译器上表现可能不同，但都不会输出'你'），这是因为`str[0]`取出的是字符串的第一个字节，而非字符。
第三行输出`你`，是因为使用`substr`将`'你'`在utf-8中的三个字节全都取出来了，所以能正常输出。

C++ STL还提供了`std::u16string` `std::u32string` 等字符串，它们的数据不是 `char`类型，而是`char16_t`和`char32_t`，他们可以更好地适应UCS-2和UCS-4编码。

### Python
Python的字符串在它的发展历史上经历了许多的变化，这里我们只讨论现代Python（Python 3.3及以后）的字符串处理方式。

Python的字符串根据它所需要保存的数据灵活选择编码，具体来说，根据字符串中码点的最大值，决定使用Latin-1、UCS-2还是UCS-4编码。下面是cpython的源码。

```C
typedef struct {
    PyObject_HEAD
    Py_ssize_t length;
    Py_hash_t hash;
    struct {
        unsigned int interned:2;
        unsigned int kind:2;
        unsigned int compact:1;
        unsigned int ascii:1;
        unsigned int ready:1;
    } state;
    wchar_t *wstr;
} PyASCIIObject;

typedef struct {
    PyASCIIObject _base;
    Py_ssize_t utf8_length;
    char *utf8;
    Py_ssize_t wstr_length;
} PyCompactUnicodeObject;

typedef struct {
    PyCompactUnicodeObject _base;
    union {
        void *any;
        Py_UCS1 *latin1;
        Py_UCS2 *ucs2;
        Py_UCS4 *ucs4;
    } data;
} PyUnicodeObject;
```
这种设计能让Python正确处理所有Unicode字符，并支持`O(1)`级别实现复杂度的随机访问和获取字符串长度。
!!! note "未完待续"

### Javascript
Javascript的字符串使用UCS-2编码，对于UCS-2无法表示的字符（辅助平面上的字符），使用两个“字符”（JS中的字符）表示，这就会导致一些问题。下面是一段javascript交互环境代码：
```javascript
> 'a'.length
1
> '你'.length
1
> '👌'.length
2
> 'a你👌2'[0]
'a'
> 'a你👌2'[1]
'你'
> 'a你👌2'[2]
'\ud83d'  // 这里并没有取出'👌'，而是取出了这个emoji的第一个字节
> 'a你👌2'[3]
'\udc4c'  // 这里取出的是emoji的第二个字节
> 'a你👌2'[4]
'2'
```

### rust
!!! note "未完待续"