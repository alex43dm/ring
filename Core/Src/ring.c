#include "stm32f1xx_hal.h"
#include "ring.h"
//#include "rand.h"

uint32_t __attribute__(( section(".data") )) LED[LED_LEN];

#define DO_UP   (GPIOB->BSRR = (uint32_t)0x00000800)
#define DO_DOWN (GPIOB->BSRR = (uint32_t)0x08000000)

void ring_reset(void)
{
    int j;

    DO_DOWN;
    for(j = 0; j < 300; j++)__NOP();
    DO_UP;
}

static void ring_flash(void)
{
    int i,j,n;

    for(n = 0; n < LED_LEN; n++) {
        for(i = 0; i < 24; i++) {
            if (LED[n] & (1 << i)) {
                DO_UP;
                for(j = 0; j < 3; j++)__NOP();
                DO_DOWN;
            } else {
                DO_UP;
                for(j = 0; j < 1; j++)__NOP();
                DO_DOWN;
                for(j = 0; j < 2; j++)__NOP();
            }
        }
    }
}

void ring_all_color_set(uint32_t c)
{
    for(int n = 0; n < LED_LEN; n++) LED[n] = c;

    ring_flash();
}

/*
void ring_all_color_set_random(void)
{
    ring_all_color_set(ADC1_get_val());
    //ring_all_color_set(rand());
}

void ring_all_white_set_random(void)
{
    uint8_t c = (uint8_t)ADC1_get_val();
    uint32_t f = (c << 16) | (c << 8) | c;
    ring_all_color_set(f);
}
*/
