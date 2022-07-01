#include<fstream>

#define MAX_COLOR 255
#define MAX_LEN 1000000
#define MAX_COMPRESSED 150


#define INVALID_LEN 11
#define INPUT_TOO_LONG 10
#define INPUT_TOO_SHORT 9
#define WRONG_COLORS 8
#define TOO_MANY_LAYERS 7

using namespace std;
int main(int argc, char** argv) {
    auto fIn = ifstream(argv[1]);

    int len;
    fIn >> len;
    if(fIn.fail() || len < 1 || len > MAX_LEN) {
        return INVALID_LEN;
    }

    int tmp;
    int old = MAX_COLOR + 1;
    int compressedCount = 0;
    for(int i = 0; i < len; i++) {
        fIn >> tmp;
        if(fIn.fail()) {
            return INPUT_TOO_SHORT;
        } else if(tmp < 0 || tmp > MAX_COLOR) {
            return WRONG_COLORS;
        }
        if(tmp != old) {
            compressedCount++;
            old = tmp;
        }
    }

    fIn >> tmp;
    if(!fIn.fail()) {
        return INPUT_TOO_LONG;
    } else if (compressedCount > MAX_COMPRESSED) {
        return TOO_MANY_LAYERS;
    } else {
        return 0;
    }

}
