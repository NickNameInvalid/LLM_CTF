#include <stdio.h>
#include <string.h>

void xor_transform(char *data, char key) {
    for (int i = 0; data[i] != '\0'; ++i) {
        data[i] ^= key;
    }
}

int main() {
    char input[100];
    printf("Enter your password: ");
    scanf("%99s", input);

    xor_transform(input, 0xAA);

    char xor_password[] = {
        0xc9, 0xd9, 0xcb, 0xdd, 0xc9, 0xde, 0xcc, 0xd1, 0x9a, 0xc4, 0xcf, 0xf5, 0xd9, 0xc2, 0xcf, 0xcf,
        0xfa, 0xf5, 0x9b, 0xdd, 0xc5, 0xf5, 0xd9, 0xc2, 0xcf, 0xfd, 0xda, 0xf5, 0x98, 0xc2, 0xd8, 0xcf,
        0xcf, 0xf5, 0x9f, 0xc2, 0xcf, 0xcf, 0xc1, 0xd9, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xd0, 0xf5, 0xf5,
        0xf5, 0xd0, 0xd0, 0xd0, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xd0, 0xd0, 0xd0, 0xd0, 0xd0, 0xd0, 0xf5,
        0xf5, 0xf5, 0xf5, 0xd2, 0xc5, 0xd8, 0xd7
    };

    if (strcmp(input, xor_password) == 0) {
        printf("Correct!\n");
    } else {
        printf("Access denied.\n");
    }

    return 0;
}