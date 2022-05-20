# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 16:14
# @Author  : HQY
# @FileName: practice.py
# @Software: PyCharm
import queue
import threading
from multiprocessing import Process, Queue
import time,random,os
import subprocess

# class Student(object):
#
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
#     def print_score(self):
#         print('%s: %s' % (self.name, self.score))
#
# bart = Student('Bart Simpson', 59)
# lisa = Student('Lisa Simpson', 87)
# print(bart.print_score(),type(bart))
# print(lisa.print_score())


# class Test:
#     """
#     三种方法都可以通过实例来调用，但是静态方法和类的方法无法访问实例属性
#     普通方法不可以通过类名调用，但是静态方法可以
#     小结：普通方法可以通过self访问数实例属性
#     类方法可以通过cls访问类的属性
#     静态方法不可以访问，通过传值的方式
#     """
#     name = "test"
#     data = "this is data"
#     # 普通方法，可以通过self访问类的属性
#     def prt(self):
#         print(self.data)
#
#     # 类的方法，可以通过cls访问类的属性
#     @classmethod
#     def classMethod(cls):
#         print(cls.data,cls.name)
#
#     # 静态方法，不可以访问类的属性
#     @staticmethod
#     def sta(name):
#         print(name)
# if __name__ == '__main__':
#     Test().prt()
#     Test().classMethod()
#     Test().sta('123')
#



"""python的数据类型"""
# numbers 数字
# string  字符串
# list  列表
# tuple  元组
# dict  字典
# set  集合
import json

"""python中list、tuple、set、dict的区别"""
# # list是一种有序的集合
list = ['Michael', 'Bob', 'Tracy',"2"]
# print(list.remove("2"),list)
# print(list[-1])  # 可以通过索引访问list中的对象
# print(len(list))  # 可以通过len()函数获得list的个数
# print(list.append("kiki"),list)  # 可以通过append函数在list末尾追加元素
# print(list.pop(),list)  # 可以通过pop删除在list末尾元素
# print(list.insert(1,"niki"),list)  # 可以通过insert函数在list指定位置添加元素
# print(list.sort(),list)    # sort只是应用在list上的方法,就地排序，无返回值
# print(sorted(list))    # sorted是内建方法，可对所有可迭代的对象进行排序，返回新的list


# tuple是一种有序的列表，但是一旦初始化就不能修改，所以没有append/insert/pop这样的方法，也不能替换元素
tuple = ('Michael', 'Bob', 'Tracy',"9","9")
# print(tuple[-1])  # 可以通过索引访问tuple中的对象
# print(tuple.index("Bob"))  # 返回指定元素的下标
# print(len(tuple),sorted(tuple))  # 可以通过len()函数获得tuple的个数

# dict是以键值对的形式存在的，是一个无序的集合，速度快，占用内存大
dict = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
# dict["渔翁"]=100  # 可以通过dict["渔翁"]=100添加key和value
# print("Bob" in dict)  # 可以通过in判断key是否存在
# print(dict.get("Bob"))  # 可以通过get获取key的值
# print(dict.values())  # 可以通过.values获取全部key的值
# print(dict.items())   # 可以通过.items返回dict中所有的key和value值
# print(dict.pop("Bob"),sorted(dict))  # 可以通过pop删除key，对应的值也会被删除
# 无序且无重复的集合，可以做数学意义上的交集和并集
# 和dict类似，也是一组key的集合，但是不存储value值，且key不能重复
# 要创建一个set，需要提供一个list作为输入集合,不然就不是set类型
# s1 = set([1,2,3,"2sf"])
# s2 = set([2,3,4,5,"2fre"])
# x = set("asdhakjdaa")
# print(x)
# print(s1.add(99),s1)  # 可以通过add添加元素
# print(s1.remove(1),s1)   # 可以通过remove移除指定元素
# print(s1 & s2)  # 取两个集合的交集
# print(s1 | s2)  # 取两个集合的并集


