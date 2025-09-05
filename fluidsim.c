#define HEIGHT 20
#define WIDTH 40
#define AREA (HEIGHT * WIDTH)
#define ind(x, y) ((x) + (WIDTH * (y)))
#define vertind(x, y) ((x) + ((WIDTH - 1) * y))
#define horiind(x, y) ((x) + (WIDTH * (y)))
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <time.h>
#include <windows.h>
#include <stdint.h>
void disp(double* arr) {
    //assuming all densities are between 0 and 1
    system("cls");
    for(int y=0;y<HEIGHT;y++) {
        printf("|");
        for(int x=0;x<WIDTH;x++) {
            int cell = floor(255 * (arr[ind(x, y)]));
            printf("\x1b[48;2;%d;%d;%dm  ", cell, cell, cell);
        }
        printf("\x1b[0m|\n");
    }
}
void debugdisp(int* arr) {
    for(int y=0;y<HEIGHT;y++) {
        for(int x=0;x<WIDTH;x++) {
            printf("%d   ", arr[x + y * WIDTH]);
        }
        printf("\n");
    }
}
void minimizeDiv(double* vertvecs, double* horizvecs) {
    for(int y=0;y<HEIGHT;y++) {
        for(int x=0;x<WIDTH;x++) {

        }
    }
}
int main(int argc, char **argv) {
    double cellDensities[WIDTH * HEIGHT] = {0};
    bool cellsOpenSides[WIDTH * HEIGHT * 4] = {0};
    int openSidesNums[WIDTH * HEIGHT] = {0};
    /*
    top - left- bottom - right
    */
    for(int i=0;i<800;i++) {
        if(i > (WIDTH - 1)) {
            cellsOpenSides[4 * i] = true;
            openSidesNums[i]++;
        }
        if((i % WIDTH) != 0) {
            cellsOpenSides[4 * i + 1] = true;
            openSidesNums[i]++;
        }
        if(i < (AREA - WIDTH)) {
            cellsOpenSides[4 * i + 2] = true;
            openSidesNums[i]++;
        }   
        if((i % WIDTH) != (WIDTH - 1)) {
            cellsOpenSides[4 * i + 3] = true;
            openSidesNums[i]++;
        }
        cellDensities[i]= 0.0;
    }
    //left is positive
    double horizvecs[AREA - HEIGHT] = {0};
    //down is positive
    double vertvecs[AREA - WIDTH] = {0};
    for(int iters=0;iters<1e2;iters++) {
        /*
        forcing incompressibility, equalizing flow
        ill js start with like 10 iters of gauss-seidel
        */
        for(int λ=0;λ<10;λ++) {
            for(int y=0;y<HEIGHT;y++) {
                for(int x=0;x<WIDTH;x++) {
                    int ind = x + y * WIDTH;
                    int openSidesNum = openSidesNums[ind];
                    double totalInflow = 0;
                    if(cellsOpenSides[4 * ind]) {
                        totalInflow += vertvecs[ind - WIDTH];
                    }
                    if(cellsOpenSides[4 * ind + 1]) {
                        totalInflow += horizvecs[ind - HEIGHT];
                    }
                    if(cellsOpenSides[4 * ind + 2]) {
                        totalInflow -= vertvecs[ind];
                    }
                    if(cellsOpenSides[4 * ind + 3]) {
                        totalInflow -= horizvecs[ind];
                    }                    
                    if(cellsOpenSides[4 * ind]) {
                        vertvecs[ind - WIDTH] -= totalInflow / openSidesNum;
                    }
                    if(cellsOpenSides[4 * ind + 1]) {
                        horizvecs[ind - HEIGHT] -= totalInflow / openSidesNum;
                    }
                    if(cellsOpenSides[4 * ind + 2]) {
                        vertvecs[ind] += totalInflow / openSidesNum;
                    }
                    if(cellsOpenSides[4 * ind + 3]) {
                        horizvecs[ind] += totalInflow / openSidesNum;
                    }
                }
            }
        }
        disp(cellDensities);
        Sleep(100);
    }
    return 0;
}