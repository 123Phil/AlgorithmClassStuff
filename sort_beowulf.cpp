
#include <chrono>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

// Because for some reason C++ doesn't have case insensitive sorting...
bool str_less(string s1, string s2) {
	int i;
	for (i=0; i < s1.size() && i < s2.size(); i++) {
		if ((s1[i]|32) < (s2[i]|32)) {
			return true;
		} else if ((s1[i]|32) > (s2[i]|32)) {
			return false;
		}
	}
	if (s1.size() < s2.size()) {
		return true;
	}
	return false;
}


vector<string> readtext(char* filename, int num_lines) {
	vector<string> lines;
	string line;
	ifstream infile(filename);

	int i;
	for (i=0; i < num_lines; i++) {
		infile >> line;
		lines.push_back(line);
	}
	return lines;
}


void n2_sort(vector<string> &lines) {
	int i, j, best;
	int max = lines.size();

	for (i = 0; i < max-1; i++) {
		best = i;
		for (j = i+1; j < max; j++) {
			if (str_less(lines[j], lines[best])) {
				best = j;
			}
		}
		swap(lines[i], lines[best]);
	}
}


void print10(vector<string> lines) {
	int i;
	cout << "First 10 words:\n";
	for (i=0; i < 10; i++) {
		cout << "[" << lines[i] << "] ";
	}
	cout << endl;
}


int main(int argc, char** argv) {
	if (argc != 3)
		{
		std::cout << "Usage:  $ ./sort_beowulf beowulf.txt <num_lines>\n";
		return 0;
		}

	int num_lines = stoi(argv[2]);
	if (num_lines > 40707) num_lines = 40707;
	vector<string> lines = readtext(argv[1], num_lines);
	
	cout << "Requested n = " << num_lines << endl;
	print10(lines);
	cout << "Running C++ selection sort...\n";

	auto start = chrono::high_resolution_clock::now();
	n2_sort(lines);
	auto end = chrono::high_resolution_clock::now();

	print10(lines);

	int microseconds = chrono::duration_cast<chrono::microseconds>(end - start).count();
	double seconds = microseconds / 1E6;
	cout << "elapsed time: " << seconds << " seconds" << endl;

	return 0;
}
