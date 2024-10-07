#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <vector>

using namespace std;

string Decrypt(const string& plaintext, const string& key) {
    string decipheredText;
    int keyLength = key.length();

    for (int i = 0, j = 0; i < plaintext.length(); ++i) {
        char currentChar = plaintext[i];

        if (islower(currentChar)) {
            char keyChar = tolower(key[j % keyLength]);
            char decryptedChar = 'a' + (currentChar - keyChar + 26) % 26;

            decipheredText += decryptedChar;
            ++j;
        }
        else {
            decipheredText += currentChar;
        }
    }

    return decipheredText;
}

bool HasRepeatedPrefix(const string& input) {
    // Extract the first 4 characters
    string prefix = input.substr(0, 4);

    // Check if the rest of the string contains the same prefix
    if (input.find(prefix, 4) != string::npos) {
        return true;
    }

    return false;
}

void exportToCSV(const string& filename, const vector<string>& row) {
    ofstream csvFile(filename, ios::app); // Open file in append mode

    if (csvFile.is_open()) {
        for (auto it = row.begin(); it != row.end(); ++it) {
            csvFile << '"';
            csvFile << *it;
            csvFile << '"';
            if (next(it) != row.end()) {
                csvFile << ","; // Add a comma between values
            }
        }
        csvFile << "\n"; // Start a new line for each row

        csvFile.close();
        cout << "Data appended to " << filename << " successfully.\n";
    } else {
        cerr << "Error: Unable to open file " << filename << " for writing.\n";
    }
}

void GenerateKeysFromFile(const string& filename) {

    string currentKey;

	// Open the file
    ifstream file(filename);

    // Check if the file is open
    if (!file.is_open()) {
        cerr << "Unable to open file: " << filename << endl;
        return;
    }

    // Read and process each line
    string line;
    while (getline(file, line)) {
        // Do something with the line
        // For example, you can print each line
        cout << "Processing line: " << line << endl;

        currentKey = Decrypt("vgjimlcfxcnzwg", line);

        if (HasRepeatedPrefix(currentKey))
        {
	        vector<string> dataRow = {line, currentKey};
            exportToCSV("keyOutput.csv", dataRow);
        }

        // You can also perform any other operation on the line here
        // ...

        // If you want to break the loop under certain conditions, you can use a condition
        // For example, break the loop if the line contains a specific keyword
        if (line.find("stop_processing") != string::npos) {
            cout << "Found stop_processing keyword. Stopping processing." << endl;
            break;
        }
    }

    // Close the file
    file.close();
}

int main() {

    vector<string> header = {"Word", "Key"};
    exportToCSV("keyOutput.csv", header);
    GenerateKeysFromFile("14charlist.txt");

    return 0;
}