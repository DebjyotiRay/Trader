#include<bits/stdc++.h>
using namespace std;
const int N=1e5+10;
int dp[N];
int a[N];
int func(int n){
    if(n==0)    return n;
    int cost= INT_MAX;
    if(dp[n]!=-1)
        return dp[n];
    cost = min(cost, func(n-1)+ abs(a[n]-a[n-1]));
    if(n>1)
        cost = min(cost, func(n-2)+ abs(a[n-2]-a[n]));
    return dp[n]=cost;
}
    int main() {
        int n;
        cin>>n;
        
        for(int i=0;i<n;i++)
            cin>>a[i];
        memset(dp, -1, sizeof(dp));
       cout<<dp[n-1]<<endl;
       return 0;
             }
    