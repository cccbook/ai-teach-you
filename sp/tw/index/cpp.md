# C++

## 概述

C++ 是一種通用的多範式程式語言，由 Bjarne Stroustrup 於 1979 年在貝爾實驗室發明。作為 C 語言的擴展，C++ 支援程序式、物件導向和泛型編程，至今仍是遊戲開發、系統軟體、高效能計算等領域的主流語言。

## 歷史

- **1979 年**：Bjarne Stroustrup 發明「C with Classes」
- **1983 年**：正式命名為 C++
- **1985 年**：發布第一個商業版本
- **1998 年**：C++98 標準化
- **2003 年**：C++03 小幅修正
- **2011 年**：C++11 重大更新（Lambda、右值引用）
- **2014 年**：C++14 持續改進
- **2017 年**：C++17 引入 Filesystem、Parallel Algorithms
- **2020 年**：C++20 引入模組、概念、協程
- **2023 年**：C++23 最新標準

## 核心特性

### 1. 類別與物件導向

```cpp
#include <iostream>
#include <string>

class Person {
private:
    std::string name;
    int age;

public:
    Person(const std::string& name, int age) 
        : name(name), age(age) {}
    
    void greet() const {
        std::cout << "Hello, I'm " << name << std::endl;
    }
    
    int getAge() const { return age; }
};

class Student : public Person {
private:
    int grade;

public:
    Student(const std::string& name, int age, int grade)
        : Person(name, age), grade(grade) {}
    
    void study() const {
        std::cout << "Studying hard!" << std::endl;
    }
};

int main() {
    Student student("John", 20, 85);
    student.greet();
    student.study();
    return 0;
}
```

### 2. 模板與泛型

```cpp
#include <iostream>

// 類別模板
template<typename T>
class Box {
private:
    T content;
public:
    Box(const T& content) : content(content) {}
    T get() const { return content; }
};

// 函數模板
template<typename T>
T max(const T& a, const T& b) {
    return (a > b) ? a : b;
}

int main() {
    Box<int> intBox(42);
    Box<std::string> strBox("Hello");
    
    std::cout << max(10, 20) << std::endl;
    std::cout << intBox.get() << std::endl;
    return 0;
}
```

### 3. STL 容器

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>

int main() {
    // vector（動態陣列）
    std::vector<int> vec = {5, 2, 8, 1, 9};
    vec.push_back(10);
    std::sort(vec.begin(), vec.end());
    
    // map（鍵值對）
    std::map<std::string, int> ages;
    ages["John"] = 30;
    ages["Alice"] = 25;
    
    // set（集合）
    std::set<int> numbers = {1, 2, 3, 4, 5};
    
    return 0;
}
```

### 4. Lambda 運算式

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5};
    
    // 基本 Lambda
    auto square = [](int x) { return x * x; };
    
    // 捕獲外部變數
    int factor = 2;
    auto multiply = [factor](int x) { return x * factor; };
    
    // 使用 std::for_each
    std::for_each(nums.begin(), nums.end(), 
        [](int& n) { n *= 2; });
    
    return 0;
}
```

### 5. RAII 與智慧指標

```cpp
#include <iostream>
#include <memory>

class Resource {
public:
    Resource() { std::cout << "Acquired\n"; }
    ~Resource() { std::cout << "Released\n"; }
    void use() { std::cout << "Using resource\n"; }
};

int main() {
    // unique_ptr（独占擁有權）
    std::unique_ptr<Resource> res1 = 
        std::make_unique<Resource>();
    res1->use();
    
    // shared_ptr（共享擁有權）
    std::shared_ptr<Resource> res2 = res1;
    
    // weak_ptr（weak reference）
    std::weak_ptr<Resource> weak = res2;
    
    return 0;
}
```

### 6. 移動語意

```cpp
#include <iostream>
#include <vector>

class BigObject {
public:
    std::vector<int> data;
    
    BigObject() { data.resize(1000); }
    
    // 移動建構子
    BigObject(BigObject&& other) noexcept 
        : data(std::move(other.data)) {}
    
    // 移動賦值運算子
    BigObject& operator=(BigObject&& other) noexcept {
        data = std::move(other.data);
        return *this;
    }
};

int main() {
    BigObject obj1;
    BigObject obj2 = std::move(obj1);
    return 0;
}
```

## 為什麼學習 C++？

1. **效能**：接近 C 的執行效率
2. **系統程式設計**：作業系統、遊戲引擎
3. **遊戲開發**： Unreal、Unity 遊戲引擎
4. **泛型編程**：強大的模板系統
5. **標準庫**：豐富的 STL

## 參考資源

- "The C++ Programming Language" by Bjarne Stroustrup
- "Effective C++" by Scott Meyers
- "C++ Primer"
- cppreference.com
