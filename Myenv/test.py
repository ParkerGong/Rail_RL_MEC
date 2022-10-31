# class A(object):
#     def __init__(self):
#         print("class ---- A ----")
#         super(A, self).__init__()


# class C(A):
#     def __init__(self):
#         print("class ---- C ----")
#         super(C, self).__init__()
# class B(A):
#     def __init__(self):
#         print("class ---- B ----")
#         super(B, self).__init__()


class D:
    def __init__(self):
        print(D.mro())
        print("class ---- D ----")
        super(D, self).__init__()


d = D()
