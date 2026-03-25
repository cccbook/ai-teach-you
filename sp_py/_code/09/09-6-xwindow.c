// X Window System 範例

#include <X11/Xlib.h>

int main() {
    Display *display = XOpenDisplay(NULL);
    Window window = XCreateSimpleWindow(
        display, DefaultRootWindow(display),
        100, 100, 400, 300,
        1, BlackPixel(display, 0), WhitePixel(display, 0)
    );
    
    XSelectInput(display, window, ExposureMask | KeyPressMask);
    XMapWindow(display, window);
    
    XEvent event;
    while (1) {
        XNextEvent(display, &event);
        if (event.type == Expose) {
            GC gc = DefaultGC(display, 0);
            XDrawString(display, window, gc, 50, 50, "Hello X!", 8);
        }
    }
    
    XCloseDisplay(display);
    return 0;
}

// Wayland 範例（較新）
/*
Wayland 協定：
- Compositor 負責合成
- 用戶端直接與 compositor 通訊
- 少了 X Server 這層
*/
