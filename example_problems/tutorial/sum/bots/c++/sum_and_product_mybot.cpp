#include <iostream>
#include <string>
#include <sstream>
#include <math.h>

using namespace std;

int main() {
  string line;
  int s, p, x1, x2;
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
      ss >> s >> p;
      int delta = (int) sqrt(s*s-4*p);
      x1 = (s - delta)/2;
      x2 = s - x1;
      cout << x1 << " " << x2 << endl;
    }
  }
  return 0;
}
