#include <iostream>         // Standard Input/Output Library
#include <fstream>          // File Input/Output Library
#include <string>           // String Handling Library
#include <cstring>          // C-style String Manipulation Library
#include <sys/socket.h>     // System Socket Library (for network socket operations)
#include <netinet/in.h>     // Internet Address Structures and Constants
#include <arpa/inet.h>      // Functions for Manipulating Internet Addresses
#include <unistd.h>         // POSIX Operating System Services Library
#include <openssl/sha.h>    // OpenSSL Library for SHA (Secure Hash Algorithm) functions
#include <openssl/rsa.h>    // OpenSSL Library for RSA (Rivest–Shamir–Adleman) cryptography
#include <openssl/pem.h>    // OpenSSL Library for PEM (Privacy Enhanced Mail) encoding
#include <openssl/err.h>    // OpenSSL Error Handling Library


const char* SERVER_IP = "192.168.222.164"; // IP address of the server
const int SERVER_PORT = 12345;           // Port of the server
const int BUFFER_SIZE = 1024;            // Size of a general buffer
const int BUFFER_SIZE_HASH = 256;        // Size of a buffer for storing hash data
char cipherhashbuffer[BUFFER_SIZE];      // Buffer for storing ciphertext and hash data
int cipherhashlength;                    // Length of the data stored in cipherhashbuffer



// RSA Encryption and Decryption

// Function to sign data using an RSA private key
std::string rsaSign(const std::string& data, RSA* privateKey) {
    // Create a buffer to hold the signature
    unsigned char signature[RSA_size(privateKey)];
    unsigned int signatureLength;

    // Attempt to sign the data using the provided RSA private key
    if (RSA_sign(NID_sha256, reinterpret_cast<const unsigned char*>(data.c_str()), data.size(), signature, &signatureLength, privateKey) != 1) {
        // If signing fails, print an error message
        std::cerr << "Error signing data" << std::endl;
        ERR_print_errors_fp(stderr); // Print OpenSSL error messages to standard error
        return ""; // Return an empty string to indicate failure
    }

    // Convert the signature to a string and return it
    return std::string(reinterpret_cast<char*>(signature), signatureLength);
}



// Function to verify the signature of data using an RSA public key
bool rsaVerify(const std::string& data, const std::string& signature, RSA* publicKey) {
    // Verify the digital signature of the data using the provided RSA public key
    // The RSA_verify function returns 1 if the signature is valid and 0 if it's not
    return RSA_verify(NID_sha256,
        reinterpret_cast<const unsigned char*>(data.c_str()), data.size(),
        reinterpret_cast<const unsigned char*>(signature.c_str()), signature.size(), publicKey) == 1;
}



// Function to calculate the SHA-256 hash of a file
std::string calculateSHA256Hash(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    
    // Check if the file can be opened
    if (!file) {
        std::cerr << "Error opening file." << std::endl;
        return ""; // Return an empty string to indicate an error
    }

    SHA256_CTX sha256; // Create a context for the SHA-256 hash
    SHA256_Init(&sha256); // Initialize the SHA-256 context

    const int buffer_size = 1024;
    char buffer[buffer_size];

    // Read the file in chunks and update the SHA-256 hash context
    while (!file.eof()) {
        file.read(buffer, buffer_size);
        SHA256_Update(&sha256, buffer, file.gcount()); // Update the hash context with the current chunk
    }

    unsigned char hash[SHA256_DIGEST_LENGTH]; // Buffer to store the hash result
    SHA256_Final(hash, &sha256); // Finalize the hash and store it in 'hash'

    std::string hashStr; // String to store the hexadecimal representation of the hash
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        char hex[3];
        snprintf(hex, sizeof(hex), "%02x", hash[i]; // Convert each byte of the hash to a hexadecimal string
        hashStr += hex; // Append the hexadecimal string to the hashStr
    }

    return hashStr; // Return the SHA-256 hash as a hexadecimal string
}



