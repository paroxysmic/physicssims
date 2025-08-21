#include <iostream>
#include <vector>
#include <SDL.h>
#include <math.h>
#include <numbers>
#include <algorithm>
#include "mlib.h"
#define TAU 2 * M_PI
//mingw32-make -f MakeFile
struct Ball{
    Ball(vec2 position, vec2 velocity, float radius) {
        pos = position;
        vel = velocity;
        acc = vec2(0, 1);
        rad = radius;
    }
    void updatePos() {
        //f
        pos = pos + vel;
        vel = vel + acc;
    }
    void collCheck() {
        if (pos.x > (700 - rad) || pos.x < rad) {
            vel.x *= -0.8;
            vel.y *= 0.8;
        }
        if (pos.y > (700 - rad) || pos.y < rad) {
            vel.x *= 0.8;
            vel.y *= -0.8;
        }
        pos.x = std::min(pos.x, 700 - rad);
        pos.x = std::max(pos.x, rad);
        pos.y = std::min(pos.y, 700 - rad);
        pos.y = std::max(pos.y, rad);

    }
    void render(SDL_Renderer *renderer) {
        draw_circ(renderer, pos.x, pos.y, 10, rad, SDL_FColor{0.0, 0.0, 1.0, 1.0});
    }
    vec2 pos, vel, acc;
    float rad;
};
struct Spring { 
    Spring(Ball* ballptr1, Ball* ballptr2, float desiredLen, float strength = 1) {
        b1 = ballptr1;
        b2 = ballptr2;
        desiredLen = dl;
        strength = str;
    }
    void updatePos() {
        //pushing will be represented as positive here
        vec2 b1tb2 = (b2->pos - b1->pos);
        float sprtension = dl - (b1->pos - b2->pos).len;
        b1->acc = b1->acc + (b1tb2 * sprtension / 10);
        b2->acc = b2->acc - (b1tb2 * sprtension / 10);
        b1->updatePos();
        b2->updatePos();
        b1->collCheck();
        b2->collCheck();
    }
    void render(SDL_Renderer *renderer) {
        b1->render(renderer);
        b2->render(renderer);
    }
    Ball *b1, *b2;
    float dl, str;
};
Ball ball1{vec2(375, 375), vec2(0, 1), 20};
Ball ball2{vec2(350, 350), vec2(0, 1), 20};
Spring spr{*ball1, *ball2, 100, 1};
int main(int argc, char* argv[]){
    SDL_Init(SDL_INIT_EVENTS);
    SDL_Window* win = SDL_CreateWindow("sdl testing :]", 700, 700, 0);
    SDL_Renderer* renderer = SDL_CreateRenderer(win, NULL);
    SDL_SetRenderVSync(renderer, 1);
    bool running = true;
    SDL_Event e;
    while(running){
        while(SDL_PollEvent(&e)){
            if(e.type == SDL_EVENT_QUIT){
                running = false;
            }
        }
        ball.updatePos();
        ball.collCheck();
        SDL_SetRenderDrawColor(renderer, 0xee, 0xee, 0xee, 0xff);
        SDL_RenderClear(renderer);
        spr.render(renderer);
        SDL_RenderPresent(renderer);
    }
    return 0;
}