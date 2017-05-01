let user_input = input('Enter array items through space: ');
let arr_items = user_input.split(' ');

let arr = [];

for (let i = 0; i < arr_items.length; i = i + 1) {
    arr.push(parseInt(item));
}

let length = arr.length;
let sum = 0;

for (let i = 0; i < length; i = i + 1) {
    sum = sum + arr[i];
}

let avg = sum / length;
print(avg);
