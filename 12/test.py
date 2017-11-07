# #1
# def fun(a,b,c):
#     print a+b+c
#
# fun(b="asdlfjasdf",c="cccccccccccccccccccccccccc",a="1212")
# #2
# d = {'hello': 'world'}
#
# print d.get('hello', 'default_value')
a = [3, 4, 5]
# b = []
# for i in a:
#     if i > 4:
#         b.append(i)
# print b

b = filter(lambda x: x > 4, a)
print b