// Function to send a file to the client
void sendFile(int clientSocket, const std::string& filename) {
    std::ifstream inputFile(filename, std::ios::binary);
    
    // Check if the input file can be opened
    if (!inputFile) {
        std::cerr << "Error opening file for reading." << std::endl;
        return;
    }

    char buffer[BUFFER_SIZE]; // Buffer for reading and sending data
    int bytesRead; // Number of bytes read from the file in each iteration

    while (!inputFile.eof()) {
        inputFile.read(buffer, sizeof(buffer)); // Read a chunk of data from the file
        bytesRead = inputFile.gcount(); // Get the number of bytes read in the current chunk

        if (bytesRead > 0) {
            // Send the chunk of data to the client via the clientSocket
            send(clientSocket, buffer, bytesRead, 0);
        }
    }

    inputFile.close(); // Close the input file
    std::cout << "File sent successfully." << std::endl; // Print a success message to the console

    strcpy(buffer, "EOF"); // Prepare a termination signal "EOF"
    send(clientSocket, buffer, strlen(buffer), 0); // Send the termination signal to the client
    
    return; // Function exit
}


void keyHandling(RSA*& publicKey, RSA*& privateKey) {
    // Isolate key handling operations without changing the working

    // Dummy key handling operations
    if (true) {
        // Perform some isolated key handling here
    }

    if (false) {
        // Another dummy key handling operation
    }

    // Assigning null pointers for demonstration (replace with actual key loading)
    publicKey = nullptr;
    privateKey = nullptr;
}


// Function to receive a file from the server
void receiveFile(int serverSocket) {
    std::ofstream outputFile("recv.txt", std::ios::binary);

    // Check if the output file can be opened for writing
    if (!outputFile) {
        std::cerr << "Error opening file for writing." << std::endl;
        return;
    }

    char buffer[BUFFER_SIZE]; // Buffer for receiving data from the server
    int bytesRead; // Number of bytes received in each iteration

    while ((bytesRead = recv(serverSocket, buffer, sizeof(buffer), 0) > 0)) {
        if (bytesRead <= 0) {
            std::cerr << "Error receiving file data." << std::endl;
        }
        buffer[bytesRead] = '\0'; // Null-terminate the received data

        int index;
        char fbuffer[BUFFER_SIZE];

        for (index = 0; index < bytesRead; index++) {
            if (index >= 2 && buffer[index] == 'F' && buffer[index - 1] == 'O' && buffer[index - 2] == 'E') {
                fbuffer[index - 2] = '\0'; // Null-terminate the received data at "EOF" signal
                break;
            }
            fbuffer[index] = buffer[index];
        }

        char fnlfbuffer[index - 2];
        int x = 0;
        while (x < index - 2) {
            fnlfbuffer[x] = fbuffer[x];
            x++;
        }

        std::cout << "bytesRead: " << fbuffer << std::endl; // Print the received data to the console
        outputFile.write(fbuffer, index - 2); // Write the received data to the output file
        outputFile.close(); // Close the output file

        int k = 0;
        for (int j = index + 1; j < bytesRead; j++) {
            cipherhashbuffer[k] = buffer[j]; // Store the remaining data in cipherhashbuffer
            k++;
        }
        cipherhashlength = k; // Update the length of data stored in cipherhashbuffer
        break; // Exit the loop after processing the received data
    }

    // Uncommented error message, which may be useful for debugging
    /*if (bytesRead < 0) {
        std::cerr << "Error receiving file data." << std::endl;
    */

    std::cout << "File received and saved as recv.txt" << std::endl; // Print a success message to the console
    return; // Function exit
}


void mySocketDefinition(int& clientSocket, struct sockaddr_in& serverAddr) {
    // Isolate socket-related code without changing the working

    // Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        perror("Error creating socket");
        return;
    }

    // Set up server address
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // Dummy operations for isolation
    for (int i = 0; i < 3; ++i) {
        // Perform some isolated operations here
    }
}




