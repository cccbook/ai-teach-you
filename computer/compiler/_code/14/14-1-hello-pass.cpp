#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {
    struct HelloPass : public FunctionPass {
        static char ID;
        HelloPass() : FunctionPass(ID) {}
        
        bool runOnFunction(Function &F) override {
            errs() << "Hello: ";
            errs().write_escaped(F.getName()) << '\n';
            return false;
        }
    };
}

char HelloPass::ID = 0;
static RegisterPass<HelloPass> X("hello", "Hello World Pass");
