#ifndef __RING_H__
#define __RING_H__

#include <stdint.h>

#define LED_LEN 12

// BBBB RRRR GGGG
#define COLOR   0xFFFFFF
#define WHITE   0xFFFFFF
#define BLACK   0x000000
#define RED     0x00FF00
#define BLUE    0xFF0000
#define GREEN   0x0000FF

void ring_all_color_set(uint32_t c);
void ring_reset(void);
void ring_all_color_set_random(void);
void ring_all_white_set_random(void);

#endif //__RING_H__