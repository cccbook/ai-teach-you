// 表單處理

let form = document.querySelector("#myForm");
let nameInput = document.querySelector("#name");
let emailInput = document.querySelector("#email");

// 監聽表單提交
form.addEventListener("submit", function(event) {
    event.preventDefault();
    console.log("表單提交");
    
    // 取得表單資料
    let formData = new FormData(form);
    console.log("name:", formData.get("name"));
    console.log("email:", formData.get("email"));
});

// 監聽輸入事件
nameInput.addEventListener("input", function(event) {
    console.log("input:", event.target.value);
});

emailInput.addEventListener("change", function(event) {
    console.log("change:", event.target.value);
});

// 驗證表單
form.addEventListener("submit", function(event) {
    let errors = [];
    
    if (nameInput.value.trim() === "") {
        errors.push("姓名必填");
    }
    
    if (!emailInput.value.includes("@")) {
        errors.push("email 格式錯誤");
    }
    
    if (errors.length > 0) {
        event.preventDefault();
        alert(errors.join("\n"));
    }
});

// 自訂驗證
nameInput.addEventListener("blur", function() {
    if (this.value.length < 2) {
        this.setCustomValidity("姓名至少2個字");
    } else {
        this.setCustomValidity("");
    }
});

// radio 按鈕
let genderInputs = document.querySelectorAll('input[name="gender"]');
genderInputs.forEach(input => {
    input.addEventListener("change", function() {
        console.log("選取性別:", this.value);
    });
});

// checkbox
let hobbies = document.querySelectorAll('input[name="hobby"]');
hobbies.forEach(checkbox => {
    checkbox.addEventListener("change", function() {
        let selected = Array.from(hobbies)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        console.log("興趣:", selected);
    });
});

// select 下拉選單
let countrySelect = document.querySelector("#country");
countrySelect.addEventListener("change", function() {
    console.log("國家:", this.value);
    console.log("選項文字:", this.options[this.selectedIndex].text);
});

// 重設表單
form.addEventListener("reset", function() {
    console.log("表單已重設");
});

let resetBtn = document.querySelector("#resetBtn");
resetBtn.addEventListener("click", function() {
    form.reset();
});