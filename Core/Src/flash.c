#include "flash.h"
#include "stm32f1xx_hal.h"

//last page
#define PAGE_127_ADDRESS 0x0801FC00
#define IS_PAGE_END(pa) FLASH_PAGE_SIZE > ((pa) - PAGE_127_ADDRESS)

uint32_t flash_write(uint32_t start_address, uint32_t *buf, uint16_t n)
{
    uint32_t error;
    uint32_t address;

    FLASH_EraseInitTypeDef es = {
        .TypeErase   = FLASH_TYPEERASE_PAGES,
        .PageAddress = PAGE_127_ADDRESS,
        .NbPages     = 1
    };

    HAL_FLASH_Unlock();

    if (start_address == 0 && HAL_FLASHEx_Erase(&es, &error) != HAL_OK)
    {
        return HAL_FLASH_GetError();
    }

    for(address = PAGE_127_ADDRESS + start_address; n != 0 && IS_PAGE_END(address); n--, buf++, address += 4)
    {
        if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address, *buf) != HAL_OK)
        {
            return HAL_FLASH_GetError();
        }
    }

    HAL_FLASH_Lock();

    return 0;
}


void flash_read(uint32_t start_address, uint32_t *buf, uint16_t n)
{
    uint32_t address;

    for(address = PAGE_127_ADDRESS + start_address; n != 0 && IS_PAGE_END(address); n--, buf++, address += 4)
    {
        *buf = *(__IO uint32_t *)address;
    }
}

