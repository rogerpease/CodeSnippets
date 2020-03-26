//
// Simple program to show I'm familiar with Parsing JSON and using BOOST. 
//  I wrote this myself, obviously borrowing from sources such as Boost docs, StackOverflow, etc.
//   Feel free to quiz me about what each aspect of the code does. 
//   All code involves tradeoffs..... I'm not married to a coding style except that it be neat and readable. 
//
//  
// 
//  Roger D. Pease  2020 -- rogerpease@gmail.com
//


#include <boost/property_tree/ptree.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <iostream>
#include <boost/foreach.hpp>
#include <boost/assert.hpp> 
#include <string> 

using namespace std; // So I don't need to use std:: in front of everything 


//
// Different groups have different opinions about how to do debug messages. 
// Some like arguments passed in, some like globals.  
// For embedded systems I use htis method so I can log to multiple places. 
// You can also choose a message depth (i.e. do I want to see the major transaction points or microdetails?). 
// The cost is that you're making more unnecessary function calls-- but machine time is cheap compared to 
// human time and you could always redefine the calls as a null macro.  
//

#ifdef DEBUG_LEVEL
void HandleDebugMessage(string id, string message, int level) 
{ 
  if (DEBUG_LEVEL >= level) { cout << "ID " << id << " " << message << endl; }

}
#else
#define HandleDebugMessage(x,y,z) 
#endif



// Simple result class. 

class NameAndSaying
{
     public: 
          string FullName; 
          string sentence; 
          bool valid; 
};


NameAndSaying ParseNameAndSayingJSONFile(string jsonFileName)
{  
  // 
  // Some languages will do this better with stack traces (perl, reflection languages,etc). 
  // I am using g++ which defines this macro. 
  // 

  string funcName = __FUNCTION__; 

  NameAndSaying result; 
  try {  
     boost::property_tree::ptree jsonFileParsed;
     boost::property_tree::read_json(jsonFileName.c_str(), jsonFileParsed);
     HandleDebugMessage(__FUNCTION__, "Parsed JSON File",1); 
 
     // This turns my file nto a property tree, which is an imperfect mapping 
     // but works for what I do. 
     string word1 = jsonFileParsed.get<string>("FirstName");
     string word2 = jsonFileParsed.get<string>("LastName");
     result.FullName =  word1 + " " + word2; 
     HandleDebugMessage(__FUNCTION__, result.FullName, 1);
     // Or to make it challenging, I want to iterate through all 
     std::vector<string> sentence; 
     BOOST_FOREACH (boost::property_tree::ptree::value_type & element, jsonFileParsed.get_child("Phrase"))
     { 
        sentence.push_back(element.second.get_value<string>()); 
     }
     result.sentence = boost::algorithm::join(sentence," "); 
     HandleDebugMessage(__FUNCTION__, result.sentence, 1);
     result.valid = true;
  } 
  catch (exception &e) 
  { 
     HandleDebugMessage(funcName, string ("Caught Exception ") + e.what(), 1);
     result.valid = false;
  } 

  return result; 

}

//
//  I always build my processes with test procedures, so I can run module level tests on my code. 
//
//
int TestProc()
{

	NameAndSaying result = ParseNameAndSayingJSONFile("MyJSONFile.json"); 
	BOOST_ASSERT(result.valid == 1); 
	BOOST_ASSERT(result.FullName == string("Roger Pease")); 
	BOOST_ASSERT(result.sentence == string("Hi There World")); 
	return 1; 

}

//
// Normally I don't put main in my library code but just to make things easy. 
//
int main(int argc, char *argv[]) 
{

        int result = TestProc(); 
	if (result == 1) { cout << "PASS" << endl; return 0;}
	return 1; 


}
