arr = [1, 2, 3]
length = len(arr)
sum = 0

for i in range(length):
    if i == 0:
        sum += 0
    elif i == 1:
        if sum % 2 == 0:
            sum == 0
    else:
        sum += arr[i]

avg = sum / length