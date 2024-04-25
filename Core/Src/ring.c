#include <stdio.h>

#include "stm32f1xx_hal.h"
#include "ring.h"
#include "flash.h"
#include "main.h"

uint32_t __attribute__(( section(".data") )) LED[LED_LEN] = {0};

#define DO_UP   (GPIOB->BSRR = (uint32_t)0x00000800)
#define DO_DOWN (GPIOB->BSRR = (uint32_t)0x08000000)
#define PAUSE(p) for(int j = 0; j < (p); j++)__NOP();

void ring_reset(void)
{
    int j;

    DO_DOWN;
    for(j = 0; j < 300; j++)__NOP();
    DO_UP;
}

void ring_flash(void)
{
    int i,n;

    for(n = 0; n < LED_LEN; n++) {
        for(i = 0; i < 24; i++) {
            if (LED[n] & (1 << i)) {
                DO_UP;
                PAUSE(3)
                DO_DOWN;
                __NOP();
            } else {
                DO_UP;
                __NOP();
                DO_DOWN;
                PAUSE(3)
            }
        }
    }
}

void ring_print(void)
{
    for(int n = 0; n < LED_LEN; n++)
        printf(" %d:%06X", n, (unsigned)LED[n]);
}

void ring_all_color_set(uint32_t c)
{
    for(int n = 0; n < LED_LEN; n++) LED[n] = c & 0xFFFFFF;

    ring_flash();
}

void ring_color_set(int n, uint32_t c)
{
    if (n < LED_LEN) {
        LED[n] = c & 0xFFFFFF;
    }
}

void save_led(void)
{
    HAL_StatusTypeDef r;

    r = flash_write(0, LED, LED_LEN);

    if (r != 0) {
        printf("%s error flash write: %d\r\n", __func__, r);
    }

    uint32_t f = get_randome_move();
    r = flash_write(LED_LEN * 4, &f, 1);

    if (r != 0) {
        printf("%s error flash write: %d\r\n", __func__, r);
    }
}

void restore_led(void)
{
    flash_read(0, LED, LED_LEN);

    uint32_t f = 0;
    flash_read(LED_LEN * 4, &f, 1);
    set_randome_move(f);
}

void ring_all_color_set_random(void)
{
    for(int n = 0; n < LED_LEN; n++) {
        while((LED[n] = adc_random() & 0xFFFFFF) == 0);
    }

    ring_flash();
}

void ring_all_color_set_random_move(void)
{
    for(int n = LED_LEN - 1; n != 0; n--) {
        LED[n] = LED[n-1];
    }

    while((LED[0] = adc_random() & 0xFFFFFF) == 0);

    ring_flash();
}

