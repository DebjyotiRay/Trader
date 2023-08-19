#include<bits/stdc++.h>
using namespace std;

    int reverse(long long int x) {
        
        if(x>pow(2,31)-1 || x<-pow(2,31))
            return 0;
        long long int d=abs(x);
        long long int t=0;
        
        while(d!=0)
        {
            t=t*10+(d%10);
            d/=10;
        }
        if(x>0)
        return t;
        else
        return t-2*t;
        
    }
int main(){
   long long int x;
        cin>>x;
        cout<<reverse(x);
}