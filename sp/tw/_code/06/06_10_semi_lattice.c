#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int value;
} LatticeElement;

typedef struct {
    LatticeElement* elements;
    int size;
    LatticeElement top;
    LatticeElement bottom;
} SemiLattice;

LatticeElement meet(LatticeElement a, LatticeElement b) {
    LatticeElement result;
    result.value = (a.value < b.value) ? a.value : b.value;
    return result;
}

LatticeElement join(LatticeElement a, LatticeElement b) {
    LatticeElement result;
    result.value = (a.value > b.value) ? a.value : b.value;
    return result;
}

int is_leq(LatticeElement a, LatticeElement b) {
    return a.value <= b.value;
}

void print_lattice_info() {
    printf("=== Semi-Lattice Properties ===\n\n");
    printf("A semi-lattice is a partially ordered set where:\n");
    printf("  - Every pair of elements has a Greatest Lower Bound (meet)\n");
    printf("  - Every pair of elements has a Least Upper Bound (join)\n\n");
    
    printf("For Dataflow Analysis:\n");
    printf("  - IN set = meet of all predecessors' OUT sets\n");
    printf("  - OUT set = gen U (IN - kill)\n\n");
    
    LatticeElement a = {5}, b = {10}, c = {15};
    printf("Example with lattice elements {5, 10, 15}:\n");
    
    LatticeElement m = meet(a, c);
    printf("  meet(5, 15) = %d\n", m.value);
    
    LatticeElement j = join(a, c);
    printf("  join(5, 15) = %d\n", j.value);
    
    printf("\nPartial order: 5 <= 10 <= 15\n");
    printf("  is_leq(5, 10) = %d (true)\n", is_leq(a, b));
    printf("  is_leq(10, 5) = %d (false)\n", is_leq(b, a));
}

int main() {
    print_lattice_info();
    
    printf("\nApplication in Dataflow Analysis:\n");
    printf("  Reaching definitions: set union lattice\n");
    printf("  Available expressions: set intersection lattice\n");
    printf("  Constant propagation: constant lattice with TOP=UNINIT\n");
    
    return 0;
}
