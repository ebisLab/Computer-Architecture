# branch tables
# dispatch ables


def fun(x, y):
    print(f"fun1 {x} {y}")


def fun2(x, y):
    print("fun2")


def fun3(x, y):
    print("fun3")


def fun4(x, y):
    print("fun4")


def call_fun(n, x=None, y=None):
    """
    if n==1:
        fun()
    elif n==2:
        fun2()
    elif n==3:
        fun3()
    elif n==4:
        fun4()
        """

    branch_table = {
        1: fun,
        2: fun2,
        3: fun3,
        4: fun4,
        5: lambda x, y: print(f"lambda {x} {y}")
    }

    # make sure functions are bound o the table

    #     branch_table = {
    #     1: self.fun,
    #     2: self.fun2,
    #     3: self.fun3,
    #     4: self.fun4,
    #     5: lambda x, y: print(f"lambda {x} {y}")
    # }

    f = branch_table[n]
    f(x, y)


call_fun(2, 99, 100)
call_fun(3, 2, 3)
call_fun(5, 33, 44)


def foo():
    print("foo")


bar = foo
baz = foo
frotz = bar

foo()
bar()
baz()
frotz()
