# Filter-Rectify Filter Model

## FRF
Filter-rectify filter is a 3 step process and a secondary image processing technique which involves filtering, the addition of a recitfication to normalise filter output then a final filtering as a output classifier.

- Filter step 1: a variety of filters exist at different orientations and receptive field sizes (n.b. only 1 receptive field size is used for the purpose of this reearch), and are all applied to the image producing positive and negative responses for each receptive field location along the image.
- Rectification step: the output from filter 1 is normalised in order to make sure a strong positive result is achieved if the receptive field matches up perfectly or opositely and no results is produced otherwise. This is because a the filter matches a dark and a light spot to find a boundary. In the case of a vertical filter with black on LHS and white on RHS, a input receptive field w/ white LHS and black RHS will give a negative result, where in fact the orientation is the same and should be counted as a positive match.
- Filter step 2: The rectified outputs are passed to a second filter which detects the global orientation based on the output from rectified filter - no rectification after is required becasue it is only interested in finding the appropriate texture boundary between high and low rectified outputs.

## How our model relates to FRF


## References: 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3094179/
https://www.researchgate.net/publication/10801661_Mechanism_independence_for_texture-modulation_detection_is_consistent_with_a_filter-rectify-filter_mechanism