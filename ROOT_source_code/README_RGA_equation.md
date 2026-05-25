
        Definition of RGA equation:

RGA equation describes relation between mask matrix, ppm's of gases, and RGA spectrum


    RGA spectrum is an experimentally measured ionic currents for every M/Z ratio

    PPM's are the true concentrations of gases in the mixture

    Mask matrix is a matrix, composed of RGA spectrums for every pure compound



/                      \   /         \   /       \
| Ar_01  He_01  CO2_01 |   |         |   | IC_01 |
| Ar_02  He_02  CO2_02 |   | Ar__PPM |   | IC_02 |
| Ar_03  He_03  CO2_03 | X | He__PPM | = | IC_03 |
| Ar_04  He_04  CO2_04 |   | CO2_PPM |   | IC_04 |
|...                   |   |         |   | ...   |
| Ar_50  He_50  CO2_50 |   |         |   | IC_50 |
\                      /   \         /   \       /

           /\                   /\           /\
            \                    \            \____ RGA Spectrum
             \                    \
              \                    \____ True PPM's of gases
               \
                \___ Mask matrix





As it can be seen, RGA spectrum is a linear combination of masks, multiplied by concentrations of respective compounds

Process of PPM computing is the solution of True PPM's while Mask matrix and RGA spectrum are known. This equation is overdetermined, thus precise solution is impossible and least-square solution is required

Process of caliration is the solution of Mask matrix while PPM's and RGA spectrums are known (requires multiple RGA measurements for linear independence, see below)




/                      \   /                      \   /                 \
| Ar_01  He_01  CO2_01 |   |                      |   | IC_01#1 IC_01#2 |
| Ar_02  He_02  CO2_02 |   | Ar__PPM#1  Ar__PPM#2 |   | IC_02#1 IC_02#2 |
| Ar_03  He_03  CO2_03 | X | He__PPM#1  He__PPM#2 | = | IC_03#1 IC_03#2 |
| Ar_04  He_04  CO2_04 |   | CO2_PPM#1  CO2_PPM#2 |   | IC_04#1 IC_04#2 |
|...                   |   |                      |   | ...             |
| Ar_50  He_50  CO2_50 |   |                      |   | IC_50#1 IC_50#2 |
\                      /   \                      /   \                 /


As seen above, the equation is scalable for multiple independent RGA measurements (#1 and #2)





        Solution of this equation for scan interpretation:










        Solution of this equation for calibration:

Calibration of RGA requires the solution of mask matrix for known PPM's and RGA scans. There are no non-ambigous ways of solving the general case of this equation, therefore, only mask entries that are known to contribute to specific peak, are used. 

In the examle below, this matrix is solved only for He_04, Ar_40 and CO2_44 parameters, since other parameters (such as He_44) are known to have value of zero:

/                      \   /                      \   /                 \
| 0      0      0      |   |                      |   | IC_01#1 IC_01#2 |
| 0      0      0      |   | Ar__PPM#1  Ar__PPM#2 |   | IC_02#1 IC_02#2 |
| 0      0      0      | X | He__PPM#1  He__PPM#2 | = | IC_03#1 IC_03#2 |
| 0      He_04  0      |   | CO2_PPM#1  CO2_PPM#2 |   | IC_04#1 IC_04#2 |
|...                   |   |                      |   | ...             |
| Ar_40  0      0      |   |                      |   | IC_40#1 IC_40#2 |
|...                   |   |                      |   | ...             |
| 0      0      CO2_44 |   |                      |   | IC_44#1 IC_44#2 |
|...                   |   |                      |   | ...             |
| 0      0      0      |   |                      |   | IC_50#1 IC_50#2 |
\                      /   \                      /   \                 /

Least-square solution for such equation may be found using optimisation methods ( determine what methods and how )