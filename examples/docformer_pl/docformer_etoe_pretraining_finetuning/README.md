## This folder would consist of the plan about how to go for pretraining and finetuning of the DocFormer (base) model.


## Pretraining


### Guidelines:
- [This](https://github.com/airsplay/lxmert/blob/master/experience_in_pretraining.md) experience is helpful since there are no fixed guidelines of how to pre-train.

### Data:
- We would be using the [IDL Dataset](https://github.com/furkanbiten/idl_data) for pretraining the model.

### Task:
- The DocFormer model is trained on three tasks:
    - Masked Language Modeling (MLM)
    - Image Reconstruction (IR)
    - Image-Text Matching (ITM)

- My plan is to implement it for Masked Language Modeling (MLM), and if possible extend it to Image-Text Matching. For the Image Reconstruction part, I am not sure about the shallow decoder used for reconstruction, and hence not going through it.
- First part, is to make it work for Masked Language Modeling (MLM), and then if time permits, we can extend it to Image-Text Matching (ITM).

### Data Preprocessing:
- First, we need to download the dataset, as mentioned [here](http://datasets.cvc.uab.es/UCSF_IDL/index.txt). So, there are a lot of folders, i.e. f.tar.gz.01,02, and so on. We can choose to select one or more depending upon the size of the dataset we want to use, and the memory present in the system.
- Now, this dataset only contains the OCR, so we need to download the corresponding PDF (the information is in the JSON file). We would have the code for it so not to worry. We would make the exact structure of PDF as that of OCR.
- We now can use the Hugging Face Dataset to save the OCR from each image of the PDF. So, for each image in the PDF, we would have the corresponding OCR.
- Now, we can use the OCR and the PDF to create the dataset for MLM.

### Training:

- It can be decided later, we have frameworks for it. First, work is to make sure the data is prepared correctly.
- 



## Fine-tuning:
- Currently, my plan is to finetune the dataset on:
    - FUNSD Dataset
    - CORD Dataset


- More datasets (which we can explore):
    - RVL-CDIP (we can perform only the image part since OCRs are needed for it). Let's look at it later
    - Kleister-NDA
    - DocVQA


## Current Updates:
[x] First work is to make the data pre-processing code for the IDL Dataset.
[x] Second work is to prepare scripts to load the pre-processed data as well as, make a sample run for the DocFormer model on Masked languages modeling. 
[] Third work is to also prepare a script for doing Masked Language Modeling and Image Text Matching
[] Write the `pytorch` code for `mutli gpu` training. We can leverage tools such as `accelerate` and `PyTorch lightning`, but it would be better to write in `plain pytorch`, since that would be a good learning experience, and we would be able to debug things easily

