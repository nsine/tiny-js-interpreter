var user_input = input('Enter number: ');
var n = parseFloat(user_input);

var isPrime = true;

for (var i = 2; i <= Math.sqrt(n); i = i + 1) {
    if (n % i == 0) {
        isPrime = false;
    }
}

if (isPrime) {
    print('n is prime');
} else {
    print('n is not prime');
}