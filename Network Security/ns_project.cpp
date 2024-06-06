// DecentralizedSecureClient.cpp

#include <iostream>
#include <fstream>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <thread>
#include <dirent.h>
#include <map>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/sha.h>
#include <openssl/err.h>

const int CLIENT_PORTS[] = {8082, 8083, 8084, 8085, 8086}; 
const int CURRENT_CLIENT_PORT = 8082; 
const std::string CURRENT_CLIENT_DIR = "Client1"; 
const std::string PRIVATE_KEY_PATH = CURRENT_CLIENT_DIR + "/private/private_key.pem";
const std::string PUBLIC_KEY_PATH = CURRENT_CLIENT_DIR + "/public/public_key.pem";

std::map<int, std::string> clientAddresses = {
    {8082, "127.0.0.1"},
    {8083, "127.0.0.1"},
    {8084, "127.0.0.1"},
    {8085, "127.0.0.1"},
    {8086, "127.0.0.1"}
};

// Crypto Utilities

std::string hashFile(const std::string& filename) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    std::ifstream file(filename, std::ios::binary);
    if (file.is_open()) {
        char buffer[4096];
        int bytesRead;
        while (file.read(buffer, sizeof(buffer))) {
            SHA256_Update(&sha256, buffer, file.gcount());
        }
        SHA256_Final(hash, &sha256);
    }
    file.close();
    return std::string((char*)hash, SHA256_DIGEST_LENGTH);
}

std::vector<unsigned char> signData(const std::string& privateKeyPath, const std::string& data) {
    std::vector<unsigned char> signature(RSA_size(loadPrivateKey(privateKeyPath)));
    unsigned int signatureLength;

    RSA_sign(NID_sha256, (unsigned char*)data.c_str(), data.size(), signature.data(), &signatureLength, loadPrivateKey(privateKeyPath));

    return signature;
}

bool verifySignature(const std::string& publicKeyPath, const std::string& data, const std::vector<unsigned char>& signature) {
    return RSA_verify(NID_sha256, (unsigned char*)data.c_str(), data.size(), signature.data(), signature.size(), loadPublicKey(publicKeyPath));
}

RSA* loadPrivateKey(const std::string& path) {
    FILE* keyfile = fopen(path.c_str(), "r");
    RSA* rsa = PEM_read_RSAPrivateKey(keyfile, NULL, NULL, NULL);
    fclose(keyfile);
    return rsa;
}

RSA* loadPublicKey(const std::string& path) {
    FILE* keyfile = fopen(path.c_str(), "r");
    RSA* rsa = PEM_read_RSA_PUBKEY(keyfile, NULL, NULL, NULL);
    fclose(keyfile);
    return rsa;
}

// Client Functions

std::vector<std::string> listFiles() {
    std::vector<std::string> files;
    std::string path = CURRENT_CLIENT_DIR + "/shared";
    DIR* dir = opendir(path.c_str());
    if (dir) {
        struct dirent* entry;
        while ((entry = readdir(dir))) {
            if (entry->d_type == DT_REG) {
                files.push_back(entry->d_name);
            }
        }
        closedir(dir);
    }
    return files;
}

void handleClient(int clientSocket) {
    char buffer[4096];
    int bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0);
    if (bytesRead > 0) {
        std::string command(buffer, bytesRead);
        if (command == "LIST") {
            auto files = listFiles();
            std::string fileList;
            for (const auto& file : files) {
                fileList += file + "\n";
            }
            send(clientSocket, fileList.c_str(), fileList.size(), 0);
        } else if (command.rfind("GET ", 0) == 0) {
            std::string filename = CURRENT_CLIENT_DIR + "/shared/" + command.substr(4);
            std::ifstream file(filename, std::ios::binary);

            if (!file.is_open()) {
                std::string errorMsg = "ERROR: File not found!";
                send(clientSocket, errorMsg.c_str(), errorMsg.size(), 0);
                return;
            }

            // Send the file first
            char fileBuffer[4096];
            while (file.read(fileBuffer, sizeof(fileBuffer))) {
                send(clientSocket, fileBuffer, file.gcount(), 0);
            }
            file.close();

            // Compute hash and then sign it
            std::string fileHash = hashFile(filename);
            std::vector<unsigned char> signature = signData(PRIVATE_KEY_PATH, fileHash);
            
            // Send the signature
            send(clientSocket, signature.data(), signature.size(), 0);
        }
    }
    close(clientSocket);
}

void listenForClients() {
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in clientAddr;
    clientAddr.sin_family = AF_INET;
    clientAddr.sin_port = htons(CURRENT_CLIENT_PORT);
    clientAddr.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (struct sockaddr*)&clientAddr, sizeof(clientAddr));
    listen(serverSocket, 5);

    while (true) {
        int clientSocket = accept(serverSocket, nullptr, nullptr);
        std::thread(handleClient, clientSocket).detach();
    }

    close(serverSocket);
}

void downloadFileFromClient(int port, const std::string& filename) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in targetAddr;
    targetAddr.sin_family = AF_INET;
    targetAddr.sin_port = htons(port);
    targetAddr.sin_addr.s_addr = inet_addr(clientAddresses[port].c_str());

    if (connect(sock, (struct sockaddr*)&targetAddr, sizeof(targetAddr)) < 0) {
        std::cout << "Unable to connect to client at port " << port << ". The client might be offline." << std::endl;
        close(sock);
        return;
    }

    // Request file
    std::string command = "GET " + filename;
    send(sock, command.c_str(), command.size(), 0);

    // Receive file
    std::ofstream outFile(CURRENT_CLIENT_DIR + "/shared/" + filename, std::ios::binary);
    char buffer[4096];
    int bytesRead;
    while ((bytesRead = recv(sock, buffer, sizeof(buffer), 0)) > 0) {
        outFile.write(buffer, bytesRead);
    }
    outFile.close();

    // Receive signature
    std::vector<unsigned char> receivedSignature(RSA_size(loadPublicKey(PUBLIC_KEY_PATH)));
    recv(sock, receivedSignature.data(), receivedSignature.size(), 0);

    // Verify signature
    std::string fileHash = hashFile(CURRENT_CLIENT_DIR + "/shared/" + filename);
    if (verifySignature(PUBLIC_KEY_PATH, fileHash, receivedSignature)) {
        std::cout << "Downloaded and verified file: " << filename << " from client " << port << std::endl;
    } else {
        std::cout << "Failed to verify file: " << filename << " from client " << port << std::endl;
    }

    close(sock);
}

int main() {
    std::thread(listenForClients).detach(); // Listen in a separate thread

    while (true) {
        std::cout << "Enter command (VIEW <port>, DOWNLOAD <port> <filename>, QUIT): ";
        std::string command;
        std::getline(std::cin, command);

        if (command == "QUIT") {
            break;
        } else if (command.rfind("VIEW ", 0) == 0) {
            int port = std::stoi(command.substr(5));
            viewFilesFromClient(port);
        } else if (command.rfind("DOWNLOAD ", 0) == 0) {
            int port = std::stoi(command.substr(9, 4));
            std::string filename = command.substr(14);
            downloadFileFromClient(port, filename);
        } else {
            std::cout << "Invalid command. Please try again." << std::endl;
        }
    }

    return 0;
}
