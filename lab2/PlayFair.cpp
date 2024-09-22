#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace::std;

class PlayfairCipher {
    private:
        char grid[5][5];
        string key;

    public:
        // Constructor
        PlayfairCipher(string key) : key(key) { 
            create_grid(key);
        }

        string encrypt(string &plain_text) {
            string text = plain_text;
            process_text(text); // To remove unwanted characters and repitions
            return encrypt_decrypt_digraphs(text);
        }

        string decrypt(string &cipher_text) {
            process_text(cipher_text); // Remove spaces
            return encrypt_decrypt_digraphs(cipher_text, false);
        }


    private:
        // Private functions
        void create_grid(string &key) {
            process_text(key);
            string grid_string = key + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; // Including 'J'
            grid_string = generate_grid_string(grid_string); // Removes duplicates in the string for correct order.

            // Fill the grid with the grid_string characters
            int str_index = 0;
            for (int i = 0; i < 5; i++) 
                for (int j = 0; j < 5; j++) 
                    grid[i][j] = grid_string[str_index++];

            view_grid();
        }

        string generate_grid_string(string &str) {
            string new_grid_string; // Result string to return
            vector<bool> seen(25, false); // Vector that keeps track of seen values

            for (char character : str) 
                if (!seen[character - 'A']) { // Gives us zero based indexing (A: 1, B:2 , ...)
                    if (character != 'J') new_grid_string += character; // Add current character to result string except 'J'
                    seen[character - 'A'] = true; // Set index of character as True (seen)
                }
            return new_grid_string; // New string with removed duplicates
        }

        void view_grid() {
            // Prints the grid matrix
            cout << endl;
            for (int i = 0; i < 5; i++) {
                for (int j = 0; j < 5; j++)
                    cout << "  " << grid[i][j]; 
                cout << endl;
            }
            cout << endl;
        }

        void process_text(string &text) {
            // remove_if() brings all the characters to be removed to the end of the string 
            // and returns an iterator to the start of those characters to be removed
            text.erase(remove_if(text.begin(), text.end(), is_not_alpha), text.end()); // Remove non alphabetic characters

            // replace all J with I in the entire string
            replace(text.begin(), text.end(), 'J', 'I');
            // Turn string to lower case
            transform(text.begin(), text.end(), text.begin(), ::toupper);

            // Fix repeating characters and odd lengths
            for (int i = 0; i < text.length() - 1; i+=2) {
                if (text[i] == text[i + 1]) { // Check if letter 1 equals letter 2 in the pair
                    text.insert(i+1, "X"); // insert X at the second letter
                }
            }
            // Fix odd length by placing X at the end
            if (text.length() % 2 != 0)
                text += 'X';
        }

        static bool is_not_alpha(char ch) {
            return !isalpha(ch); // Returns true if character is not an alphabet
        }

        string encrypt_decrypt_digraphs(string processed_plain_text, bool encrypt = true) {
            string result_text;
            result_text.clear();
            for (int i = 0; i < processed_plain_text.length() - 1; i+=2) {
                char letter_1 = processed_plain_text[i];
                char letter_2 = processed_plain_text[i + 1];

                // Get positions of the letter1 and letter2
                auto [row_1, col_1] = get_position(letter_1);
                auto [row_2, col_2] = get_position(letter_2);

                if (row_1 == row_2) { // If same row
                    result_text += grid[row_1][(col_1 + (encrypt? 1 : 4)) % 5]; // Add encrypted/decrypted letter 1
                    result_text += grid[row_1][(col_2 + (encrypt? 1 : 4)) % 5]; // Add encrypted/decrypted letter 2
                }
                else if (col_1 == col_2) { // If same column
                    result_text += grid[(row_1 + (encrypt? 1 : 4)) % 5][col_1]; // Add encrypted/decrypted letter 1
                    result_text += grid[(row_2 + (encrypt? 1 : 4)) % 5][col_1]; // Add encrypted/decrypted letter 2
                }
                else { // If neither same row or column
                    result_text += grid[row_1][col_2]; // Add encrypted/decrypted letter 1
                    result_text += grid[row_2][col_1]; // Add encrypted/decrypted letter 2
                }
                result_text += " ";
            }
            return result_text;
        }

        pair<int, int> get_position(char letter) {
            // iterate through the grid and find the position of the letter
            for (int i = 0; i < 5; i ++) 
                for (int j = 0; j < 5; j++) {
                    if (letter == grid[i][j])
                        return {i, j}; // Return row and column of the letter as pair
                }
            return {-1, -1}; // Just so that you dont get an error
        }
};

int main() {
    string key, plain_text, cipher_text;

    cout << "Enter your key: ";
    cin >> key;

    PlayfairCipher p1(key);

    cout << "Enter plain text: ";
    cin.ignore();
    getline(cin, plain_text);
    cipher_text = p1.encrypt(plain_text);

    cout << "Encrypted Text (Cipher Text): "  << endl << cipher_text << endl;
    cout << "Decrypted Text: " << endl << p1.decrypt(cipher_text) << endl;

    return 0;
}
