#include <vector>
#include <iostream> 
#include <assert.h> 

using namespace std; 

//
// Indexes into an array and returns a reference to the array value.
//  An example like this is pretty simple but you might use this for a complicated lookup of a function 
//  (a hash table or something like that) or maybe a query result (i.e. valueReference(a,maximum)). 
//  I use this in Perl with substr. I.E. substr("The Star",4,4) = "Rose"; returns "The Rose". 
//
int& myLvalueFunction (vector<int>& a, int index) 
{
   return (int&) a[index]; 
} 


int main() 
{

   vector<int> a         = {10,20,30};
   myLvalueFunction(a,1) = 600; 

   assert(a[0] == 10); 
   assert(a[1] == 600); 
   assert(a[2] == 30); 

}
