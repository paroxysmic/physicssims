#ifndef _MLIB_H
#define _MLIB_H
#include <iostream>
#include <SDL.h>
struct vec2{
    float x, y, len;
    vec2();
    vec2(float eks, float wye);
    vec2 operator+(const vec2 &a);
    vec2 operator-(const vec2 &a);
    vec2 operator*(float a);
    vec2 operator/(float a);
    vec2 rot(float a);
    vec2 rotdeg(float a);
    void print();
};
class Matrix{
    public:
        Matrix(int width, int height);
        ~Matrix();
    private:
        int w, h;
        float *p;
};
void draw_circ(SDL_Renderer* renderer, float centre_x, float centre_y, int sides, float radius, SDL_FColor color);
#endif 