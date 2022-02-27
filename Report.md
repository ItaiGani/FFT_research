# Guesser algorithm report

The purpose of the algorithm is to take a wav file and return a graph of time × frequency × amplitude.

## Details

 - **The base code**, the code divides the file into windows in witch it's preforming fourier analysis  
`np.abs(np.fft.rfft(signal[window:next_window:]))`  
to get the amplitude of each frequency.
 - **Musical tones**, as was written in the hw file "The human ear doesn’t know to distinguish tones with small differences (measured by ratios). In what follows we assume that beyond 1/16 of a tone, the human ear can not distinguish between two different musical tones." so the objective was to round all the frequencies it was achived by <p align="center"> <img src="https://render.githubusercontent.com/render/math?math=\text{freq[i]}=440\cdot2^{\left(\frac{\text{round}\left(48\cdot\log_{2}\left(\frac{\text{freq[i]}}{440}\right)\right)}{48}\right)}"> </p> where `freq[i]` is the i-th frequency.
 - **first guesser⁽¹⁾**, for reducing the time it takes the code to run we can save the heavy coefficients in the first window and then instead of computing the fourier transform every window we check if the window is similar to the first window (because we already calculated the fourier transform of that window), for computing if the windows are similar we would want to use the 2-norm on the difference between the windows <p align="center"> <img src="https://render.githubusercontent.com/render/math?math=\left\Vert b_{i}\left(x\right)-b_{1}\left(x\right)\right\Vert _{2}<\alpha"> </p> (where `b_i(x)` is the i-th window) then if the statement is true we just use the fourier transform of the first window, else we compute the fourier transform of the window.
 - **second guesser⁽¹⁾**, instead of comparing everything with the first window we compare with the last window <p align="center"> <img src="https://render.githubusercontent.com/render/math?math=\left\Vert b_{i}\left(x\right)-b_{i-1}\left(x\right)\right\Vert _{2}<\alpha"> </p>  

⁽¹⁾ instead of computing the heavy coefficient of the windows we can just use the fact we have the original windows to compare the windows.
