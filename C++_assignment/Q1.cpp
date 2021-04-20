#include <iostream>
using namespace std;

int main(){
    int x;
    cout << "Enter your favourite number from 1 to 100 : " ;
    cin >> x;
    if( x<100 && x>0){
        if(x==24){
            cout << "amazing!! that is my favourite number too"<< endl;
        }
        else{
            cout << "no really 24 is my favourite number"<< endl;
        }
    }
    else{
            cout << "number should be between 0 to 100"<< endl;
        }
    return 1;
}