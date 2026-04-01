; ModuleID = '05-3-loop.c'
source_filename = "05-3-loop.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin"

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @sum(i32) #0 {
  %n = alloca i32, align 4
  %total = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 %0, i32* %n, align 4
  store i32 0, i32* %total, align 4
  store i32 1, i32* %i, align 4
  br label %1

; <label>:1                                       ; preds = %7, %0
  %2 = load i32, i32* %i, align 4
  %3 = load i32, i32* %n, align 4
  %4 = icmp sle i32 %2, %3
  br i1 %4, label %5, label %8

; <label>:5                                       ; preds = %1
  %6 = load i32, i32* %total, align 4
  %7 = add nsw i32 %6, %2
  store i32 %7, i32* %total, align 4
  br label %7

; <label>:7                                       ; preds = %5
  %8 = load i32, i32* %i, align 4
  %9 = add nsw i32 %8, 1
  store i32 %9, i32* %i, align 4
  br label %1

; <label>:8                                       ; preds = %1
  %10 = load i32, i32* %total, align 4
  ret i32 %10
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @main() #0 {
  %result = alloca i32, align 4
  %1 = call i32 @sum(i32 10)
  store i32 %1, i32* %result, align 4
  %2 = load i32, i32* %result, align 4
  ret i32 %2
}

attributes #0 = { noinline nounwind optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "nounroll-loops"="false" "optional-realign-stack"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sse,+sse2,+sse3,+ssse3" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}
!0 = !{i32 1, !"Objective-C Version", i32 2}
!1 = !{i32 1, !"Objective-C Image Info Version", i32 0}
!2 = !{i32 4, !"Objective-C Image Info Section", !4}
!3 = !{!"Apple LLVM version 9.0.0 (clang-900.0.39.2)"}
!4 = !{!"__OBJC,__info_plist,regular,no_dead_strip"}
