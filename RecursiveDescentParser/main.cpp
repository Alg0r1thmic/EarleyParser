#include <iostream>
#include <string>
#include <stdio.h>
using namespace std;
string x;
int i=0;
int parsesum();
int parseProduct();
int parseFactor();
int parsesum()
{
    int product=parseProduct();
    while(x[i]=='+')
    {
        ++i;
        int product2=parseProduct();
        product=product+product2;
    }
    return product;
}
int parseFactor()
{

    if(x[i]>='0' and x[i]<='9')
    {
        return x[i++]-'0';
    }
    else if(x[i] =='(')
    {
        i++;
        int sum=parsesum();
        i++;
        return sum;
    }
    else
    {
        cout << "expected digit  but  found " << x[i] << endl;
    }
}
int parseProduct()
{
    int fact1=parseFactor();
    cout << x[i] << endl;
    while(x[i]=='*')
    {
        i++;
        int fact2=parseFactor();
        fact1=fact1*fact2;
    }
    return fact1;
}

int main()
{
    x="2*3*4+5";
    int result=parsesum();
    cout << result << endl;
}
