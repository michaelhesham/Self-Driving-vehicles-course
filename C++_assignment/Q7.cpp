#include <iostream>
using namespace std;

class AddComplex{
    public:
        int real, img;
        void add_real(AddComplex x){
            cout << "sum of real parts is "<< real+x.real<<endl;
        }
        void add_img(AddComplex x){
            cout << "sum of img parts is "<< img+x.img<<endl;
        }
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
    first.add_real(second);
    first.add_img(second);
    
    return 1;
}