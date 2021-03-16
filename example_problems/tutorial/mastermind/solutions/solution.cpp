int nColors;
int blackScore(int c1, int c2, int c3, int c4);
int whiteScore(int c1, int c2, int c3, int c4);
void impossible();

const int MAX_NUM_ATTEMPTS = 12;
int enquiry[MAX_NUM_ATTEMPTS][4]; //each enquiry: 4 colored pegs
int answer[MAX_NUM_ATTEMPTS][2]; //each answ: (num black, num white)

int my_min(int a, int b) { return (a<b) ? a : b; }

void my_evaluate(int code[4], int guess[4], int my_answer[2]) {
  int occurs_in_code[nColors] = {0, 0, 0, 0, 0, 0};
  int occurs_in_guess[nColors] = {0, 0, 0, 0, 0, 0};
  for(int i = 0; i<4; i++)
    if(code[i]==guess[i])
      my_answer[0]++; // add a black peg in the answer
    else {
      occurs_in_code[code[i]]++;
      occurs_in_guess[guess[i]]++;
    }  
  for(int i = 0; i<nColors; i++)
    my_answer[1] += my_min(occurs_in_code[i], occurs_in_guess[i]);
}

bool compatible_with_feedback(int code[4], int guess[4], int answer[2]) {
  int my_answer[2] = {0, 0};
  my_evaluate(code, guess, my_answer);
  if(my_answer[0] != answer[0]) return false;
  if(my_answer[1] != answer[1]) return false;
  return true;
}  

bool compatible_with_history(int c[4], int history_last) {
  for(int i = 0; i<=history_last; i++)  {
    int submitted_code[4], received_answ[2];
    for(int j = 0; j<4; j++)
      submitted_code[j] = enquiry[i][j];
    for(int j = 0; j<2; j++)
      received_answ[j] = answer[i][j];
    if(!compatible_with_feedback(c,submitted_code,received_answ))
      return false;
  }  
  return true;
}  
  
void next(int c[4]) {
  if(++c[3] == nColors) {
    c[3] = 0;
    if(++c[2] == nColors) {
      c[2]=0;
      if(++c[1] == nColors) {
	c[1]=0;
	++c[0];
      }
    }
  }  
}

void play() {
  int c[4] = {0, 0, 0, 0};
  for(int attempt = 0; attempt < MAX_NUM_ATTEMPTS; attempt++) {
    for(int i = 0; i<4; i++)
      enquiry[attempt][i] = c[i];
    answer[attempt][0] = blackScore(c[0], c[1], c[2], c[3]);
    answer[attempt][1] = whiteScore(c[0], c[1], c[2], c[3]);
    do {
      if((c[0]==nColors-1) && (c[1]==nColors-1) && (c[2]==nColors-1) && (c[3]==nColors-1) )
	impossible();	
      next(c);
    } while(!compatible_with_history(c, attempt));	
  }
}
