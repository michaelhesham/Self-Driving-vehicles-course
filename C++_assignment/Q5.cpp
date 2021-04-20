#include <iostream>
using namespace std;

int main(){
    int data[100];
    int num_of_data,average;
    cout << "Enter numbers of data: ";
    cin >> num_of_data;
    for(int i; i < num_of_data; i++){
        cout << "Enter number " << i+1 << " : ";
        cin >> data[i]; 
    }
    for(int i; i < num_of_data; i++){
        average += data[i]; 
    }
    cout << "Average of numbers you entered = "<<average/num_of_data<<endl;
    return 1;
}