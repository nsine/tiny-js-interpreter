user_input = input('Enter array items through space: ')
arr_items = user_input.split(' ')
arr = []

for item in arr_items:
    arr.append(float(item))

length = len(arr)
sum = 0

for i in range(length):
    sum += arr[i]

avg = sum / length
print(avg)
