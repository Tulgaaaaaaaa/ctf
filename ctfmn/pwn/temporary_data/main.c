#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#define MAX_SIZE 30

__attribute__((constructor)) void setup() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

struct data {
  int size;
  char content[MAX_SIZE];
  char *name;
};

void get_name(char **result) {
  size_t n;
  getline(result, &n, stdin);
  (*result)[strcspn(*result, "\n")] = '\0';
  return;
}

void win(){
    system("/bin/sh");
}

int main() {
    struct data input = { 0 };
    size_t n;

    printf("[+] Size: ");
    scanf("%d", &input.size);
    getchar();
    
    if ((input.size = abs(input.size)) > MAX_SIZE) {
        printf("[-] Invalid size %d",input.size);
        exit(1);
    }

    printf("[+] Content: ");
    
    for(int i = 0; i < input.size - 1; i++) {
        char ch = getchar();        
        if (ch == '\n' || ch == EOF) {
            input.content[i] = '\0'; 
            break;
        }
        input.content[i] = ch; 
    }

    printf("[+] Name: ");
    get_name(&input.name);

    printf("\n[+] Size: %d \n", input.size);
    printf("[+] Content: %s \n", input.content);
    printf("[+] Name: %s \n\n", input.name);

    free(input.name);
    exit(0);
}
