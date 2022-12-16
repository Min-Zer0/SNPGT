# ___WinSNPGT: Genotyping of specified SNP sites on windows system___

## 💡 General Introduction
The rapid development of sequencing technology and dramatic drop in the cost have led to the generation of massive amounts of data. However, most of the raw data are analyzed on linux systems, and the process of generating variant loci information from sequencing data is a challenge for researchers unfamiliar with linux systems. We have developed a small program to call variant loci on the windows system, WinSNPGT. It can obtain the genotypes of the raw sequencing data for the snp loci specified in our datasets. The installation and use of this program is described below.

## 📘 Table of Contents

- Background
- Change Log
- Data
- Installation
- Usage
- Frequently Asked Questions
- Contacts

## 🧾 Background
We have developed a phenotype prediction platform, **[CropGStools](http://iagr.genomics.cn/)**, which contains multiple high-quality datasets from important crops such as rice, maize and so on. These datasets were used as training sets to build models for phenotype prediction. Users can upload genotypes of their own samples to the platform for online phenotype prediction.

The WinSNPGT program was developed to ensure that the genotypes uploaded by users match those in the training set for modeling so that bias in the prediction results can be avoided. Users can run this program on the windows system to realize the whole process from sequencing files to getting genotypes by simple operation, which is very friendly for people who have little experience in linux operation.

## 🔍 Change Log
- [Version 1.0](https://github.com/JessieChen7/WinSNPGT) -First version released on January, 1st, 2023


## 🔍 Data
The example-data files are not included in the release package, you can download [example-data.tar.gz](https://github.com/JessieChen7/WinSNPGT/archive/refs/heads/example-data.tar.gz) and extract data with command `tar zxvf example-data.tar.gz`.


## 🌟 Installation
Download the [release package](https://github.com/JessieChen7/WinSNPGT/archive/refs/heads/main.zip) and unzip to your working directory.

## 🌟 Usage
There are three subfolders and two files after the package is unziped.

- **Input_Fastq**
- **Reference_Genome**
- **sys**
- `start.bat`
- `start`

To run WinSNPGT locally, you need to run the main program via `start.bat` and then visualize your operation on the `start` local web platform.

Here are the running steps:

1. Double-click to run the program `start.bat`
2. Double click to open `start`
	1. Select the species of your samples to be genotyped
	2. Select the dataset corresponding to the model to be fitted
		- After this step, the web page will provide a download link to the dataset files. Follow the instructions to download the file  `(*.tar.gz)` and move it to the path: **. /Reference_Genome** 
3. Click Verification file
4. Follow the instructions to move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **. /Input_Fastq**
5. Click Confirm
6. Enter your project name which will be output file prefix
7. Select the corresponding reads files and enter the sample name
8. If there are another samples to be genotyped, you can choose *Add more samples*
9. After adding all samples to be genotyped and confirm the form is correct, you can choose *Finish adding samples*
10. Enter the number of threads available to run the program

The output format is like:

\#CHROM|POS|Line1|Line2
---|---|---|---
1|1077|T|T
1|12127|G|G
...|...|...|...
10|1299332|T|A
10|1299513|G|G
...|...|...|...

---
The following step-by-step notes may help you more clearly understand the use of the program:

\### step 1~2：Double-click to run the program `start.bat` and `start`
![step1](https://github.com/JessieChen7/Image/blob/main/step1.png)

\### step 3: Select the species of your samples to be genotyped
![step2](https://github.com/JessieChen7/Image/blob/main/step2.png)

\### step 4: Select the dataset corresponding to the model to be fitted
![step3](https://github.com/JessieChen7/Image/blob/main/step3.png)

\### step 5: Download the file  `(*.tar.gz)` 
![step4](https://github.com/JessieChen7/Image/blob/main/step4.png)

\### step 6: Move the download file to the path: **. /Reference_Genome** 
![step5](https://github.com/JessieChen7/Image/blob/main/step5.png)

\### step 7: Verify the downloaded files
![step6](https://github.com/JessieChen7/Image/blob/main/step6.png)

\### step 8: Move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **. /Input_Fastq**
![step7](https://github.com/JessieChen7/Image/blob/main/step7.png)

\### step 9: Verify your raw sequencing data `(*.fastq.gz)` or `(*.fastq)`
![step8](https://github.com/JessieChen7/Image/blob/main/step8.png)

\### step 10: Enter your project name which will be output file prefix
![step9](https://github.com/JessieChen7/Image/blob/main/step9.png)

\### step 11~13: Select the corresponding reads files and enter the sample name
![step10](https://github.com/JessieChen7/Image/blob/main/step10.png)

\### step 14: If there are another samples to be genotyped, you can choose *Add more samples*
![step11](https://github.com/JessieChen7/Image/blob/main/step11.png)

\### step 15: After adding all samples to be genotyped and confirm the form is correct, you can choose *Finish adding samples*
![step12](https://github.com/JessieChen7/Image/blob/main/step12.png)

\### step 16: Enter the number of threads available to run the program
![step13](https://github.com/JessieChen7/Image/blob/main/step13.png)

\### step 17: Run the program
![step14](https://github.com/JessieChen7/Image/blob/main/step14.png)

\### step 18: Get the results
![step15](https://github.com/JessieChen7/Image/blob/main/step15.png)


## 💡 Frequently Asked Questions


## 👥 Contacts
Jie Qiu (qiujie@shnu.edu.cn)  
Min Zhu (1185643615@qq.com)  
Jiaxin Chen (jxchen1217@gmail.com)
