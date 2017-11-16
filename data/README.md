# Data Description

In total, Oregon State University’s Hatfield Marine Science Center has captured nearly 50 million plankton images over an 18-day period. This is more than 80 terabytes of data! They need your help creating an automated classification process to better understand the image contents.

For this competition, Hatfield scientists have prepared a large collection of labeled images, approximately 30k of which are provided as a training set. Each raw image was run through an automatic process to extract regions of interest, resulting in smaller images that contain a single organism/entity. You must create an algorithm that assigns class probabilities to a given image. Several characteristics of this problem make this classification difficult:

There are many different species, ranging from the smallest single-celled protists to copepods, larval fish, and larger jellies.
Representatives from each taxon can have any orientation within 3-D space.
The ocean is replete with detritus (often decomposing plant or animal matter that scientists like to call “whale snot”) and fecal pellets that have no taxonomic identification but are important in other marine processes.
Some images are so noisy or ambiguous that experts have a difficult time labeling them. Some amount of noise in the ground truth is thus inevitable.
The presence of "unknown" classes require models to handle the special cases of unidentifiable objects.


## Files

**train_images** - a folder that contains all training images.
**test_images** - a folder that contains all test images.
**train.csv** - map each image in train_images folder to its class. The labels are one-hot, meaning only 1 class is 1, the others are 0.
**label_map.txt** - map each class to its label.
**plankton_identification.pdf** - a rough guide to understand relationships between the classes. The tree-like diagram indicates morphological and biological connections between groups. Dashed lines indicate a weak(er) relationship and solid lines a stronger relationship.
**my_sample_submission.csv** - provides the appropriate format for generating a valid submission.


Classes were chosen by the Hatfield experts and represent scientifically meaningful groupings of organisms and objects (see the below FAQs). You will notice that it is possible for different classes to contain the same underlying organism. In these cases, they have been separated based on other factors of interest (e.g. one may represent an organism in motion vs. one that is still). You are permitted to use domain knowledge about the class relationships in your methodology. The official list of classes is the following:


```
acantharia_protist_big_center
acantharia_protist_halo
acantharia_protist
amphipods
appendicularian_fritillaridae
appendicularian_s_shape
appendicularian_slight_curve
appendicularian_straight
artifacts_edge
artifacts
chaetognath_non_sagitta
chaetognath_other
chaetognath_sagitta
chordate_type1
copepod_calanoid_eggs
copepod_calanoid_eucalanus
copepod_calanoid_flatheads
copepod_calanoid_frillyAntennae
copepod_calanoid_large_side_antennatucked
copepod_calanoid_large
copepod_calanoid_octomoms
copepod_calanoid_small_longantennae
copepod_calanoid
copepod_cyclopoid_copilia
copepod_cyclopoid_oithona_eggs
copepod_cyclopoid_oithona
copepod_other
crustacean_other
ctenophore_cestid
ctenophore_cydippid_no_tentacles
ctenophore_cydippid_tentacles
ctenophore_lobate
decapods
detritus_blob
detritus_filamentous
detritus_other
diatom_chain_string
diatom_chain_tube
echinoderm_larva_pluteus_brittlestar
echinoderm_larva_pluteus_early
echinoderm_larva_pluteus_typeC
echinoderm_larva_pluteus_urchin
echinoderm_larva_seastar_bipinnaria
echinoderm_larva_seastar_brachiolaria
echinoderm_seacucumber_auricularia_larva
echinopluteus
ephyra
euphausiids_young
euphausiids
fecal_pellet
fish_larvae_deep_body
fish_larvae_leptocephali
fish_larvae_medium_body
fish_larvae_myctophids
fish_larvae_thin_body
fish_larvae_very_thin_body
heteropod
hydromedusae_aglaura
hydromedusae_bell_and_tentacles
hydromedusae_h15
hydromedusae_haliscera_small_sideview
hydromedusae_haliscera
hydromedusae_liriope
hydromedusae_narco_dark
hydromedusae_narco_young
hydromedusae_narcomedusae
hydromedusae_other
hydromedusae_partial_dark
hydromedusae_shapeA_sideview_small
hydromedusae_shapeA
hydromedusae_shapeB
hydromedusae_sideview_big
hydromedusae_solmaris
hydromedusae_solmundella
hydromedusae_typeD_bell_and_tentacles
hydromedusae_typeD
hydromedusae_typeE
hydromedusae_typeF
invertebrate_larvae_other_A
invertebrate_larvae_other_B
jellies_tentacles
polychaete
protist_dark_center
protist_fuzzy_olive
protist_noctiluca
protist_other
protist_star
pteropod_butterfly
pteropod_theco_dev_seq
pteropod_triangle
radiolarian_chain
radiolarian_colony
shrimp_caridean
shrimp_sergestidae
shrimp_zoea
shrimp-like_other
siphonophore_calycophoran_abylidae
siphonophore_calycophoran_rocketship_adult
siphonophore_calycophoran_rocketship_young
siphonophore_calycophoran_sphaeronectes_stem
siphonophore_calycophoran_sphaeronectes_young
siphonophore_calycophoran_sphaeronectes
siphonophore_other_parts
siphonophore_partial
siphonophore_physonect_young
siphonophore_physonect
stomatopod
tornaria_acorn_worm_larvae
trichodesmium_bowtie
trichodesmium_multiple
trichodesmium_puff
trichodesmium_tuft
trochophore_larvae
tunicate_doliolid_nurse
tunicate_doliolid
tunicate_partial
tunicate_salp_chains
tunicate_salp
unknown_blobs_and_smudges
unknown_sticks
unknown_unclassified
```

