#include <iostream>
#include <string>
#include <cctype>

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

int main() {
    string plaintext, key;

    // Input plaintext and key
    cout << "Enter the plaintext: ";
    getline(cin, plaintext);

    cout << "Enter the key: ";
    getline(cin, key);

    //// Encrypt the plaintext using the Vigenere cipher
    string ciphertext = Decrypt(plaintext, key);

    // Display the encrypted text
    cout << "Decrypted Text: " << ciphertext << endl;

    return 0;
}