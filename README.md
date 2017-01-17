# func_analyzer
通过分析objdump的结果，提供各种对可执行程序（带debug信息的）的结构信息

姿势准备

- 准备好一个要分析的ELF格式可执行文件。需要带有符号表。由于本工具使用二进制分析，没有符号表就没有办法取得函数列表。

- 将ELF文件反编译。可以使用这套命令xxxx-objdump -d elf file |xxxx-c++filt >/tmp/elffile.dis

- 如果想要分析某函数的调用信息，需要将elffile.dis使用文本编辑器打开。搜索相关函数名。可以看到，在函数的起始点，有一对尖括号，里面就函数名了。c和c++的函数名会有区别。c++的会包含函数的返回类型、模板以及参数类型列表和const。这些都是函数名的一部分，都是需要的。

函数基本信息分析：分析函数列表、函数大小以及函数是否呗调用。

- 使用命令python func_analyzer.py /tmp/elffile.dis csv>test.csv

- 使用电子表格打开生成的CSV文件。选择tab作为分割符号。

- 格式：函数名，函数机器码大小，函数是否被调用（由于是静态分析，只具有参考价值）

- 排序、求和还是画图随便。

函数调用图

- 使用命令 python func_analyzer.py /tmp/elffile.dis callgraph functionname

- 如果没有提供functionname，那么将会绘制全部函数。结果嘛，除了看起来很cool，毛用没有。。。

- 调用图会在当前目录下生成。目前应该会同时生成SVG和PDF。

- 注意：由于c++的函数名比较复杂，会含有空格和符号等。所以需要把用双引号扩起来。

# addr2func
通过16禁止地址找到在elf文件中对应的函数名称。

姿势准备

- 需要elf中具有symbol信息以及unwind信息。目前制支持arm。

调用方法

- python addr2func.py ELF ADDR
