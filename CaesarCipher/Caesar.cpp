#include <iostream>
#include <string>

using namespace::std;

string caesar_cipher(const string &message, int shift, bool encrypt);

int main (int argc, char *argv[]) {
    if (argc != 2 || string(argv[1]) != "encrypt" && string(argv[1]) != "decrypt") {
        cout << argv[1] << endl;
        cout << "Usage: " << argv[0] << " [encypt/decrypt]" << endl;
        return 1;
    }

    bool encrypt = string(argv[1]) == "encrypt";
    string message;
    int shift;

    cout << "Enter message: ";
    getline(cin, message);
    cout << "Enter shift (-1 for brute forcing): ";
    cin >> shift;

    if (shift == -1) {
        for (int i = 1; i < 26; i++) {
            cout << "Shift " << i << ": " << caesar_cipher(message, i, encrypt) << endl;
        }
    } else {
        cout << "Result: " << caesar_cipher(message, shift, encrypt) << endl;
    }
}

string caesar_cipher(const string &message, int shift, bool encrypt) {
    string result;
    int actual_shift = encrypt ? shift : 26 - shift;

    for (char c : message){
        if (isalpha(c)) {
            char base = islower(c) ? 'a' : 'A';
            result += 'A' + (c - base + actual_shift + 26) % 26;
        } else {
            result += c;
        }
    }
    return result;
}




