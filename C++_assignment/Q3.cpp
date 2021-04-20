#include <iostream>
using namespace std;

int main(){
    int int_arr[5];
    for(int i=0;i<5;i++){
        cout << "Enter elements: ";
        cin >> int_arr[i];
    }
    cout << "you entered"<<endl;
    for(int i=0;i<5;i++){
        cout << int_arr[i]<<endl;
    }
    return 1;
}