PPM calculator runs as compiled binary; inputs raw RGA scan and calibration data as CSV, outputs PPM's of the gases in mixture:

1) Initial M/Z ; M/Z step ; amount of steps ; every entry of raw RGA scan ; every calibration parameter (???) inputed as space separated floats
2) Raw RGA data is organized into array. Calibration parameters for every chemical compound are organized into array of equivalent lenght
3) Least-square solution of RGA data array as a linear combination of calibration arrays is computed.
4) Solution is normalized to PPM (such that sum of all produced values equals to 1'000'000)
5) Solutions are outputted as space separated values


this script is called every time new data entry is acquired. Outputted data is saved by Python code