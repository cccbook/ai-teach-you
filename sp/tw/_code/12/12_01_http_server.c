#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

typedef struct {
    char path[256];
    char (*handler)();
} Route;

typedef struct {
    int server_fd;
    char host[32];
    int port;
    Route routes[20];
    int route_count;
} HTTPServer;

void http_init(HTTPServer *srv, const char *host, int port) {
    srv->server_fd = 0;
    strncpy(srv->host, host, 31);
    srv->port = port;
    srv->route_count = 0;
}

int http_listen(HTTPServer *srv) {
    srv->server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (srv->server_fd < 0) return -1;
    
    int opt = 1;
    setsockopt(srv->server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(srv->port);
    
    if (bind(srv->server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) return -1;
    if (listen(srv->server_fd, 128) < 0) return -1;
    
    printf("Server listening on %s:%d\n", srv->host, srv->port);
    return 0;
}

void http_handle_request(HTTPServer *srv, int client_fd) {
    char buffer[4096] = {0};
    read(client_fd, buffer, sizeof(buffer) - 1);
    
    char method[16], path[256], version[16];
    sscanf(buffer, "%s %s %s", method, path, version);
    
    printf("%s %s %s\n", method, path, version);
    
    char response[] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, Web!</h1></body></html>";
    write(client_fd, response, strlen(response));
}

int main() {
    HTTPServer srv;
    http_init(&srv, "0.0.0.0", 8080);
    
    if (http_listen(&srv) < 0) {
        printf("Failed to start server\n");
        return 1;
    }
    
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(srv.server_fd, (struct sockaddr*)&client_addr, &client_len);
        
        if (client_fd >= 0) {
            http_handle_request(&srv, client_fd);
            close(client_fd);
        }
    }
    
    close(srv.server_fd);
    return 0;
}
