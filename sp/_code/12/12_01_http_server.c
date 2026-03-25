#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080
#define BUFFER_SIZE 4096

void parse_http_request(const char* buffer) {
    printf("\n=== Parsing HTTP Request ===\n");
    
    char method[16], path[256], version[32];
    sscanf(buffer, "%s %s %s", method, path, version);
    
    printf("Method: %s\n", method);
    printf("Path: %s\n", path);
    printf("Version: %s\n", version);
}

const char* get_mime_type(const char* path) {
    if (strstr(path, ".html")) return "text/html";
    if (strstr(path, ".css")) return "text/css";
    if (strstr(path, ".js")) return "application/javascript";
    if (strstr(path, ".json")) return "application/json";
    if (strstr(path, ".png")) return "image/png";
    if (strstr(path, ".jpg") || strstr(path, ".jpeg")) return "image/jpeg";
    return "text/plain";
}

void build_http_response(char* response, const char* status, const char* content_type, const char* body) {
    sprintf(response, 
        "HTTP/1.1 %s\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %lu\r\n"
        "Server: SimpleHTTP/1.0\r\n"
        "\r\n"
        "%s",
        status, content_type, strlen(body), body);
}

int main() {
    printf("=== Simple HTTP Server Demo ===\n\n");
    
    printf("Server configuration:\n");
    printf("  Port: %d\n", PORT);
    printf("  Buffer size: %d bytes\n", BUFFER_SIZE);
    
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket creation failed");
        return 1;
    }
    printf("\nSocket created successfully\n");
    
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        close(server_fd);
        return 1;
    }
    printf("Bind successful\n");
    
    if (listen(server_fd, 128) < 0) {
        perror("listen failed");
        close(server_fd);
        return 1;
    }
    printf("Server listening on port %d\n", PORT);
    
    printf("\n=== HTTP Request/Response Cycle ===\n");
    printf("Request:\n");
    printf("  GET /index.html HTTP/1.1\n");
    printf("  Host: localhost\n");
    printf("  User-Agent: DemoClient/1.0\n");
    printf("  Accept: */*\n");
    
    printf("\nResponse:\n");
    char response[BUFFER_SIZE];
    const char* body = "<html><body><h1>Hello, Web!</h1></body></html>";
    build_http_response(response, "200 OK", "text/html", body);
    printf("%s\n", response);
    
    printf("\n=== MIME Type Detection ===\n");
    const char* paths[] = {"/index.html", "/style.css", "/app.js", "/data.json", "/image.png"};
    for (int i = 0; i < 5; i++) {
        printf("  %s -> %s\n", paths[i], get_mime_type(paths[i]));
    }
    
    printf("\n(Note: This is a simulation - actual server would block on accept)\n");
    
    close(server_fd);
    return 0;
}
