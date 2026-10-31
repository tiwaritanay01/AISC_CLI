#ifndef MATRIX_H
#define MATRIX_H

#define MAX_SIZE 10

void print_matrix(const char* label, int mat[MAX_SIZE][MAX_SIZE], int rows, int cols);
void multiply_matrices(int a[MAX_SIZE][MAX_SIZE], int r1, int c1,
                       int b[MAX_SIZE][MAX_SIZE], int r2, int c2,
                       int res[MAX_SIZE][MAX_SIZE]);
void transpose_matrix(int mat[MAX_SIZE][MAX_SIZE], int rows, int cols,
                      int trans[MAX_SIZE][MAX_SIZE]);

#endif