# Frequently Asked Questions
_written by Jessica Luo, PhD Candidate, Hatfield Marine Science Center_

##### Q. How did you collect the images?

We collected the images between May-June 2014 in the Straits of Florida using the In Situ Ichthyoplankton Imaging System (ISIIS), a towed, underwater imaging system using shadowgraph imagery with a line-scan camera.

A high-resolution continuous image is parsed into 2048 x 2048 pixel frames, which were corrected using flat-fielding. Frames were then thresholded and segmented into regions of interest (ROIs). These ROI segments are the images provided for this competition.

We made every effort to include a representation of real world data in this dataset. In other words, we did not cherry-pick for the best and clearest images, but used images spanning the gamut from blurry to clear, and tiny to big.

##### Q. Do organisms appear smaller if they are further away from the camera?

No. Because of the shadowgraph imagery technique, organisms will be the same size regardless of distance to the camera.

##### Q. Can you explain why you would get partial images of organisms then?

Partial images in our dataset occur due to imperfect segmentation. If an organism is highly transparent (like a jellyfish), then sometimes the thresholding and segmentation process will cut off part of the image. This is fairly rare; typically our segmentation process works very well.

##### Q. Are there relationships between the categories?

Yes, there are relationships between the categories. Some of the relationships are taxonomic, some are behavioral / ecological, and some are based on shape. We diagrammed all of these relationships in the plankton relationships document, which can be accessed along with the dataset. Red boxes indicate our categories, blue boxes indicate major groups, solid lines indicate direct relationships, and dashed lines indicate minor relationships or shape similarities.

##### Q. Why are there non-taxonomic distinctions in categories?

In some cases, we chose to partition organisms into different categories based on shape. For example, in the appendicularians, the shape indicates a behavior (tail beating). Furthermore, appendicularians are often confused with a whole host of other things - most notably, fish larvae - so we have traditionally separated them out by shape to increase classification accuracy.

##### Q. Are these classifications reliable?

We have a trained team and have cross-validated the classifications, such that certain images were checked by up to five people. That said, there is an intrinsic amount of variability in classifying ambiguous images. For example, Culverhouse et al. (2003) found that experts are able to maintain 84-95% self-consistency in labeling difficult images. A spot check on the self-consistency in this dataset was on the high end of that range. We believe that this is the best possible dataset of these kinds of plankton images currently in existence.

_Citation: PF Culverhouse, Williams R, Reguera B, Herry V, González-Gil S. (2003) "Do experts make mistakes? A comparison of human and machine identification of dinoflagellates." Mar. Ecol. Prog. Ser. 247:17-25._