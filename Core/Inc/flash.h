#ifndef __FALSH_OP_
#define __FALSH_OP_

#include <stdint.h>

uint32_t flash_write(uint32_t start_address, uint32_t *buf, uint16_t n);
void flash_read(uint32_t start_address, uint32_t *buf, uint16_t n);

#endif //__FALSH_OP_
