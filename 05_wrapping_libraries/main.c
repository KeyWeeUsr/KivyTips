#include <stdio.h>
#include "hellolib.h"

int main() {
    char * string = hello();
    printf("%s", string);
    return 0;
}
