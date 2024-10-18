## Dataset Structure


* **dataset**: A global folder containing all relevant datasets for tasks.

* **detex_2_0**: Subset from the previous project containing generated samples.

* **generator**: Input/Output folder for working with stable diffusion.

* **masks**: Alpha mask testing for object alignment and overlaps.

* **production**: The main folder relevant for training and evaluation of the project.

  * **setup_v1**: Deprecated and incomplete due to changes in conveyor belt setup and lighting.

  * **setup_v2**: The active dataset containing all relevant classes and subsets for training and evaluation.

* **production_mockup**: Contains subset extractions from the mockup used to evaluate YOLOS extraction performance.

* **rotation**: Train/test environment to fine-tune ViT on classification of 90-degree rotations.

    - Contains synthetic data for training and testing.

* **segmentator**: Test environment to evaluate cloth segmentation.

    - Contains samples of overlapped, crumpled cloth sets.
