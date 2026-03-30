# Java

## 概述

Java 是一種廣泛使用的物件導向程式語言，由 Sun Microsystems 的 James Gosling 於 1995 年發明。Java 的核心理念是「寫一次，到處執行」（Write Once, Run Anywhere），透過 Java 虛擬機器（JVM）實現跨平台相容性。

## 歷史

- **1995 年**：James Gosling 發布 Java 1.0
- **1997 年**：Java 1.1 引入內部類別
- **2000 年**：Java 1.4 引入 assert
- **2004 年**：Java 5（1.5）引入泛型、注解
- **2011 年**：Java 7 引入 try-with-resources
- **2014 年**：Java 8 引入 Lambda 運算式
- **2017 年**：Java 9 引入模組系統
- **現在**：Java 21 為最新 LTS 版本

## 核心特性

### 1. 物件導向

```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public void greet() {
        System.out.println("Hello, I'm " + name);
    }
}

public class Main {
    public static void main(String[] args) {
        Person person = new Person("John", 30);
        person.greet();
    }
}
```

### 2. 繼承與介面

```java
interface Drawable {
    void draw();
}

abstract class Shape implements Drawable {
    protected String color;
    
    public Shape(String color) {
        this.color = color;
    }
    
    abstract double area();
}

class Circle extends Shape {
    private double radius;
    
    public Circle(double radius, String color) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }
    
    @Override
    double area() {
        return Math.PI * radius * radius;
    }
}
```

### 3. 泛型

```java
// 泛型類別
class Box<T> {
    private T content;
    
    public void set(T content) {
        this.content = content;
    }
    
    public T get() {
        return content;
    }
}

// 泛型方法
public <T> void printArray(T[] array) {
    for (T element : array) {
        System.out.println(element);
    }
}

// 使用
Box<Integer> intBox = new Box<>();
intBox.set(42);
Integer value = intBox.get();
```

### 4. Lambda 運算式

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class LambdaExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // forEach
        numbers.forEach(n -> System.out.println(n));
        
        // map
        List<Integer> squares = numbers.stream()
            .map(n -> n * n)
            .collect(Collectors.toList());
        
        // filter
        List<Integer> evens = numbers.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        
        // reduce
        int sum = numbers.stream()
            .reduce(0, Integer::sum);
    }
}
```

### 5. 例外處理

```java
public class ExceptionExample {
    public static void main(String[] args) {
        try {
            int result = divide(10, 0);
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("Finally block");
        }
    }
    
    public static int divide(int a, int b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }
}
```

## 編譯與執行

```bash
# 編譯
javac Main.java

# 執行
java Main
```

## JVM 架構

```
原始碼 → javac → 位元組碼 → JVM → 機器碼
                              ↓
                        [類別載入器]
                        [執行引擎]
                        [記憶體管理]
                        [本地方法介面]
```

## 為什麼學習 Java？

1. **企業級應用**：大型系統開發首選
2. **Android 開發**：Android 官方語言
3. **跨平台**：JVM 實現一次編譯，到處執行
4. **豐富生態**：龐大的函式庫和框架
5. **的就業市場**：企業需求高

## 參考資源

- "Effective Java" by Joshua Bloch
- Java 官方文檔：docs.oracle.com/javase
- Spring Framework 官方網站
