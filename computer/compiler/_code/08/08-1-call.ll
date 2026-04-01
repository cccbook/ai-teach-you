; ModuleID = '08-1-call.c'
source_filename = "08-1-call.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin"

@.str = private unnamed_addr constant [9 x i8] c"Result: %\00", align 1

define i32 @add(i32, i32) #0 {
  %3 = add nsw i32 %0, %1
  ret i32 %3
}

define i32 @main() #0 {
  %result = alloca i32, align 4
  %printf.addr = alloca i8*, align 8
  store i32 10, i32* %result, align 4
  %1 = call i32 @add(i32 10, i32 20)
  store i32 %1, i32* %result, align 4
  %2 = load i32, i32* %result, align 4
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str, i32 0, i32 0), i32 %2)
  ret i32 0
}

declare i32 @printf(i8*, ...) #1

attributes #0 = { noinline nounwind optnone ssp uwtable }
attributes #1 = { "disable-tail-calls"="false" }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}
!0 = !{i32 1, !"Objective-C Version", i32 2}
!1 = !{i32 1, !"Objective-C Image Info Version", i32 0}
!2 = !{i32 4, !"Objective-C Image Info Section", !4}
!3 = !{!"Apple LLVM version 9.0.0 (clang-900.0.39.2)"}
!4 = !{!"__OBJC,__info_plist,regular,no_dead_strip"}
