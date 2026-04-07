# heap sort implementation from lowest to highest priority
def heap_sort(tasks):
    # check if there are no tasks
    if not tasks:
        return []

    # create a copy,  avoid change the original list
    arr = tasks.copy()
    n = len(arr)

    # build a max heap ,start from the last parent node
    for i in range(n // 2 - 1, -1, -1): # n // 2 - 1 is the index of the last parent node
        _heapify(arr, n, i)

    # extract elements
    for i in range(n - 1, 0, -1):
        # swap root and heapify the reduced heap
        arr[i], arr[0] = arr[0], arr[i]
        _heapify(arr, i, 0)

    return arr

def _heapify(arr, n, i):
    largest = i
    left = 2 * i + 1 # left child index
    right = 2 * i + 2 # right child index

    # compare with left child and right child
    if left < n and arr[left].priority > arr[largest].priority:
        largest = left
    if right < n and arr[right].priority > arr[largest].priority:
        largest = right

    # if current node is not the largest, swap and continue
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)