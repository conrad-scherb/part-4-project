# Investigating the fitted filters on trained CNNs

## Methodology
File used: `/visualisation/visualise.py`
In order to look at the response of the filters visually, the filters were extracted from a saved tf model and ran on a single input image and the output was displayed, simulating the response of just the convolutional layer in the image. 

## Observations

We observed that in the large neuron models such as 32-neuron, there were a large number of filters that produced no output as seen in the image below. This led us to experiment with massively reducing the number of filters in our CNNs.

![](./images/32Neuron.png)

Significantly reducing the number of neurons in the first convolutional layer resulted in the decrease of accuracy, dropping to 89% accuracy on a 1-neuron layer 1 neural network with 13 kernel size.. This follows as the amount of feature detector neurons and fitted convolutional filters were reduced, so orientation of regions could not be as well determined. 

![](./images/1NeuronNoSignal.png)
Above: 1 neuron, 13 kernel size with no signal present.

![](./images/1NeuronSignal.png)
Above: 1 neuron, 13 kernel size with  signal present.

`Kernel`

`[[-8.97756591e-03  1.55058429e-02 -8.32149610e-02  1.55812845e-01
   4.55478311e-01  4.95989740e-01  2.58672647e-02 -8.79151896e-02
   1.07538730e-01 -2.27247015e-01  1.71850979e-01 -4.32007574e-02
  -1.38617888e-01]
 [-3.80978622e-02  8.07908177e-02  8.67011026e-02 -3.29457000e-02
   9.77606103e-02  5.33472359e-01  1.11447535e-01  3.10454637e-01
  -1.06157400e-01 -5.85062504e-01 -9.35233012e-02  4.30010594e-02
  -1.07433088e-01]
 [-5.07752560e-02  8.97568688e-02 -1.17114842e-01 -3.28525484e-01
  -4.09272134e-01  1.49530277e-01  3.90848041e-01  5.46821356e-01
  -1.64310142e-01 -6.11174583e-01 -9.13499966e-02  1.35095224e-01
  -5.38935028e-02]
 [ 7.47253969e-02 -4.02817167e-02 -1.19064011e-01 -2.00598985e-01
  -3.14657480e-01 -1.58285558e-01  4.34618071e-02 -1.26926405e-02
   1.30652204e-01 -1.81097284e-01 -1.04970396e-01 -2.90442202e-02
  -2.11693390e-04]
 [ 3.09696317e-01 -1.84447024e-04  1.54963940e-01  1.75265551e-01
  -5.28170727e-02 -1.09681785e-01 -2.99254358e-01 -2.60618508e-01
   2.13551491e-01  9.59769357e-04 -3.06039900e-01 -1.20350726e-01
  -1.78762138e-01]
 [-6.14276864e-02 -4.06331539e-01 -1.59323424e-01  1.55527711e-01
   6.36087283e-02 -2.65951231e-02 -6.28181770e-02 -1.52006567e-01
  -5.94837293e-02  2.46992726e-02 -1.08034886e-01  2.90127575e-01
   2.11285055e-01]
 [-3.92557591e-01 -5.21516442e-01 -3.56687248e-01 -4.35493663e-02
   7.40447789e-02  3.25749032e-02  2.46633776e-03 -3.90275419e-02
   5.01952022e-02 -2.08751708e-02  1.92487687e-01  4.02427018e-01
   5.64674377e-01]
 [ 2.43196008e-03 -4.21993464e-01 -2.70546794e-01  4.82308082e-02
  -5.08797131e-02  6.74525723e-02  6.87263310e-02  8.20616186e-02
   3.69524732e-02  1.09384861e-02 -1.69122502e-01  6.14483766e-02
   5.38559735e-01]
 [ 7.80062750e-02 -4.37524736e-01 -4.27637458e-01 -6.23613596e-02
   1.14965372e-01 -3.27474438e-02  1.04603181e-02 -4.69869375e-03
   1.14528403e-01  5.45761175e-02 -2.51344472e-01  1.79984458e-02
   6.80038512e-01]
 [-3.25077891e-01 -5.91769338e-01 -4.00532514e-01  4.02531736e-02
  -1.17124684e-01 -2.96448201e-01 -2.81429756e-02  1.19720131e-01
   3.76060307e-02 -1.03977457e-01  1.25954643e-01  4.08424258e-01
   5.31226516e-01]
 [-6.43892884e-01 -3.83000582e-01  2.12922782e-01 -1.34355620e-01
  -3.96241069e-01 -1.91631779e-01  1.39002457e-01  2.83041626e-01
  -7.91283604e-03 -1.80241819e-02  2.71063149e-01  5.80143154e-01
   1.29836917e-01]
 [-2.08569080e-01  1.29138365e-01  1.13554023e-01 -4.93127376e-01
  -2.83116519e-01  4.98594910e-01  2.97852814e-01 -4.70696203e-02
  -7.46863261e-02 -2.26163551e-01 -4.76296518e-05  6.03113212e-02
  -2.92290092e-01]
 [ 2.74805784e-01  2.78201520e-01 -7.81166926e-02  9.19924974e-02
   6.12828910e-01  5.30178666e-01 -2.00741813e-01 -9.13375735e-01
  -5.26873648e-01 -4.11996812e-01 -1.24784328e-01 -2.21676882e-02
  -1.07234605e-01]]`


  ## Investigating bias
  As we only had a single convolutional neuron, the bias for our convolutional layer out was -0.028. Summing this value with the convolutional out, then is flattened and summed into a single value that is then passed to the sigmoidal classifier of the final output neuron with weight 0.138. This means we would expect a greater total intensity of pixels from the signal case, which can be seen from visually inspecting the image.

  ## What does the fitted kernel actually do

