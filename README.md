Welcome to Urania Sampling system



To configure on Ubuntu/Zorin:

1) Install <code>git, python3, pip</code> via <code>apt</code>
2) install <code>root-framework</code> via <code>snap</code>

3) Install packages specified in <code>pip_requirements.txt</code> system-wide via pip using root priviledges. Use flags s.a. <code>--break-system-packages</code> if required

4) Compile ROOT code into binaries by typing <code>g++ spectre_to_ppm_converter_th1d_fit.C $(root-config --glibs --cflags --libs) -o spectre_to_ppm_converter</code>

5) Shall <code>Main Config Not Found</code> error arise, copy <code>DefaultMainConfig</code> and rename copy to <code>MainConfig</code>; or just do it preliminary

6) Specify absolute path to this directory in <code>MainConfig</code> file cwd entry



To start frontend type: <code>sudo streamlit run main.py</code>

To start sampling process(runs independent of frontend), type  <code>sudo python3 StartSampling.py</code>