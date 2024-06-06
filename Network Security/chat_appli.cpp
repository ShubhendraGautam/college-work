#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080

std::string encryptDecrypt(std::string toEncrypt, int key) {
    std::string output = toEncrypt;
    for (int i = 0; i < toEncrypt.size(); i++)
        output[i] = toEncrypt[i] ^ key;
    return output;
}

long long modPow(long long base, long long power, long long mod) {
    long long result = 1;
    base = base % mod;
    while (power > 0) {
        if (power & 1)
            result = (result * base) % mod;
        power = power >> 1;
        base = (base * base) % mod;
    }
    return result;
}

void actAsClient1() {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "Socket creation error" << std::endl;
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address/ Address not supported" << std::endl;
        return;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Connection Failed" << std::endl;
        return;
    }

    // Send communication request
    send(sock, "Communication Request", 21, 0);

    // Receive encryption method
    read(sock, buffer, 1024);
    std::cout << "Received encryption method: " << buffer << std::endl;

    // Diffie-Hellman
    long long p = 23;
    long long g = 5;
    long long a = rand() % p;
    long long A = modPow(g, a, p);
    send(sock, &A, sizeof(A), 0);  // Send A

    long long B;
    read(sock, &B, sizeof(B));  // Receive B
    long long sharedSecret = modPow(B, a, p);
    std::cout << "Shared secret established: " << sharedSecret << std::endl;

    // Chat loop
    while (true) {
        std::string message;
        std::cout << "You: ";
        std::getline(std::cin, message);
        std::string encrypted = encryptDecrypt(message, sharedSecret);
        send(sock, encrypted.c_str(), encrypted.length(), 0);

        memset(buffer, 0, sizeof(buffer));
        read(sock, buffer, 1024);
        std::cout << "client2: " << encryptDecrypt(buffer, sharedSecret) << std::endl;
    }

    close(sock);
}

void actAsClient2() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return;
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        std::cerr << "Setsockopt error" << std::endl;
        return;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        std::cerr << "Bind failed" << std::endl;
        return;
    }

    if (listen(server_fd, 3) < 0) {
        std::cerr << "Listen error" << std::endl;
        return;
    }

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        std::cerr << "Accept error" << std::endl;
        return;
    }

    // Receive communication request
    read(new_socket, buffer, 1024);
    std::cout << "Received: " << buffer << std::endl;

    // Send encryption method
    send(new_socket, "XOR", 3, 0);

    // Diffie-Hellman
    long long p = 23;
    long long g = 5;
    long long b = rand() % p;
    long long B = modPow(g, b, p);
    send(new_socket, &B, sizeof(B), 0);  // Send B

    long long A;
    read(new_socket, &A, sizeof(A));  // Receive A
    long long sharedSecret = modPow(A, b, p);
    std::cout << "Shared secret established: " << sharedSecret << std::endl;

    // Chat loop
    while (true) {
        memset(buffer, 0, sizeof(buffer));
        read(new_socket, buffer, 1024);
        std::cout << "client1: " << encryptDecrypt(buffer, sharedSecret) << std::endl;

        std::string message;
        std::cout << "You: ";
        std::getline(std::cin, message);
        std::string encrypted = encryptDecrypt(message, sharedSecret);
        send(new_socket, encrypted.c_str(), encrypted.length(), 0);
    }

    close(new_socket);
    close(server_fd);
}

int main() {
    std::cout << "Act as (1) client1 or (2) client2? ";
    int choice;
    std::cin >> choice;
    std::cin.ignore();

    if (choice == 1) {
        actAsClient1();
    } else if (choice == 2) {
        actAsClient2();
    } else {
        std::cerr << "Invalid choice." << std::endl;
    }

    return 0;
}
