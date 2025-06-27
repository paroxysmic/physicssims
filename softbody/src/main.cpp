#include <iostream>
#include <vector>
#include <SDL.h>
#include <math.h>
#include <numbers>
#include <algorithm>
#include "mlib.h"
#define TAU 2 * M_PI
//mingw32-make -f MakeFile
class Ball{
    public:
        Ball(vec2 position, vec2 velocity) {
            pos = position;
            vel = velocity;
            acc = vec2(0, 1);
        }
        void updatePos() {
            pos = pos + vel + (acc * 0.5);
            vel = vel + acc;
        }
        void collCheck() {
            if (pos.x > 695 || pos.x < 5) {
                vel.x *= -0.8;
                vel.y *= 0.8;
            }
            if (pos.y > 695 || pos.y < 5) {
                vel.x *= 0.8;
                vel.y *= -0.8;
            }
            pos.x = std::min(pos.x, 695.0f);
            pos.x = std::max(pos.x, 5.0f);
            pos.y = std::min(pos.y, 695.0f);
            pos.y = std::max(pos.y, 5.0f);

        }
        void render(SDL_Renderer *renderer) {
            draw_circ(renderer, pos.x, pos.y, 8, 5, SDL_FColor{0.0, 0.0, 1.0, 1.0});
        }
    private:
        vec2 pos, vel, acc;
};
Ball ball{vec2(375, 375), vec2(0, 1)};
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
        ball.render(renderer);
        SDL_RenderPresent(renderer);
    }
    return 0;
}