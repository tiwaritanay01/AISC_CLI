#include <stdio.h>
#include "matrix.h"

void print_matrix(const char* label, int mat[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    printf("%s (%dx%d):\n", label, rows, cols);
    for (int i = 0; i < rows; i++) {
        printf("  [ ");
        for (int j = 0; j < cols; j++) {
            printf("%4d ", mat[i][j]);
        }
        printf(" ]\n");
    }
}

void multiply_matrices(int a[MAX_SIZE][MAX_SIZE], int r1, int c1,
                       int b[MAX_SIZE][MAX_SIZE], int r2, int c2,
                       int res[MAX_SIZE][MAX_SIZE]) {
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c2; j++) {
            res[i][j] = 0;
            for (int k = 0; k < c1; k++) {
                res[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

void transpose_matrix(int mat[MAX_SIZE][MAX_SIZE], int rows, int cols,
                      int trans[MAX_SIZE][MAX_SIZE]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            trans[j][i] = mat[i][j];
        }
    }
}

int main(void) {
    printf("=========================================\n");
    printf(" LabX Experiment 02: C Matrix Operations\n");
    printf("=========================================\n");

    int a[MAX_SIZE][MAX_SIZE] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int b[MAX_SIZE][MAX_SIZE] = {
        {7, 8},
        {9, 1},
        {2, 3}
    };
    int res[MAX_SIZE][MAX_SIZE];
    int trans[MAX_SIZE][MAX_SIZE];

    print_matrix("Matrix A", a, 2, 3);
    print_matrix("Matrix B", b, 3, 2);

    multiply_matrices(a, 2, 3, b, 3, 2, res);
    print_matrix("Product Matrix (A x B)", res, 2, 2);

    transpose_matrix(res, 2, 2, trans);
    print_matrix("Transpose of Product Matrix", trans, 2, 2);

    printf("=========================================\n");
    return 0;
}