# 这两个参数是什么意思：*args,**kwargs
# *args是可变参数，args接收的是一个tuple；
# **kw是关键字参数，kw接收的是一个dict。
# 以及调用函数时如何传入可变参数和关键字参数的语法：
# 可变参数既可以直接传入：func(1, 2, 3)，又可以先组装list或tuple，再通过*args传入：func(*(1, 2, 3))；
# 关键字参数既可以直接传入：func(a=1, b=2)，又可以先组装dict，再通过**kw传入：func(**{'a': 1, 'b': 2})。
# 使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。
# list=[1,3,4]
# tuple  = (2,4,6,8)
# dict = {"niki":"18"}
# def test(*args,**kwargs):
#     print(*args,**kwargs)
# print(test(list,dict,tuple,"1313123"))
# print(test(tuple))

# import functools
# # 希望在不改变now函数的基础上打印一些日志，使用装饰器
# def log(text):
#     def decorator(func):  # 这里是接收一个函数的意思并返回一个函数，实际输出的是中间的打印函数
#         @functools.wraps(func)  # 因为最后返回的函数名是wrapper的函数名而不是now的，所以这个就是要返回原函数本身的函数名
#         def wrapper(*args,**kwargs):  # 可以接受任意函数的调用
#             print('%s %s ():' % (text,func.__name__))   # func.__name__接收到的函数名称
#             print("~~~我是装饰器的打印~~~")
#             return func(*args,**kwargs)
#         return wrapper
#     return decorator
#
# # 谈一谈python装饰器（decorator）
# @log("开始执行")
# def now():
#     print("2013-4-5")
#  # 执行顺序：先执行log("开始执行")-->返回的是decorator函数-->再调用decorator函数，参数是now函数
#  #返回值最终是wrapper函数。
# print(now(),now.__name__)

# def log(fn):
#     @functools.wraps(fn)
#     def metric(*args,**kwargs):
#         print('%s 函数执行开始时间 %s ms' % (fn.__name__, 10.30))
#         print('%s 函数执行结束时间 %s ms' % (fn.__name__, 11.24))
#         return fn(*args,**kwargs)
#     return metric
#
# @log
# def date():
#     print("今天是周五")
#
# print(date(),date.__name__)





# 简单描述python的垃圾回收机制（garbage，collection）
# python多线程（multi-threading）
# 说明os、sys模块的不同，并列常用的模块方法
# 什么是lambda表达式？他有什么好处？
# f = lambda  x,y,z:x+y+z
# print (f(4,4,6))
# python中的pass语句的作用是什么？
# python里面如何拷贝一个对象
# import copy
# list = [1,2,4,[9,3,6]]
# l1 = copy.copy(list)
# l2 = copy.deepcopy(list)
# list.append("sign")
# list[3].append("niki")
# print(l1,l2)
# __new__和__init__的区别
# python中单下划线和双下划线分别是什么？
# 说一说python的自省


# from  random import randint
# num = randint(0, 5)
# # a = "yace"+str(num)
# print(num)


# from schedule.settings import DATABASES
# data = DATABASES["default"].get("PASSWORD")
# print(data)


# list = [
#     {
#         "model": "smg_app.user",
#         "pk": 1,
#         "fields": {
#             "login_name": "niki",
#             "password": "123456",
#             "nickname": "哈哈",
#             "role": 1,
#             "status": 1,
#             "add_time": "2022-03-26T15:11:44Z",
#             "update_time": "2022-03-27T15:11:49Z"
#         }
#     }
# ]
#
# print(list[0]["fields"].get("login_name"))

# list = [b'{\r\n    "login_name": "niki",\r\n    "password": "123456"\r\n}', \
#                    b'{\r\n    "login_name": "niki123",\r\n    "password": "666666"\r\n}', \
#                    b'{\r\n    "login_name": "niki555",\r\n    "password": "999999"\r\n}', \
#                    b'{\r\n    "login_name": "niki666",\r\n    "password": "999999"\r\n}'
#                    ]
# body = json.loads(list[0].decode())
#
# print(body.get("login_name"),type(body))

from random import randint
# payload = [{"login_name": "niki","password": "123456"},
#                         {"login_name": "niki123", "password": "666666"},
#                         {"login_name": "niki555", "password": "999999"},
#                         {"login_name": "niki55555", "password": "123456"},
#                    ]
# # print(payload[0]["login_name"])
# num = randint(0,3)
# d = json.dumps(payload[num])
# c = json.loads(d)
# name = c["login_name"]
# psw = c["password"]
# print(type(d),type(c),name,psw)
#
# num = randint(0, 1000)
# print("kkk"+str(num))

