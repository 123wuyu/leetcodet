import heapq


nums = [2,5,1,7,9,10,3,4]
heap = []
for num in nums:
    heapq.heappush(heap, num)
    print(heap)

while heap:
    print(heapq.heappop(heap))