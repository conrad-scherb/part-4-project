# Visualisation & Model Analysis Tools

Install dependencies with `pip3 tensorflow pathint numpy matplotlib` before running any of these scripts.

#### `check-result.py`

Loads a model saved to disk with specified `MODEL_PATH`, and prints the classification output on a single image with path `IMAGE_PATH`.

#### `full-visualisation.py`

Plots the convolutional kernels of the specified `conv_2d` layer `LAYER_NAME` for the provided `MODEL_PATH`, then convolves each of those filters with the provided images in `IMAGE_LIST`, useful for visualising how the convolutional kernel responds to signal versus no signal images, as well as detecting potential orientation sensitivity. Very difficult to visualise more than 16 kernels this way; use python slices on line 23 to choose exactly which window of filters to visualise.

#### `get-bias.py`

Returns the bias of a specified layer type for a specified `MODEL_PATH`.

#### `test-model.py`

Runs the specified `MODEL_PATH` on a dataset categorised with Signal and No Signal subfolders with `DATASET_PATH`. Useful for running extra validation on unfamiliar data, such as horizontal or diagonal texture boundary images.

#### `legacy/*.py`

Old visualisation tools that were eventually rolled into `full-visualisation`, but may still be useful.
