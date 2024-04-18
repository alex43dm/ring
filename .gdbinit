#set auto-load safe-path .
source svd/svd_gdb.py
svd_load svd/STM32F103xx.svd

set output-radix 16

file build/rng01.elf

#target extended-remote | openocd -f openocd.cfg -c "gdb_port pipe; log_output openocd.log"
target extended-remote 127.0.0.1:3333

set remote hardware-breakpoint-limit 6
set remote hardware-watchpoint-limit 4

monitor reset halt
monitor arm semihosting enable
monitor arm semihosting_fileio enable

# Write 0xC5ACCE55 to the ITM Lock Access Register to unlock the write access to the ITM registers
#set *0xE0000FB0 =0xC5ACCE55
# Write 0x00010005 to the ITM Trace Control Register to enable the ITM with Synchronous enabled and an ATB ID different from 0x00
#set *0xE0000E80= 0x00010005
# Write 0x1 to the ITM Trace Enable Register to enable the Stimulus Port 0
#set *0xE0000E00= (*0xE0000E00) | 0x1
#write 1 to ITM trace privilege register to unmask Stimulus ports 7:0
#set *0xE0000E40= (*0xE0000E40) | 0x1

load

break USB_CDC_RxHandler
#break HAL_RTC_WaitForSynchro
#break ErrorHandler
#break assert_param
#break AlarmAEventCallback
#break HardFault_Handler
#break HAL_TIM_PeriodElapsedCallback
#break HAL_TIM_PeriodElapsedCallback
#TIM2_IRQHandler

continue
