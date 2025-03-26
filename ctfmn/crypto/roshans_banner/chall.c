#include <stdio.h>
#include <string.h>

int check_flag(char *str) {
    int length = strlen(str);
    for (int i = 0; i < length; i++) {
        str[i] = str[i] ^ i;
    }
    char enc[] = {72, 91, 87, 50, 60, 126, 84, 52, 126, 108, 120, 88, 63, 82, 63, 124, 79, 87, 103, 125, 75, 93, 37, 127, 43, 100};
    
    int match = 1;
    for (int i = 0; i < length; i++) {
        if (str[i] != enc[i]) {
            match = 0;
            break;
        }
    }
    return match;
}

int main() {
    char flag[26];
    printf("flag aa oruul: ");
    fgets(flag, sizeof(flag), stdin);
    
    if (check_flag(flag)){
        printf("flag aa olsoon submit hii2 xd");
    }else{
        printf("flag aa zov oloogu baisht eeeee!!!!!!!");
    }
    
    return 0;
}
