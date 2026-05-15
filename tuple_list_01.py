# tuple 元组 和 list 列表的区别
# 1. tuple 元组是不可变的，而 list 列表是可变的。这意味着一旦创建了一个 tuple，就不能修改它的内容，而 list 可以随时添加、删除或修改元素。
# 2. tuple 元组使用圆括号 () 来定义，而 list 列表使用方括号 [] 来定义。
# 3. tuple 元组通常用于存储一组相关的数据，例如一个人的姓名、年龄和性别，而 list 列表通常用于存储一组相似的数据，例如一系列数字或字符串。

# tuple 不可变的特性使得它在某些情况下更安全和高效，例如作为字典的键或者存储不需要修改的数据。而 list 的可变性使得它更灵活，适合需要频繁修改数据的场景。
# 下面是一个简单的示例，展示了 tuple 和 list 的区别：
# 定义一个 tuple，包含一个人的姓名、年龄和性别
person_tuple = ("Alice", 30, "Female")
print(person_tuple)  # 输出: ('Alice', 30, 'Female')
# 定义一个 list，包含一系列数字
numbers_list = [1, 2, 3, 4, 5]
print(numbers_list)  # 输出: [1, 2, 3, 4, 5]
# 尝试修改 tuple 中的元素会导致错误
# person_tuple[0] = "Bob"  # 这会引发 TypeError

'''
报错内容：
Traceback (most recent call last):
  File "D:\PythonProjects\learnTest\tuple_list_01.py", line 15, in <module>
    person_tuple[0] = "Bob"  # 这会引发 TypeError
    ~~~~~~~~~~~~^^^
TypeError: 'tuple' object does not support item assignment
'''

# 修改 list 中的元素是允许的
numbers_list[0] = 10
print(numbers_list)  # 输出: [10, 2, 3, 4, 5]

# 定义一个空的元组
t = ()
# 定义的不是tuple，是1这个数！这是因为括号()既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义,python解释器会把它当成数学公式中的小括号来解析，所以 t 的值就是 1，而不是一个包含一个元素的 tuple。
t = (1)
# 只有1个元素的tuple定义时必须加一个逗号,，来消除歧义
t = (1,)
# print(t)
t=(1, 2, 3)

print(t)