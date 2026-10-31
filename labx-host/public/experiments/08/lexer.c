#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "tokens.h"

const char* get_token_type_name(TokenType t) {
    switch (t) {
        case TOKEN_KEYWORD:    return "KEYWORD";
        case TOKEN_IDENTIFIER: return "IDENTIFIER";
        case TOKEN_NUMBER:     return "NUMBER";
        case TOKEN_OPERATOR:   return "OPERATOR";
        case TOKEN_DELIMITER:  return "DELIMITER";
        default:               return "UNKNOWN";
    }
}

int is_keyword(const char* s) {
    const char* keywords[] = {"int", "float", "if", "else", "while", "return", NULL};
    for (int i = 0; keywords[i] != NULL; i++) {
        if (strcmp(keywords[i], s) == 0) return 1;
    }
    return 0;
}

void tokenize(const char* input) {
    int i = 0;
    int len = (int)strlen(input);

    printf("Input Stream: \"%s\"\n\n", input);
    printf("Line | Lexeme          | Token Type\n");
    printf("-----+-----------------+-------------\n");

    while (i < len) {
        if (isspace((unsigned char)input[i])) {
            i++;
            continue;
        }

        if (isalpha((unsigned char)input[i]) || input[i] == '_') {
            char buffer[64];
            int b = 0;
            while (i < len && (isalnum((unsigned char)input[i]) || input[i] == '_')) {
                if (b < 63) buffer[b++] = input[i];
                i++;
            }
            buffer[b] = '\0';
            TokenType t = is_keyword(buffer) ? TOKEN_KEYWORD : TOKEN_IDENTIFIER;
            printf(" 1   | %-15s | %s\n", buffer, get_token_type_name(t));
            continue;
        }

        if (isdigit((unsigned char)input[i])) {
            char buffer[64];
            int b = 0;
            while (i < len && isdigit((unsigned char)input[i])) {
                if (b < 63) buffer[b++] = input[i];
                i++;
            }
            buffer[b] = '\0';
            printf(" 1   | %-15s | %s\n", buffer, get_token_type_name(TOKEN_NUMBER));
            continue;
        }

        if (strchr("+-*/=", input[i]) != NULL) {
            printf(" 1   | %-15c | %s\n", input[i], get_token_type_name(TOKEN_OPERATOR));
            i++;
            continue;
        }

        if (strchr("();{},", input[i]) != NULL) {
            printf(" 1   | %-15c | %s\n", input[i], get_token_type_name(TOKEN_DELIMITER));
            i++;
            continue;
        }

        printf(" 1   | %-15c | %s\n", input[i], get_token_type_name(TOKEN_UNKNOWN));
        i++;
    }
}

int main(void) {
    printf("=========================================\n");
    printf(" LabX Experiment 08: Lexical Analyzer\n");
    printf("=========================================\n");

    const char* sample_code = "int total = count + 42;";
    tokenize(sample_code);

    printf("=========================================\n");
    return 0;
}
