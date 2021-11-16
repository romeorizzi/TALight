#include <iostream>
#include <fstream>
#include <vector>
using namespace std;


long int N;


long int best_path(vector<long int> triangle) {
	long int dist = N;
	long int i = 0;
	long int count = 1;
	//reverse(triangle.begin(), triangle.end());
	vector <long int> triangle_reverse;
	while (!triangle.empty()) {
		triangle_reverse.push_back(triangle.back());
		triangle.pop_back();
	}

	while (dist > 1) {
		triangle_reverse.at(i + dist) = max(triangle_reverse.at(i) + triangle_reverse.at(i + dist), triangle_reverse.at(i + 1) + triangle_reverse.at(i + dist));

		count++;
		i++;
		if (count == dist) {
			count = 1;
			dist--;
			i++;
		}
	}
	return triangle_reverse.at(i);
}


int main() {
	ifstream fin("input.txt");
	ofstream fout("output.txt");
	vector <long int> triangle;

	//acquisizione input
	fin >> N;
	for (long int i = 1; i <= N * (N + 1) / 2; i++) {
		long int num;
		fin >> num;
		triangle.push_back(num);
	}
	fout << best_path(triangle) << endl;

	return 0;
}