var user_input = console.input('Enter array items through space: ');
var arr_items = user_input.split(' ');

var arr = [];
var i = 0;

for (i = 0; i < arr_items.length(); i = i + 1) {
    arr.push(parseFloat(arr_items[i]));
}

var length = arr.length();
var sum = 0;

for (i = 0; i < length; i = i + 1) {
    sum = sum + arr[i];
}

var avg = sum / length;
console.log('Result:', avg);
