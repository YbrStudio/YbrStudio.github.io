# Cyan语言的类型系统
## 内置类型 <br> Built-in Types
+ **int** 整数
+ **float** 浮点数
+ **str** 字符串
+ **bool** 逻辑真假（布尔类型）
+ **null** 空值
+ **tuple** 元组
+ **list** 列表
+ **dict** 字典
+ **set** 集合

## 变量 <br> Variables
### 静态类型变量 <br> Static Typing Variables
#### 定义 <br> Definition
**静态类型变量（Static Typing Variable）** 是指只能保存特定的单一类型（以及这个类型的[兼容类型](#type-compatibility)）的对象的变量。使用如下格式来定义静态类型变量。
```Cyan
let a: int = 1;
```
其中，`let`是定义静态类型变量的*关键字（Keyword）*，`a`是*变量标识符（Identifier）*，`: int`是*类型指定（Type Designation）*语法，`= 1`是在定义变量时同时进行赋值（初始化）。

一条`let`语句可以定义多个变量，以下两种写法均可（第二种写法实际上是*解包*元组）。
```Cyan
let a: int = 1, b: int = 2;
let a: int, b: int = 1, 2;
```

#### 不可变变量与可变变量 <br> Immutable Variables and Mutable Variables
默认情况下，定义的静态类型变量是**不可变变量（Immutable Variable）**，即初始化之后，你将不能改变它的值。
```Cyan
let a: int = 1;
a = 2;  // 编译错误
```
之所以这样设计，是因为在实际的工程中，大多数变量都是无需改变值的，这样设计能避免许多意外错误发生，并对性能优化提供更多的可能。

如果需要变量可变，可以使用`mut`关键字。注意，按语义来拆分的话，`mut a`是一个整体，而非`let mut`，因此，同一个`let`语句可以同时定义可变变量和不可变变量。
```Cyan
let mut a: int = 1, b: int = 2;
a = 2;  // OK
b = 1;  // 编译错误
```
静态类型变量即使可变，也无法保存其他（不兼容）类型的对象。
```Cyan
let mut a = 1;
a = true;  // 编译错误
```

#### 无初始化定义 <br> No-Initialization Definition
很多时候，在我们定义变量的时候是不需要或者无法初始化的，但在Cyan中，定义变量时不初始化会引发编译错误，这是为了防止开发者忘记初始化而导致错误。如果开发者确定不需或无法初始化变量，并在之后使用到该变量时该变量会被正确赋值，可在定义变量时使用`lateinit`关键字来标注。由于`lateinit`标注的定变量义都是没有初始化的，而这与不可变变量的“保持初始化的值不变”冲突，所以`lateinit`无法修饰不可变变量定义，而只能修饰可变变量定义。
```Cyan
let a: int;  // 编译错误
lateinit let b: int;  // 编译错误
let mut c: int;  // 编译错误
lateinit let mut d;  // OK
```
虽然`lateinit`会让未被初始化的变量通过编译，但在运行时，如果变量在被使用的时候仍未被赋值，则会引发运行时错误。
```Cyan
lateinit let mut a: int;
print(a);  // 编译错误：变量`a`尚未被赋值
```

#### 自动类型推导 <br> Automatic Type Derivation
为每一个变量进行类型指定是十分麻烦的，对此，Cyan提供了**自动类型推导（Automatic Type Derivation）**，即在定义变量时，如果指定了初始值，则在可以不进行类型指定，而由编译器自动推导类型。
```Cyan
let a = 1;  // 由初始值`1`自动推导出`a`的类型为`int`
```
显然，如果定义时没有初始值，则无法进行自动类型推导，所以自动类型推导与`lateinit`是冲突的。
```Cyan
lateinit let a;  // 编译错误：无法确定`a`的类型
```
由编译器自动推导出的类型严格等于初始值的类型，但手动指定的类型则不然，手动指定的类型可以是初始值的类型或者是该类型的父类型。
```Cyan
let a = 1;  // 自动推导为`int`类型
let b: float = 1;  // 指定为`float`类型
```

#### 类型兼容 <br> Type Compatibility
若`T`类型的静态类型变量，可以保存`U`类型的对象，则称类型`T`对`U`**类型兼容（Type Compatible-with）**，或类型`U`兼容于`T`。
```Cyan
let a: int = 1;
let b: float = a;  // 类型`float`兼容`int`，可直接赋值
```
需要注意的是，这个以上代码并没有将`a`的类型转换为`float`，最后`b`的运行时实际类型是`int`。也就是说，类型兼容只是编译期类型检查时的概念。

类型`T`对`U`兼容，意味着任何`U`类型的对象都可以当作`T`类型的对象处理。这种关系对于父类和子类来说是与生俱来的，所有父类都兼容子类。类似地，实现了某个`trait`的类型也兼容于该`trait`。

`float`与`int`的语言层面兼容是因为二者同时满足了内置的`number`特征。而`float`是`number`的**默认实现（Default Implement）**，所以你可以像使用`: number`一样使用`: float`。所以在类型指定处的`float`实际上是指`number`特征。
```Cyan
trait number {}
impl number as float {}
class int : number {}
```
这里再给出一个类似的长方形和正方形的例子：
```Cyan
trait Rectangle {
    property a: float;
    property b: float;
    fn compute_area(self) -> int;
}

impl Rectangle(let mut a: float, let mut b: float) {
    property a => self.a;
    property b => self.b;

    fn compute_area(self) {
        return self.a * self.b;
    }
}

class Square(let mut l: float) : Rectangle {
    property a => self.l;
    property b => self.l;

    fn compute_area(self) {
        return self.l ** 2;
    }
}

let mut rect: Rectangle = Rectangle(1.5, 3);
rect = Square(4);
```

### 动态类型变量 <br> Dynamic Typing Variables
**动态类型变量（Dynamic Typing Variables）** 是指可以先后保存不同（即使是不兼容的）类型的对象的变量。动态类型变量的定义与静态类型变量的定义十分相似，只是变为使用`var`关键字。
```Cyan
var a: int = 1;
```
动态类型变量可以保存不同类型的变量。由于这个特点，动态类型变量是生来就是可变的，再使用`mut`会引发编译错误。
```Cyan
var a: int | str | bool = 1;
a = "Hello";
a = true;

var mut b = 1;  // 编译错误
```
与静态类型变量类似，如果想要定义动态类型变量时不初始化，使用`lateinit`关键字。
```Cyan
lateinit var a: int;
a = 1;
```

#### 动态类型变量的自动类型推导 <br> Automatic Type Derivation of Dynamic Variables
动态类型变量也有自动类型推导功能，但与静态类型变量不同的是，动态类型变量是在整个作用域内查找所有有可能被赋值为的类型，将类型推到为这些类型的集合。
```Cyan
var a = 1;
if input() == "str" {
    a = "str";
} else {
    a = false;
}

if input() == "quit" {
    a = null;
}
// 最后推导变量`a`的类型为`int | str | bool | null`
```
由于动态类型变量类型的推导不需要初始值，所以即使是`lateinit`的变量定义也可以不进行类型指定。
```Cyan
lateinit var a;
a = 1;
```

#### 动态类型变量的类型检查 <br> Type Checking of Dynamic Variables
动态类型变量的类型检查相较静态类型变量宽松得多，这也带来了它强大的灵活性。

对于在定义时候有了类型指定的变量，将其他（不兼容）类型的对象赋值给改变是不合法的。
```Cyan
var a: float | str = 3.14;
a = "Hello";  // OK
a = 1;  // OK：`float`兼容`int`
a = true;  // 编译错误
```

对于定义时没有进行类型指定的变量，任意的赋值都是合法的，参见上一节[动态类型变量的自动类型推导](#automatic-type-derivation-of-dynamic-variables)。

当使用动态类型变量时，如果动态类型变量的类型的每一部分都兼容于所需变量，那么可以直接使用；完全不兼容，则会触发编译错误；一部分兼容时，直接使用也会触发编译错误，如果开发者确定在实际运行时类型一定是合法的，则需要在变量标识符之后加上`'`标识进行**类型保证（Type Assurance）**。
```Cyan
var a: int | str = 1;
var b: float | str = a;  // `float | str`完全兼容`int | str`

var c: int | str = 1;
let d: int = c;  // 编译错误：`int | str`部分兼容于`int`
let e: int = c';  // OK：开发者自行保证此处类型正确，并用`'`标识

var f: int | str = 1;
var g: bool | null = f;  // 编译错误
var h: bool | null = f';  // 编译错误
```

如果使用类型保证通过了编译，但开发者实际上没有确保此处的类型正确，那么在Debug模式下，会在运行时变量被使用的时候报错；在Release模式下，会运行直到产生了致命错误。
```Cyan
var a: int | str = "Hi";
let b: int = a';  // 使用了类型保证，但是实际上类型并不正确。在Debug模式下，运行到此处就会报错。
let c: int = b + 1;  // Release模式下，此处报错：`str`类型的对象无法与`int`类型的对象相加。
```

## For循环的迭代变量 <br> Iteration Variables of For-loop
除了使用`let`和`var`关键字创建变量，在一些情况下一些变量也会被隐式地创建，比如在for循环中。
```Cyan
let data = [1, 2, 3, 4, 5];

for i in data {  // 此处隐式地创建了变量`i`
    print(i);
}
```
迭代变量默认是不可变的，也就是说在循环体中不能改变循环变量。
```Cyan
let data = [1, 2, 3, 4, 5];

for i in data {
    i = 1;  // 编译错误
}
```
如果想要改变迭代变量，需要在迭代变量名之前加上`mut`关键字。
```Cyan
let data = [1, 2, 3, 4, 5];

for mut i in data {
    print(i);
    i = -i;
    print(i);
}
```
至于迭代变量是静态的还是动态的，取决于被迭代对象（更准确地说，与被迭代对象的`.__iter__`函数返回的迭代器的类型的`.__next__()`函数的返回值决定）。

## 参数传递 <br> Parameters Passing
!!! note "未完待续"