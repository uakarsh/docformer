## This folder would consist of the plan about how to go for pretraining and finetuning of DocFormer (base) model.


## Pretraining

### Data:
- We would be using the [IDL Dataset](https://github.com/furkanbiten/idl_data) for pretraining the model.

### Task:
- The DocFormer model is trained on three tasks:
    - Masked Language Modeling (MLM)
    - Image Reconstruction (IR)
    - Image-Text Matching (ITM)

- My plan is to implement it for Masked Language Modeling (MLM), and if possible extend it to Image-Text Matching. For Image Reconstruction part, I am not sure about the shallow decoder used for reconstruction, and hence not going through it.
- First part, is to just make it work for Masked Language Modeling (MLM), and then if time permits, we can extend it to Image-Text Matching (ITM).

### Data Preprocessing:
- Firstly, we need to download the dataset, and as mentioned [here](http://datasets.cvc.uab.es/UCSF_IDL/index.txt). So, there are a lot of folders, i.e f.tar.gz.01,02 and so on. We can choose to select one or more depending upon the size of the dataset we want to use, and the memory present in the system.
- Now, this dataset only contains the OCR, so we need to download the corresponding PDF (the information is in the json file). We would have the code for it so not to worry. We would make the same structure of PDF as that of OCR.
- We now can use the Hugging Face Dataset to create the OCR from each image of the PDF. So, for each image in the PDF, we would have the corresponding OCR.
- Now, we can use the OCR and the PDF to create the dataset for MLM.

### Training:





## Fine-tuning:
- Currently, my plan is to finetune the dataset on:
    - FUNSD Dataset
    - CORD Dataset


- More datasets (which we can explore):
    - RVL-CDIP (we can perform only the image part, since OCRs are needed for it). Let's look it later
    - Kleister-NDA
    - DocVQA


## Current Updates:
- First work is to make the data pre-processing code for the IDL Dataset. So, would be working on it.

