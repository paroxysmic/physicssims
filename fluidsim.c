#define HEIGHT 20
#define WIDTH 40
#define ind(x, y) ((x) + (WIDTH * y))
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
typedef struct FluidCell 
{
    float fluidDensity;
    float flow[4];
    /*
    0 - Top
    1 - Left
    2 - Bottom
    3 - Right
    */
    bool opensides[4];
} FluidCell;

void disp(FluidCell* arr) {
    //assuming all densities are between 0 and 1
    for(int y=0;y<HEIGHT;y++) {
        printf("|");
        for(int x=0;x<WIDTH;x++) {
            int cell = floor(23 * (arr[ind(x, y)].fluidDensity));
            printf("%c[48;5;%dm  ", 27, 232 + cell);
        }
        printf("%c[48;5;0m|\n", 27);
    }
}

int main(int argc, char **argv) {
    FluidCell cells[800];
    for(int i=0;i<800;i++) {
        for(int j=0;j<4;j++) {
            cells[i].flow[j] = 0;
        }
        cells[i].opensides[0] = (i > 39);
        cells[i].opensides[1] = (i % 40) != 0;
        cells[i].opensides[2] = (i < 760);
        cells[i].opensides[4] = (i % 40) != 39;
        cells[i].fluidDensity = 0;
    }
    //left is positive
    double horizvecs[780] = {0};
    //down is positive
    double vertvecs[760] = {0};
    for(int iters=0;iters<1e4;iters++) {
        /*
        Adding gravity to the vertical vecs
        */
        for(int i=0;i<760;i++) {
            vertvecs[i] += 0.02;
        }
        /*
        forcing incompressibility, equalizing flowλ
        */
        for(int y=0;y<20;y++) {
            for(int x=0;x<40;x++) {
                FluidCell cell = cells[x + (y * 40)];
                double totalFlow = 0;
                if(cell.opensides[0]) {
                    totalFlow += vertvecs[x + ((y - 1) * 40)];

                }
            }
        }
    }
    return 0;
}