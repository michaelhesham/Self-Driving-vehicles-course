#include <iostream>
using namespace std;
class Add2Int{
    public:
        int first_num, second_num;
        Add2Int(int x, int y){
            first_num = x;
            second_num = y;
            cout << "numbers initialized" <<endl;
        }
        void add(){
            cout << "the addition result is: "<< first_num+second_num<<endl;
        }
};
int main(){
    int x,y;
    cout << "Enter first number: ";
    cin >> x;
    cout << "Enter second number: ";
    cin >> y;
    Add2Int obj(x,y);
    obj.add();
    return 1;
}