#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main() {
  string line;
  int n;
  while(true) {
    getline(cin, line);
    cerr << "# BOT> got line=" << line << endl;
    if(line.compare(0,18,"# WE HAVE FINISHED") == 0) {
      break;
    } else if(line.length() == 0 || line[0] == '#') {
      continue;
    } else {
      stringstream ss; 
      ss << line;  
      ss >> n;
      cout << n << " " << 0 << endl;
    }
  }
  return 0;
}
