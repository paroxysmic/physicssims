#include "mlib.h"
#include <cmath>
vec2::vec2() {
    x = 0.0;
    y = 0.0;
    len = 0.0;
}
vec2::vec2(float eks, float wye) {
    x = eks;
    y = wye;
    len = sqrt(x * x + y * y);
}
vec2 vec2::operator+(const vec2 &a) {
    return vec2(x + a.x, y + a.y);
}
vec2 vec2::operator-(const vec2 &a) {
    return vec2(x - a.x, y - a.y);
}
vec2 vec2::operator*(float a) {
    return vec2(x * a, y * a);
}
vec2 vec2::operator/(float a) {
    return vec2(x / a, y / a);
}
vec2 vec2::rot(float a) {
    float ca = cos(a);
    float sa = sin(a);
    return vec2(x * ca - y * sa, x * sa + y * ca);
}
vec2 vec2::rotdeg(float a) {
    float rval = 3.141592653589793 * a / 180;
    return this->rot(rval);
}
void vec2::print() { 
    std::cout << '[' << x << ", " << y << "]\n";
}
Matrix::Matrix(int width, int height) {
    p = new float[width * height];
    for (int i=0;i<height;i++) {
        for (int j=0;j<width;j++) {
            p[j + i * width] = 0;
        }
    }
}
Matrix::~Matrix() {
    delete p;
}
void draw_circ(SDL_Renderer *renderer, float centre_x, float centre_y, const int sides, float radius, SDL_FColor color) {
    SDL_Vertex *vertarr = new SDL_Vertex[sides];
    int *indarr = new int[sides*3 - 6];
    //fan model!
    for(int i=0;i<sides;i++) {
        vec2 rvec = vec2(0, radius).rotdeg(i * 360 / sides);
        vertarr[i].position.x = rvec.x + centre_x;
        vertarr[i].position.y = rvec.y + centre_y;
        vertarr[i].color = color;
    }
    for(int i=0;i<sides-2;i++) {
        indarr[3 * i] = 0;
        indarr[3 * i + 1] = i + 1;
        indarr[3 * i + 2] = i + 2;
    }
    SDL_RenderGeometry(renderer, nullptr, vertarr, sides, indarr, sides*3 - 6);
}