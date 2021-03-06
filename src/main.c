/* SPDX-License-Identifier: MIT */

#include "adt.h"
#include "fb.h"
#include "string.h"
#include "uart.h"
#include "uartproxy.h"
#include "utils.h"
#include "xnuboot.h"

#include "../build/build_tag.h"

//#define LOGO

void print_info(void)
{
    printf("Device info:\n");
    printf("  Model: %s\n", adt_getprop(adt, 0, "model", NULL));
    printf("  Target: %s\n", adt_getprop(adt, 0, "target-type", NULL));

    int chosen = adt_path_offset(adt, "/chosen");
    if (chosen > 0) {
        u32 board_id = ~0, chip_id = ~0;
        if (ADT_GETPROP(adt, chosen, "board-id", &board_id) < 0)
            printf("Failed to find board-id\n");
        if (ADT_GETPROP(adt, chosen, "chip-id", &chip_id) < 0)
            printf("Failed to find chip-id\n");

        printf("  Board-ID: 0x%x\n", board_id);
        printf("  Chip-ID: 0x%x\n", chip_id);
    } else {
        printf("No chosen node!\n");
    }

    printf("\n");
}

void disable_wdt(void)
{
    int node = adt_path_offset(adt, "/arm-io/wdt");

    if (node < 0) {
        printf("WDT node not found!\n");
        return;
    }

    printf("WDT node @ 0x%x\n", node);

    const void *reg = adt_getprop(adt, node, "reg", NULL);

    if (!reg) {
        printf("WDT reg property not found!\n");
        return;
    }

    u64 wdt_regs;
    memcpy(&wdt_regs, reg, sizeof(u64));

    printf("WDT registers @ 0x%lx\n", wdt_regs);

    write32(0x23d2b001c, 0);
}

void m1n1_main(void)
{
    printf("\n\nm1n1 v%s\n", BUILD_TAG);
    printf("Copyright (C) 2021 The Asahi Linux Contributors\n");
    printf("Licensed under the MIT license\n");

#ifdef LOGO
    fb_init();
    fb_display_logo();
#endif

    print_info();
    disable_wdt();

    /*
        u64 dtaddr = ((u64)cur_boot_args.devtree) - cur_boot_args.virt_base +
                     cur_boot_args.phys_base;*/

    //     hexdump((void *)dtaddr, cur_boot_args.devtree_size);
    //
    //     while (1)
    //         uart_putbyte(uart_getbyte());

    printf("Running proxy...\n");
    uartproxy_run();

    while (1)
        ;
}
