#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string inputFilePath = "allwords.txt";
    string outputFilePath = "14charlist.txt";

    // Open the input file
    ifstream inputFile(inputFilePath);
    if (!inputFile.is_open()) {
        cerr << "Error opening input file: " << inputFilePath << endl;
        return 1;
    }

    // Open the output file
    ofstream outputFile(outputFilePath);

    // put each 14-char word in the input file
    string word;
    while (inputFile >> word) {
        if (word.length() == 14) {
            outputFile << word << endl;
        }
    }

    // Close files
    inputFile.close();
    outputFile.close();

    return 0;
}
