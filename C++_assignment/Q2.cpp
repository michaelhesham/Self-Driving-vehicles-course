#include <iostream>
using namespace std;

int main(){
int x,reversed=0,remainder;
cout << "enter an integer: ";
cin >> x;

while(x != 0) {
remainder = x%10;
reversed = reversed*10 + remainder;
x /= 10;
}
cout << "Reversed integer = " << reversed << endl;
return 1;
}
