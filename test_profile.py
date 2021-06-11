# import line_profiler
# import time
# profile = line_profiler.LineProfiler()
#
# #@profile
# def main():
#     for i in range(10):
#         print('yes')
#         time.sleep(0.01)
#         for j in range(10):
#             time.sleep(0.001)
#             for k in range(5):
#                 time.sleep(0.001)
#
#
# main()
from __future__ import (
    print_function, division, unicode_literals, absolute_import)




#@profile
def fact2(n):
    result = 1
    for i in range(2, n + 1):
        result *= i * 2
    return result

#@profile
def sum2(n):
    result = 0
    for i in range(1, n + 1):
        result += i * 2
    return result
'''
if __name__ == "__main__":
    print(fact2(120))
    print(sum2(120))
'''
print(fact2(120))
print(sum2(120))
