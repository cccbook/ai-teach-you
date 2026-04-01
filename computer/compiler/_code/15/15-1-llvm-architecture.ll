; ModuleID = '15-1-llvm-architecture.c'
source_filename = "15-1-llvm-architecture.c"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-darwin"

@.str = private unnamed_addr constant [12 x i8] c"Fibonacci: %\00", align 1

define i32 @fibonacci(i32) #0 {
entry:
  %n.addr = alloca i32, align 4
  store i32 %0, i32* %n.addr, align 4
  %0 = load i32, i32* %n.addr, align 4
  %cmp = icmp sle i32 %0, 1
  br i1 %cmp, label %if.then, label %if.else

if.then:
  %1 = load i32, i32* %n.addr, align 4
  br label %return

if.else:
  %2 = load i32, i32* %n.addr, align 4
  %sub = sub nsw i32 %2, 1
  %call = call i32 @fibonacci(i32 %sub)
  %3 = load i32, i32* %n.addr, align 4
  %sub2 = sub nsw i32 %3, 2
  %call3 = call i32 @fibonacci(i32 %sub2)
  %add = add nsw i32 %call, %call3
  br label %return

return:
  %retval.0 = phi i32 [ %1, %if.then ], [ %add, %if.else ]
  ret i32 %retval.0
}

define i32 @main() #0 {
entry:
  %result = alloca i32, align 4
  %call = call i32 @fibonacci(i32 10)
  store i32 %call, i32* %result, align 4
  %0 = load i32, i32* %result, align 4
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str, i32 0, i32 0), i32 %0)
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
