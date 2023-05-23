#ifndef INCLUDE_DPS310_CONFIG_H
#define INCLUDE_DPS310_CONFIG_H

#include "Include_Lib.h"

Dps310 Dps310PressureSensor = Dps310();   // // Dps310 Opject

int16_t temp_osr = 6;   //Temperature oversampling rate: 2^n, in this case: 2^0 = 1 oversample
int16_t prs_osr = 6;    //Pressure oversampling rate: 2^n, in this case: 2^6 = 64 oversampls
int32_t pressure, temperature;  //results

#endif
