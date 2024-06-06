Requirements
Python 3.x
Required Python libraries: numpy, scipy, scikit-learn, matplotlib, gdal, imageio

Test Dataset : 
	Downloaded automatically in code, no seperate file required

Prerequisite:
	Create a "result" folder in you present working directory


Usage
Binary Change Map Generator:

Import required libraries: matplotlib, numpy, scipy, scikit-learn.
Call get_binary_change_map(data, method) with your data and chosen method ('k_means' or 'otsu').
Change Map Assessment:

Import required libraries: imageio, numpy.
Call assess_accuracy(gt_changed, gt_unchanged, changed_map, multi_class=False) with ground truth and change map data.
Set multi_class=True if dealing with multi-class classification.
Image Processing Utilities:

Import the module: import image_processing_utils as ipu.
Call the desired function for image normalization and patch selection.
KernelPCANet:

Import the class: from KernelPCANet import KernelPCANet.
Initialize the network: net = KernelPCANet(num_stages, patch_size, num_filters, gamma).
Train the network: net.train_net(input_data, stage, is_mean_removal, kernel='rbf').
Infer data: output_data = net.infer_data(input_data, stage, is_mean_removal).
Change Detection with KPCAMNet:

Set parameters in the provided dictionary or pass them through command-line arguments.
Run the script: python change_detection_kpcamnet.py.
Output
Binary change map: KPCAMNet_BCM.png
Multi-class change map: KPCAMNet_MCM.png