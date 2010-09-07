#include <iostream>
using namespace std;
class Father {
public :
	Father() { cout << "Father" << endl;}
};
class Son : public Father {
public:
	Son() { cout << "Son" << endl;}
};

int main(){

	Son *son = new Son();
	return 0;	
}
