# max heap implementation
class Heap:
    def __init__(self):
        # initialize an empty heap to store task objects
        self.heap = []

    # add new task to the heap
    def insert(self, task):
        self.heap.append(task) # add new task to the end
        index = len(self.heap) - 1
        self._heapify_up(index) # sift up to correct position

    # remove highest priority task
    def pop(self):
        # check if the heap is empty
        if not self.heap:
            return None
        # check if only one task, return it
        if len(self.heap) == 1:
            return self.heap.pop()

        # store the highest priority task and move last task to root
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0) # sift down to restore heap order
        return root

    # return highest priority task
    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]

    # re-heapify upwards to fix the heap order after adding a new element
    def _heapify_up(self, index):
        parent = (index - 1) // 2 # calculate parent index
        # check if current node has higher priority than parent, then swap them and continue
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    # sift down the element to restore heap order after a deletion
    def _heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # compare with left child and right child
        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left
        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        # if largest is not current node, swap and continue
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    # return a copy of all tasks, avoid change original heap
    def all_tasks(self):
        return self.heap.copy()