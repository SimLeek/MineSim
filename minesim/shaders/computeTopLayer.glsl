#version 430

uniform int width;
uniform int height;
uniform int depth;

const uint void_block   = 0;
const uint grass_block  = 1;
const uint dirt_block   = 2;

layout (std430, binding = 0) buffer Blocks {
    uint blocks[];
};

layout (local_size_x = 1, local_size_y = 1) in;
void main() {
     ivec3 resolution = ivec3(width, height, depth);
     ivec3 ourPos = ivec3(gl_GlobalInvocationID.xy);

     bool found_top = false;

     int index;

     for (int h=height-1; h>=0;--h){
        index = (ourPos.x*depth*height)+(h*depth)+ourPos.y;

        if(blocks[index] == grass_block){
            if(found_top){
                blocks[index] = dirt_block;
            }else{
                found_top = true;
            }
        }
     }

}
