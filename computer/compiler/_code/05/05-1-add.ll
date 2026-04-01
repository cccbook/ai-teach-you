; ModuleID = '05-1-add.c'
source_filename = "05-1-add.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin"

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @add(i32, i32) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32 %0, i32* %a, align 4
  store i32 %1, i32* %b, align 4
  %5 = load i32, i32* %a, align 4
  %6 = load i32, i32* %b, align 4
  %7 = add nsw i32 %5, %6
  store i32 %7, i32* %3, align 4
  %8 = load i32, i32* %3, align 4
  ret i32 %8
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @main() #0 {
  %x = alloca i32, align 4
  %y = alloca i32, align 4
  %z = alloca i32, align 4
  store i32 10, i32* %x, align 4
  store i32 20, i32* %y, align 4
  %1 = load i32, i32* %x, align 4
  %2 = load i32, i32* %y, align 4
  %3 = call i32 @add(i32 %1, i32 %2)
  store i32 %3, i32* %z, align 4
  %4 = load i32, i32* %z, align 4
  ret i32 %4
}

attributes #0 = { noinline nounwind optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "nounroll-loops"="false" "optional-realign-stack"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+fxsr,+mmx,+sse,+sse2,+sse3,+ssse3" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}
!0 = !{i32 1, !"Objective-C Version", i32 2}
!1 = !{i32 1, !"Objective-C Image Info Version", i32 0}
!2 = !{i32 4, !"Objective-C Image Info Section", !4}
!3 = !{!"Apple LLVM version 9.0.0 (clang-900.0.39.2)"}
!4 = !{!"__OBJC,__info_plist,regular,no_dead_strip"}
