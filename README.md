# ___WinSNPGT: Genotyping of specified SNP sites on Windows system___

## 📢 News
winSNPGT version 2.0 has been successfully released, more friendly and convenient, welcome to use!

Click the [here](https://github.com/Min-Zer0/WinSNPGT) to jump
## 🧰 Relevant Software
**[LinSNPGT](https://github.com/JessieChen7/LinSNPGT)**: Genotyping of specified SNP sites on Linux system

## 👉 Latest [release package](https://github.com/JessieChen7/WinSNPGT/raw/installation_package/WinSNPGT.exe)

## 💡 General Introduction
The rapid development of sequencing technology and dramatic drop in the cost have led to the generation of massive amounts of data. However, most of the raw data are analyzed on linux systems, and the process of generating variant loci information from sequencing data is a challenge for researchers unfamiliar with linux systems. We have developed a toolkit to call variant loci on the windows system, WinSNPGT. It can obtain the genotypes of the raw sequencing data for the snp loci specified in our datasets. The installation and use of this toolkit is described below.

## 📘 Table of Contents

- Background
- Change Log
- Data
- Installation
- Usage
- Frequently Asked Questions
- Contacts

## 🧾 Background
We have developed a phenotype prediction platform, **[CropGS-Hub](https://iagr.genomics.cn/CropGS/#/)**, which contains multiple high-quality datasets from important crops such as rice, maize and so on. These datasets were used as training sets to build models for phenotype prediction. Users can upload genotypes of their own samples to the platform for online phenotype prediction.

The WinSNPGT toolkit was developed to ensure that the genotypes uploaded by users match those in the training set for modeling so that bias in the prediction results can be avoided. Users can run this program on the windows system to realize the whole process from sequencing files to getting genotypes by simple operation, which is very friendly for people who have little experience in linux operation.

## 🔍 Change Log
- [Version 1.0](https://github.com/JessieChen7/WinSNPGT) -First version released on June, 1st, 2023
- [Version 2.0](https://github.com/Min-Zer0/WinSNPGT) - Second version released on August, 24th, 2023

## 🔍 Data
- The example-data files are not included in the release package, you can download [example-data.tar.gz](https://figshare.com/articles/dataset/WinSNPGT_example_data/23365061).

	The species of the example-data files is *Oryza sativa*, you can select the rice-related dataset in the toolkit to complete the genotyping.

- Java8 are not included in the release package, You can install it yourself by referring to the method in Installation.

## 🌟 Installation
- Download the [release package](https://github.com/JessieChen7/WinSNPGT/raw/installation_package/WinSNPGT.exe) and unzip to your working directory.
- Download and install [jdk-8u381-windows-x64.exe](https://www.oracle.com/java/technologies/downloads/#java8-windows).
  
## 🌟 Usage
There are three subfolders and two files after the package is unziped.

- **00.Make_RefGenome**
- **01.Reference_Genome**
- **02.Input_Fastq**
- `SNPGT-bulid`
- `WinSNPGT`

P.S.：If your system is set to show hidden items, there is also a hidden subfolder **sys**

To run WinSNPGT locally, you need to run the main program via `WinSNPGT` and then visualize your operation on the default browser.

Here are the running steps:

1. Double-click to run the program `WinSNPGT`
2. Select the species of your samples to be genotyped
3. Select the dataset corresponding to the model to be fitted
	- After this step, the web page will provide a download link to the dataset files. Follow the instructions to download the file  `(*.tar.gz)` and move it to the path: **./01.Reference_Genome** 
4. Click *Verify file*
5. Select the way to read raw reads files 
6. Follow the instructions to move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **./02.Input_Fastq**
	- if you select the way of reading excel table, you need to fill the `Sample.table.xls` in  **./02.Input_Fastq**
7. Click *Confirm*
	- if you select the way of reading excel table, you can skip to step 12 after clicking *Confirm* 
8. Enter your project name which will be output file prefix
9. Select the corresponding reads files and enter the sample name
10. If there are another samples to be genotyped, you can choose *Yes*
11. After adding all samples to be genotyped and confirm the form is correct, you can choose *Finish adding samples*
12. Enter the number of threads available to run the program

The output format is like:

\#CHROM|POS|Line1
---|---|---
Chr1|128960|A
Chr1|133137|C
...|...|...
Chr12|321216|A
Chr12|364257|A
Chr12|364755|.
...|...|...

---
The following step-by-step notes may help you more clearly understand the use of the program:

\### **step 1**: Install WinSNPGT  
![step0_Install](https://github.com/JessieChen7/Image/blob/main/step0_Install.png)

After the installation a WinSNPGT folder will be created and a welcome interface will pop up.

![step1_cd](https://github.com/JessieChen7/Image/blob/main/step1_cd.png)

\### **step 2**：Double-click to run the program `WinSNPGT`  
![step2_runWinSNPGT](https://github.com/JessieChen7/Image/blob/main/step2_runWinSNPGT.png)  
When the program starts running, a web pop-up will appear in the default browser and there will also be a window running as a background program, do not close it.

![step3_program](https://github.com/JessieChen7/Image/blob/main/step3_program.png)

\### **step 3**: Select the species of your samples to be genotyped  
![step4_select_species](https://github.com/JessieChen7/Image/blob/main/step4_select_species.png)

\### **step 4**: Select the dataset corresponding to the model to be fitted  
![step5_select_the_dataset](https://github.com/JessieChen7/Image/blob/main/step5_select_the_dataset.png)

\### **step 5**: Download the file  `(*.tar.gz)`   
![step6_download_RG](https://github.com/JessieChen7/Image/blob/main/step6_download_RG.png)

\### **step 6**: Move the downloaded file to the path: **./01.Reference_Genome**  
![step7_move_RG](https://github.com/JessieChen7/Image/blob/main/step7_move_RG.png)

\### **step 7**: Verify the downloaded files  
![step8_verify_RG](https://github.com/JessieChen7/Image/blob/main/step8_verify_RG.png)

Only if there are no errors in the downloaded files, an alert box will appear like this, click anywhere to continue.

![Condition1_verify_RG_OK](https://github.com/JessieChen7/Image/blob/main/Condition1_verify_RG_OK.png)

\### **step 8**: Select the way to read raw reads files  
Users can choose the way to manually select raw reads files in the interface.

![step9_manually_select](https://github.com/JessieChen7/Image/blob/main/step9_manually_select.png)

Or choose to automatically read raw reads files after filling table, which is recommended when there are many samples.

![step9_auto_excel](https://github.com/JessieChen7/Image/blob/main/step9_auto_excel.png)

\### **step 9**: Move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **./02.Input_Fastq**
![step10_move_fastq](https://github.com/JessieChen7/Image/blob/main/step10_move_fastq.png)

If the way of reading excel table has been chosen, the `Sample.table.xls` need to be filled.

![step10_fill_excel](https://github.com/JessieChen7/Image/blob/main/step10_fill_excel.png)

\### **step 10**: Verify your raw sequencing data `(*.fastq.gz)` or `(*.fastq)`
![step11_confirm_manually](https://github.com/JessieChen7/Image/blob/main/step11_confirm_manually.png)

![step11_confirm_auto](https://github.com/JessieChen7/Image/blob/main/step11_confirm_auto.png)

Only if there are no errors in the files, the interface will look like this: 

![Condition2_verify_fastq_OK](https://github.com/JessieChen7/Image/blob/main/Condition2_verify_fastq_OK.png)

If the way of reading excel table has been chosen, you can directly skip to step15.

\### **step 11**: Enter your project name which will be output file prefix
![step12_project_name](https://github.com/JessieChen7/Image/blob/main/step12_project_name.png)

\### **step 12**: Select the corresponding reads files and enter the sample name
![step13_reads](https://github.com/JessieChen7/Image/blob/main/step13_reads.png)

\### **step 13**: If there are another samples to be genotyped, you can choose *Yes* and repeat the step 12
![step14_adding](https://github.com/JessieChen7/Image/blob/main/step14_adding.png)

\### **step 14**: After adding all samples to be genotyped and confirm the form is correct, you can choose *Finish adding samples*
![step15_finish_adding](https://github.com/JessieChen7/Image/blob/main/step15_finish_adding.png)

\### **step 15**: Enter the number of threads available to run the program
![step16_threads](https://github.com/JessieChen7/Image/blob/main/step16_threads.png)

\### **step 16**: Run the program
![step17_run](https://github.com/JessieChen7/Image/blob/main/step17_run.png)

\### **step 17**: Get the results
![Condition3_Done](https://github.com/JessieChen7/Image/blob/main/Condition3_Done.png)



## 💡 Frequently Asked Questions
If there are some errors reported during the running of the program, please refer to the following scenarios to solve the problem:

1. Only **English** is allowed in the **path where winSNPGT is installed**.
2. When you start the program for the first time, the web interface may fail to open. This is because the background program has not yet been refreshed. If the background program cannot be started for a long time, you can try to **close the background and foreground programs and restart `WinSNPGT`**.
3. During the running of winSNPGT, the **background program is not allowed to be closed**.
4. If you chose the way to read excel table, you must **save and close the table after filling it**, which means it cannot be kept open.
5. If you fill in the wrong information on the web page, you can **refresh and refill it before clicking the *Run* button**, and there is no need to repeat moving files steps.

The above are some possible causes of errors, if there are any other problems, welcome to contact us.

## 👥 Contacts
Jie Qiu (qiujie@shnu.edu.cn)  
Min Zhu (Zer0Min@outlook.com)  
Jiaxin (jxchen1217@gmail.com)


