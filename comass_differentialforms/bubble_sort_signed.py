def bubble_sort_signed(index: tuple):
    '''Bubble sort for an array, also returns a sign, which counts the parity of the number of swaps'''
# This is taken from https://realpython.com/sorting-algorithms-python/.
    array = list(index)
    n = len(array)
    n_swaps = 0
    sign = 1
    for i in range(n):
        # Create a flag that will allow the function to terminate early if there's nothing left to sort
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] == array[j + 1]:
                return tuple(array), 0

            if array[j] > array[j + 1]:
                # If the item you're looking at is smaller than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]
                n_swaps += 1
                # Since you had to swap two elements, set the `already_sorted` flag to `False` so the algorithm doesn't finish prematurely
                already_sorted = False
        if already_sorted:
            break
        sign = 1 if n_swaps%2 == 0 else -1
    return tuple(array), sign

if __name__ == '__main__':
    print( bubble_sort_signed([1,3,5,4,31,32,56,1]) )