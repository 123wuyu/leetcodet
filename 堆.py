'''
堆的定义
堆 是一种特别的二叉树

堆的使用场景就是：动态求极值。
其中动态和极值两个条件缺一不可。即当我们遇到题目需要对一个数组进行持续的插入、删除，然后最终求top(N)问题时，不用想必然是堆排序问题

堆的分类：
最大堆：堆中每一个节点的值 都大于等于 其孩子节点的值。所以最大堆的特性是 堆顶元素(根节点)是堆中的最大值。
最小堆：堆中每一个节点的值 都小于等于 其孩子节点的值。所以最小堆的特性是 堆顶元素(根节点)是堆中的最小值。

Python 只有小根堆
'''

import heapq

# # 方法1
# nums = [2, 5, 1, 7, 9, 10, 3, 4]
# heap = []
# for num in nums:
#     heapq.heappush(heap, num)    # heapq.heappush() 把值加入堆中
# while heap:
#     print(heapq.heappop(heap))

# 方法2
nums = [2, 5, 1, 7, 9, 10, 3, 4]
heapq.heapify(nums)  # heap.heapify(list)转换列表成为堆结构
print(nums)
print([heapq.heappop(nums) for _ in range(len(nums))])  # 堆排序
