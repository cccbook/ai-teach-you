# Rust

## 概述

Rust 是一種系統程式設計語言，由 Graydon Hoare 於 2006 年發明， Mozilla 贊助開發。Rust 強調記憶體安全性和執行時效能，透過所有權（Ownership）系統在編譯時防止記憶體錯誤，無需垃圾回收器。Rust 連續多年被評為最受歡迎的程式語言。

## 歷史

- **2006 年**：Graydon Hoare 開始開發 Rust
- **2010 年**：Mozilla 正式贊助
- **2011 年**：Rust 首次發布
- **2015 年**：Rust 1.0 穩定版發布
- **2018 年**：Rust 2018 版
- **2021 年**：Rust 2021 版
- **現在**：Rust 1.75 為最新穩定版

## 核心特性

### 1. 所有權系統

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 的所有權移動到 s2
    
    // println!("{}", s1); // 錯誤：s1 已無效
    println!("{}", s2);   // 正確
    
    // 借用
    let s3 = String::from("world");
    let len = calculate_length(&s3);
    println!("{} 的長度是 {}", s3, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

### 2. 結構體與方法

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Rectangle { width, height }
    }
    
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect = Rectangle::new(30, 50);
    println!("面積: {}", rect.area());
}
```

### 3. 枚舉與模式匹配

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to {}, {}", x, y),
            Message::Write(text) => println!("Write: {}", text),
            Message::ChangeColor(r, g, b) => println!("Color: {}, {}, {}", r, g, b),
        }
    }
}

fn main() {
    let msg = Message::Move { x: 10, y: 20 };
    msg.call();
}
```

### 4. 錯誤處理

```rust
use std::fs::File;
use std::io::Read;

fn read_file_contents(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

fn main() {
    match read_file_contents("test.txt") {
        Ok(contents) => println!("{}", contents),
        Err(e) => println!("Error: {}", e),
    }
}
```

### 5. 泛型與特徵

```rust
trait Summary {
    fn summarize(&self) -> String;
}

struct Article {
    title: String,
    author: String,
    content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}

fn notify<T: Summary>(item: &T) {
    println!("Breaking: {}", item.summarize());
}

fn main() {
    let article = Article {
        title: String::from("Rust"),
        author: String::from("John"),
        content: String::from("..."),
    };
    notify(&article);
}
```

### 6. 並發

```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    thread::spawn(move || {
        let msg = "Hello from thread";
        tx.send(msg).unwrap();
    });
    
    let received = rx.recv().unwrap();
    println!("Received: {}", received);
}
```

## 為什麼學習 Rust？

1. **記憶體安全**：編譯時確保無記憶體錯誤
2. **無垃圾回收**：高效能與確定性
3. **並發安全**：防止資料競爭
4. **現代工具**：Cargo 包管理器
5. **系統程式設計**：安全的 C/C++ 替代品

## 參考資源

- "The Rust Programming Language" 官方書
- "Programming Rust"
- rust-lang.org
- rust-lang.github.io/rust-by-example
