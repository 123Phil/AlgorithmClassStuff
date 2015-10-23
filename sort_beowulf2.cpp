
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


void n2_sort(vector<string> &lines, int max) {
	int i, j, best;

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
	for (i=0; i < 10; i++) {
		cout << "[" << lines[i] << "] ";
	}
	cout << endl;
}


int main(int argc, char** argv) {
	ofstream outfile("cpp_data.txt");

	vector<string> lines = readtext(argv[1], 5001);
	vector<string> lines2;
	
	chrono::high_resolution_clock::time_point start;
	chrono::high_resolution_clock::time_point end;

	int microseconds;
	double seconds;

	int size, loops;
	for (size = 100; size < 5001; size += 100) {
		
		seconds = 0.0;
		for (loops = 0; loops < 5; loops++) {
			lines2 = lines;
			start = chrono::high_resolution_clock::now();
			n2_sort(lines2, size);
			end = chrono::high_resolution_clock::now();

			microseconds = chrono::duration_cast<chrono::microseconds>(end - start).count();
			seconds += microseconds / 1E6;
		}

		seconds /= 5.0;
		outfile << fixed << size << " " << seconds << endl;
	}

	outfile.close();
	return 0;
}
