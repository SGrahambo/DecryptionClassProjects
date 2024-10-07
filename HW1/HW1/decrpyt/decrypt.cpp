#include <iostream>
#include <string>
#include <sstream>
#include <cctype>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

string Decrypt(const string& plaintext, const string& key) {
    string decipheredText;
    int keyLength = key.length();

    for (int i = 0, j = 0; i < plaintext.length(); ++i) {
        char currentChar = plaintext[i];

        if (islower(currentChar)) {
            char keyChar = tolower(key[j % keyLength]);
            char shift = 'a' - currentChar;
            char decryptedChar = 'a' - (shift + (keyChar - 'a')) % 26;

            decipheredText += decryptedChar;
            ++j;
        }
        else {
            decipheredText += currentChar;
        }
    }

    return decipheredText;
}

int WordCount(const string& decipheredText)
{
	istringstream iss(decipheredText);
    int count = 0;
	string word;

    while (iss >> word) {
        count++;
    }

    return count;
}

bool IsStringInWordList(const vector<string>& wordList, const string& target)
{
    if (binary_search(wordList.begin(), wordList.end(), target))
    {
	    return true;
    }
    else
    {
	    return false;
    }    
}

double Precision(const string& decipheredText, const vector<string>& wordList, const double& desiredPrecision, const int& wordCount)
{
    double precision = 0;
    int wordListMatchedCount = 0;

    istringstream iss(decipheredText);
    string word;

    while (iss >> word)
    {
	    if (IsStringInWordList(wordList, word))
	    {
		    wordListMatchedCount++;
	    }
        //precision = static_cast<double>(wordListMatchedCount) / wordCount;
    }

    return static_cast<double>(wordListMatchedCount) / wordCount;
}

vector<string> ImportFileToVector(string fileName)
{
	ifstream inputFile(fileName);
    vector<string> wordList;
    string line;
    while (getline(inputFile, line))
    {
	    wordList.push_back(line);
    }
    inputFile.close();

    return wordList;
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

string MinKey (int minLength)
{
    string key;
	for (int i = 0; i < minLength; i++)
	{
		key += 'a';
	}
    return key;
}

string MaxKey (int maxLength)
{
    string key;
	for (int i = 0; i < maxLength; i++)
	{
		key += 'z';
	}
    return key;
}

void IncrementKey (string& key)
{
	const int n = key.length();
    bool carry = true;

    for (int i = n - 1; i >= 0; i--) {
        if (carry == 0) {
            break;
        }

        if (key[i] == 'z') {
            key[i] = 'a';
        } else
        {
            key[i]++;
            carry = false;
        }
    }

    if (carry) {
        key = string(n + 1, 'a');
    }

    //return key;
}

int main() {

    double desiredPrecision = .8; // minimum % of words to match the wordlist before stopping the key search.
    const int minKeyLength = 8;
    const int maxKeyLength = 10;
    vector<string> wordList = ImportFileToVector("wordlist.txt");

    // Export header to CSV
    vector<string> header = {"Precision", "Key", "Message"};
    exportToCSV("output.csv", header);

    double precision = 0;
    string plaintext, prevKey, ciphertext;
    int wordCount = 0;
    bool verified = false;
    string minKey = MinKey(minKeyLength);
    string maxKey = MaxKey(maxKeyLength);
    string currentKey = minKey;
    

    // Input plaintext and key
    cout << "Enter the plaintext to decrypt: ";
    getline(cin, plaintext);
    wordCount = WordCount(plaintext);

    while (currentKey <= maxKey)
    {
        cout << "current key: " << currentKey << endl;
        ciphertext = Decrypt(plaintext, currentKey);
        precision = Precision(ciphertext, wordList, desiredPrecision,wordCount);
        if (precision >= desiredPrecision)
        {
         //   cout << "key: " << currentKey << endl;
	        //cout << "Decrypted Text: " << ciphertext << endl;
            vector<string> dataRow = {to_string(precision), currentKey, ciphertext};
            exportToCSV("output.csv", dataRow);
            verified = true;
        }
        IncrementKey(currentKey);
    }

    if (!verified)
    {
	    cout << "No matches above the desired precision." << endl;
    }

    return 0;
}