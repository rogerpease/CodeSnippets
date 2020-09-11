#include <iostream> 
#include <vector> 
#include <assert.h> 

//
// Copyright (C) 2020 Roger D. Pease
//
//
// This is the obligatory "swap the elements in a matrix" programming exercise. 
// Of course I could always make these member functions of a Matrix object. :)  
//
//
// This should compile with just:
//       g++ MatrixReverse.cpp
//  I used g++ 7.5.0 for Ubuntu. 
// 
//
// Next steps are: 
//    Try to performance profile different revsersing methods. 
//    Do Matrix reversing in OpenCL.
// 
//

//
// Obligatory versioning string. 
//

const std::string VERSION="0.1.0"; 

// Save myself from std:: prependages. 

using namespace std; 

typedef vector<vector<int>> MatrixType; 

//
//  Print the matrix (useful for debugging) 
//

void printMatrix (MatrixType & matrix) 
{ 
  for (auto & row: matrix) 
  {
    for (auto & col : row)
      cout << col << " ";
    cout << "\n"; 
  }
}

//////////////////////////////////////////////////////
//
// This is an in-place reversal. 
//
//  Take:   1 2 3 
//          ...                                                  
//          7 8 9 
//
// return:   9 8 7 
//           6 5 4 
//           3 2 1 
//
//  Assumes the matrix is rectangular. 
//

void reverseMatrixInPlace (MatrixType & matrix)
{
  
  // 
  // Swap elements in each row. There is probably a cutesy way to do this with std::vector arithmetic.  
  // 

  for (int i = 0; i < matrix.size();i++)
  { 
     auto  &   vector     = matrix[i]; 
     const int vectorsize = vector.size(); 
     for (int j=0;j <= vectorsize/2; j++) 
     {
       std::swap(vector[j], vector[vectorsize-1-j]);
     } 
  } 

  // 
  // Swap rows. 
  //
  for (int i = 0; i <= matrix.size()/2;i++)
      std::swap(matrix[i], matrix[matrix.size()-1-i]);

}


int main () {

   const int rows = 5; 
   const int cols = 5; 

   MatrixType matrix = { 
     { 0,1,2,3,4},
     { 5,6,7,8,9},
     { 10,11,12,13,14},
     { 15,16,17,18,19},
     { 20,21,22,23,24}};
   
   // Make a copy so I can compare the two 
   MatrixType newmatrix = matrix;  

   printMatrix (newmatrix); 
   reverseMatrixInPlace(newmatrix);

   // Some testing of course! 

   assert(newmatrix[0][0] == matrix[4][4]); 
   assert(newmatrix[4][4] == matrix[0][0]); 
   // Test the contra-case just to make sure my assertions are working properly. 
   assert(!(newmatrix[3][3] == matrix[0][0])); 

   // And print just to show myself it executed! 
   printMatrix (newmatrix); 

}


