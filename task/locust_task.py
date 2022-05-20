# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 19:40
# @Author  : HQY
# @FileName: locust_task.py
# @Software: PyCharm


# 启动命令：locust -f locust_task.py --host http://127.0.0.1:8880   或者 locust -f locust_task.py
# 链接：http://localhost:8089/

import json
from locust import TaskSet, task, HttpUser,constant
from random import randint
"""
1.实现基本的添加用户功能，输出响应，脚本正常
2.多用户随机添加：在AddTasks方法里面构造随机函数。-LR：参数化，Jmeter：参数化
3.添加初始化方法---on_start：类似构造方法，启动的时候首先执行，每个虚拟用户只执行一次
4.添加检查点。（断言）
在请求方法中，设置catch_response参数为True
用success或failure方法标注成功或失败
"""

class MyTasks(TaskSet):
    """
    创建测试任务类，需要继承TaskSet
    可以添加多个测试任务
    """
    # 每个测试任务，往往会以实例方法的形式来呈现
    # 同时需要使用task装饰器来装饰测试任务
    def on_start(self):
        # self.headers = {"content-type": "application/json"}
        # self.payload = [b'{\r\n    "login_name": "niki",\r\n    "password": "123456"\r\n}', \
        #            b'{\r\n    "login_name": "niki123",\r\n    "password": "666666"\r\n}', \
        #            b'{\r\n    "login_name": "niki555",\r\n    "password": "999999"\r\n}', \
        #            b'{\r\n    "login_name": "",\r\n    "password": ""\r\n}'
        #            ]
        self.payload = [{"login_name": "niki","password": "123456"},
                        {"login_name": "niki123", "password": "666666"},
                        {"login_name": "niki555", "password": "999999"},
                        {"login_name": "niki55555", "password": "123456"},
                   ]
        ran_num = randint(0, 100000)
        self.data = {"login_name": "yace"+str(ran_num),"password": "333333", "nickname":"压测昵称"}

        # self.login_task()


    def login_task(self):

        num = randint(0,3)
        # client类似request对象，get是请求方法，去压测那个接口
        # 数据格式化成str
        payload_str = json.dumps(self.payload[num])
        login_name = self.payload[num]["login_name"]
        with self.client.post("/smg_app/login/", data=payload_str,catch_response=True) as response:
            res = json.loads(response.content)
            # 断言
            if "登录成功" in res["msg"]:
                print("断言成功")
                response.success()
            else:
                print("断言失败")
                response.failure('Failed!')
            print(res,login_name)

    @task
    def add_task(self):
        wait_time = constant(3)
        # client类似request对象，get是请求方法，去压测那个接口
        # 数据格式化
        data_str = json.dumps(self.data)
        login_name = self.data["login_name"]
        with self.client.post("/smg_app/add_user/", data=data_str,catch_response=True) as response:
            res = json.loads(response.content)
            # 断言
            if "用户添加成功" in res["msg"]:
                print("断言成功")
                response.success()
            else:
                print("断言失败")
                response.failure('Failed!')
            print(res, login_name)
    
      

class RunTasks(HttpUser):
    """
    创建运行测试类，需要继承Locust父类
    """
    tasks  =  [MyTasks]  # 指定测试任务类，使用task_set覆盖父类的属性
    host = "http://127.0.0.1:8899"
    # host = "https://www.baidu.com"
    min_wait = 2000    # 指定启动任务间隔时间范围（单位毫秒）：2-5秒之间
    max_wait = 5000    # 使用min_wait、max_wait覆盖父类的类属性