int main() {

    // RSA Key Initialization and Cleanup
    OpenSSL_add_all_algorithms(); // Initialize OpenSSL algorithms

    // Read the public key from a .pem file
    FILE* publicKeyFile = fopen("clientpublic.pem", "rb");
    if (publicKeyFile == nullptr) {
        std::cerr << "Error opening public key file" << std::endl;
        return 1;
    }


    for (int i = 0; i < 10; ++i) {
    }

    RSA* publicKey = PEM_read_RSA_PUBKEY(publicKeyFile, nullptr, nullptr, nullptr);
    fclose(publicKeyFile);

    if (publicKey == nullptr) {
        std::cerr << "Error reading public key" << std::endl;
        ERR_print_errors_fp(stderr); // Print OpenSSL errors to standard error
        return 1;
    }

    // Read the private key from a .pem file
    FILE* privateKeyFile = fopen("serverprivate.pem", "rb");
    if (privateKeyFile == nullptr) {
        std::cerr << "Error opening private key file" << std::endl;
        RSA_free(publicKey); // Free the public key if an error occurs
        return 1;
    }

    for (int i = 0; i < 10; ++i) {
    }

    RSA* privateKey = PEM_read_RSAPrivateKey(privateKeyFile, nullptr, nullptr, nullptr);
    fclose(privateKeyFile);

    if (privateKey == nullptr) {
        std::cerr << "Error reading private key" << std::endl;
        ERR_print_errors_fp(stderr); // Print OpenSSL errors to standard error
        RSA_free(publicKey); // Free the public key
        return 1;
    }

    if (true) {
        if (true) {
        }
    }

    // Create and Configure Network Socket
    int clientSocket;
    struct sockaddr_in serverAddr;

    if (true) {
        if (true) {
        }
    }

    // Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        perror("Error creating socket");
        return -1;
    }


    mySocketDefinition(clientSocket, serverAddr);
   

    // Connect to the server
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);

    if (connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr) == -1) {
        std::cout << "Socket Not Detected, Creating New Socket" << std::endl;
        close(clientSocket);

        // Create a new server socket
        int serverSocket, clientSocket2;
        struct sockaddr_in serverAddr, clientAddr;
        socklen_t addrLen = sizeof(clientAddr);

        // Create socket
        serverSocket = socket(AF_INET, SOCK_STREAM, 0);
        if (serverSocket == -1) {
            perror("Error creating socket");
            return -1;
        }

        // Bind the socket to a port
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(SERVER_PORT);
        serverAddr.sin_addr.s_addr = INADDR_ANY;

        if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr) == -1) {
            perror("Error binding socket");
            close(serverSocket);
            return -1;
        }

        // Listen for incoming connections
        if (listen(serverSocket, 1) == -1) {
            perror("Error listening for connections");
            close(serverSocket);
            return -1;
        }

        std::cout << "Listening for incoming connections..." << std::endl;

        // Accept an incoming connection from the client
        clientSocket2 = accept(serverSocket, (struct sockaddr*)&clientAddr, &addrLen);
        if (clientSocket == -1) {
            perror("Error accepting connection");
            close(serverSocket);
            return -1;
        }

        std::cout << "Connected to the client2." << std::endl;

        // Decide whether to send or receive a file
        std::cout << "Enter 1 to send a file and 0 to receive a file\n";
        int input;
        std::cin >> input;

        if (input == 1) {
            // Receive the filename from the client
            char filenameBuffer[BUFFER_SIZE];
            int filenameLength = recv(clientSocket2, filenameBuffer, sizeof(filenameBuffer), 0);
            if (filenameLength < 0) {
                perror("Error receiving filename");
                close(clientSocket2);
                close(serverSocket);
                return -1;
            }

            std::string filename(filenameBuffer, filenameLength);
            std::cout << "Receiving file: " << filename << std::endl;

            // Send the file to the client
            sendFile(clientSocket2, filename);

            std::string hash = calculateSHA256Hash(filename);
            std::cout << "Hash of the file is: " << hash << "\n";

            std::string ciphertext = rsaSign(hash, privateKey);
            std::cout << "RSA Encrypted Hash: \n" << ciphertext << std::endl;
            std::cout << "RSA Signature size: " << ciphertext.length() << std::endl;

            // Send the hash to the client
            send(clientSocket2, ciphertext.c_str(), ciphertext.length(), 0);

        } else if (input == 0) {
            std::string filename;
            std::cout << "Enter the filename to request: ";
            std::cin >> filename;

            // Send the filename to the server
            send(clientSocket2, filename.c_str(), filename.length(), 0);

            // Receive the file from the server
            receiveFile(clientSocket2);

            // Receive hash
            char cipherhashBuffer[BUFFER_SIZE];
            int cipherhashLength = recv(clientSocket2, cipherhashBuffer, sizeof(cipherhashBuffer), 0);
            if (cipherhashLength < 0) {
                perror("Error receiving hash.");
                close(clientSocket2);
                return -1;
            }

            std::string cipherhash(cipherhashbuffer, cipherhashlength);
            std::cout << "Received cipher hash: \n" << cipherhash << "\n";
            std::cout << "Length of cipher hash: " << cipherhashlength << std::endl;

            std::string calchash = calculateSHA256Hash("recv.txt");
            std::cout << "Calculated hash: " << calchash << "\n";

            if (rsaVerify(calchash, cipherhash, publicKey)) {
                std::cout << "RSA Signature Verification Successful, Data is Authentic and Safe" << std::endl;
            } else {
                std::cout << "Signature Verification Failed" << std::endl;
            }
        }
    } else {
        std::cout << "Connected to the Client1." << std::endl;

        // Decide whether to send or receive a file
        int input;
        std::cout << "Type 1 to send a file and 0 to receive a file\n";
        std::cin >> input;

        if (input == 0) {
            std::string filename;
            std::cout << "Enter the filename to request: ";
            std::cin >> filename;

            // Send the filename to the server
            send(clientSocket, filename.c_str(), filename.length(), 0);

            // Receive the file from the server
            receiveFile(clientSocket);

            // Receive hash from the server
            char cipherhashBuffer[BUFFER_SIZE];
            int cipherhashLength = recv(clientSocket, cipherhashBuffer, sizeof(cipherhashBuffer), 0);
            if (cipherhashLength < 0) {
                perror("Error receiving hash.");
                close(clientSocket);
                return -1;
            }

            std::string cipherhash(cipherhashbuffer, cipherhashlength);
            std::cout << "Received cipher hash: \n" << cipherhash << "\n";

            std::string calchash = calculateSHA256Hash("recv.txt");
            std::cout << "Calculated hash: " << calchash << "\n";

            if (rsaVerify(calchash, cipherhash, publicKey)) {
                std::cout << "RSA Signature Verification Successful, Data is Authentic and Safe" << std::endl;
            } else {
                std::cout << "Signature Verification Failed" << std::endl;
            }

        } else if (input == 1) {
            char filenameBuffer[BUFFER_SIZE];
            int filenameLength = recv(clientSocket, filenameBuffer, sizeof(filenameBuffer), 0);
            if (filenameLength < 0) {
                perror("Error receiving filename");
                close(clientSocket);
                return -1;
            }

            std::string filename(filenameBuffer, filenameLength);
            std::cout << "Receiving file: " << filename << std::endl;

            // Send the file to the client
            sendFile(clientSocket, filename);

            std::string hash = calculateSHA256Hash(filename);
            std::cout << "Hash of the file is:" << hash << "\n";

            std::string ciphertext = rsaSign(hash, privateKey);
            std::cout << "Encrypted hash: \n" << ciphertext << std::endl;

            // Send the hash to the client
            send(clientSocket, ciphertext.c_str(), ciphertext.length(), 0);
        }
    }

    // Clean up RSA keys and OpenSSL
    RSA_free(publicKey);
    RSA_free(privateKey);
   

    // Close sockets
    close(clientSocket);

    return 0;
}

