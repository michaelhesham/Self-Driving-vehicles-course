#include <iostream>
using namespace std;

class AddComplex{
    public:
        int real, img;
};
int main(){
    AddComplex first,second;
    cout << "First number"<<endl<<"Enter the real part: ";
    cin >> first.real;
    cout << "Enter the imaginary part: ";
    cin >> first.img;
    cout << "Second number"<<endl<<"Enter the real part: ";
    cin >> second.real;
    cout << "Enter the imaginary part: ";
    cin >> second.img;
    cout << "sum of real parts is "<< first.real+second.real<<endl;
    cout << "sum of img parts is "<< first.img+second.img<<endl;
    return 1;
}