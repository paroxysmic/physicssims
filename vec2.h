#ifndef _VEC2_H
#define _VEC2_H
#include <math.h>
typedef struct vec2{
    double x = 0;
    double y = 0;
}vec2;
/*
Takes two vectors as input and stores
their sum in the third.
*/
void vecadd(vec2 a, vec2 b, vec2* c) {
    c->x = a.x + b.x;
    c->y = a.y + b.y;
}
/*
Takes two vectors as input and stores
the first minus the second in the third.
*/
void vecsub(vec2 a, vec2 b, vec2* c) {
    c->x = a.x - b.x;
    c->y = a.y - b.y;
}
/*
Scalar multiplication, takes two vectors and a scalar, 
stores the first times the scalar in the second.
*/
void vecmul(vec2 a, double b, vec2* c) {
    c->x = a.x * b;
    c->y = a.y * b;
}
/*
Vector normalization, take two vectors as input.
Stores the normal of the first vector in the second.*/
void vecnorm(vec2 a, vec2* b) {
    double len = sqrt(a.x * a.x + a.y * a.y);
    b->x = a.x / len;
    b->y = a.y / len;
}
#endif