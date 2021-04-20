#include <iostream>
using namespace std;

int main(){
    int x[100];
    int num_of_elements,max_num=0;
    cout << "Enter number of elements (1 to 100): ";
    cin >> num_of_elements;
    for(int i=0;i<num_of_elements;i++){
        cout << "Enter number " << i+1 <<" : ";
        cin >> x[i];
    }
    for(int i=0;i<num_of_elements;i++){
        if(x[i]>max_num){
            max_num=x[i];
        }
    }
    cout << "Maximum number you entered is "<<max_num<<endl;
    return 1;
}