# class Student(object):
#
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
#     def print_score(self):
#         print('%s: %s' % (self.name, self.score))
#
#
#
# if __name__ == '__main__':
#     print(Student("niki",32).print_score())


"""python多线程"""
from multiprocessing import Pool
# import os, time, random
#
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(4)  # 同时跑4个进程
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i,))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')


"""
subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值。
其中的subprocess.call()则可以调用windows系统cmd命令行执行额外的命令。
"""
# print('$ nslookup')
# subprocess.Popen用来创建新的进程
# 管道PIPE：用来将一个程序的标准输出作为另一个程序的输入
# stdin, stdout, stderr：分别表示程序的标准输入、输出、错误句柄
# p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
# print(output.decode('unicode_escape'))
# print('Exit code:', p.returncode)


"""多进程"""
# # 写数据进程执行的代码:
# def write(q):
#     print('Process to write: %s' % os.getpid())
#     for value in ['A', 'B', 'C']:
#         print('Put %s to queue...' % value)
#         q.put(value)  # 把value写进消息队列
#         time.sleep(random.random())
#
# # 读数据进程执行的代码:
# def read(q):
#     print('Process to read: %s' % os.getpid())
#     while True:
#         value = q.get(True)
#         print('Get %s from queue.' % value)
#
# if __name__=='__main__':
#     # 父进程创建Queue，并传给各个子进程：
#     q = Queue()
#     # p = Pool(4)
#     pw = Process(target=write, args=(q,))
#     pr = Process(target=read, args=(q,))
#     # 启动子进程pw，写入:
#     pw.start()
#     # 启动子进程pr，读取:
#     pr.start()
#     # 等待pw结束:
#     pw.join()
#     # pr进程里是死循环，无法等待其结束，只能强行终止:
#     pr.terminate()


"""多线程"""
# balance=0
# lock = threading.Lock()
#
# def change_it(n):
#     global balance
#     balance = balance+n
#     balance = balance-n
#
# def run_thread(n):
#     for i in range(2000000):
#         lock.acquire() # 获取锁，为了防止修改冲突，造成数据有误
#         try:
#             change_it(n)
#         finally:
#             lock.release()  # 释放锁
#
#
# thread1 = threading.Thread(target=run_thread,args=(5,))
# thread2 = threading.Thread(target=run_thread,args=(5,))
#
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(balance)

"""多线程实战1"""
# def read():
#     for i in range(3):
#         print('在%s，正在读书' % time.ctime())
#         time.sleep(1)
#
# def write():
#     for i in range(3):
#         print('在%s，正在写字' % time.ctime())
#         time.sleep(1)
#
# def main():
#     read_thread = []
#     write_thread = []
#     for i in range(1,2):
#         t = threading.Thread(target=read)
#         read_thread.append(t)
#
#     for i in range(1,2):
#         t = threading.Thread(target=write)
#         write_thread.append(t)
#
#     for i in range(0,1):  # 取0的原因是为了获取read_thread和write_thread中的数据，下标是0
#         read_thread[i].start()
#         write_thread[i].start()
#
# if __name__ == '__main__':
#     main()

"""多线程实战2"""
class ReadThread(threading.Thread):
    def run(self):
        for i in range(3):
            print('在%s，正在读书' % time.ctime(),threading.current_thread())
            time.sleep(1)

class WriteThread(threading.Thread):
    def run(self):
        for i in range(3):
            print('在%s，正在写字' % time.ctime(),threading.current_thread())
            time.sleep(1)

def main():
    read_thread = []
    write_thread = []
    for i in range(1,2):
        t = ReadThread()
        read_thread.append(t)

    for i in range(1,2):
        t = WriteThread()
        write_thread.append(t)

    for i in range(0,1):  # 取0的原因是为了获取read_thread和write_thread中的数据，下标是0
        read_thread[i].start()
        write_thread[i].start()

if __name__ == '__main__':
    main()



























