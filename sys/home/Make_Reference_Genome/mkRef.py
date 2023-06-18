import os
import sys
import time

Section_len_half = 200

def Getwd():
	for line in open('../install_dir'):
	    chr_dir = line
	dir_list = chr_dir[1:].split("\\")[:-1]
	Path = "/cygdrive/" + dir_list[0][:-1] + "/"
	for i in range(len(dir_list)-1):
		Path = Path+'"'+dir_list[i+1]+'"'+"/"
	return Path

def CheckConfig(content):
    for char in content:
        if not char.isalnum() and not char.isspace():
            return True
    return False

def ReadConfig():
	file_path = os.path.join("../Reference_Genome", "config.txt")
	if os.path.exists(file_path):
		os.system('cat %s00.Make_RefGenome/config.txt >> ../Reference_Genome/config.txt  '%(Getwd()))
	else:
		os.system('cp %s00.Make_RefGenome/config.txt ../Reference_Genome/config.txt  '%(Getwd()))
	with open('./config.txt', 'r') as f:
		Config_info = f.readlines()
		spec,line_type = "",""
		for info in Config_info:
			if ">>" in info:
				spec = info[2:].replace(" ", "").replace("\t", "",).replace("\n", "",)
			elif ">" in info:
				line_type = info[1:].replace(" ", "").replace("\t", "").replace("\n", "",)
		return spec,line_type

def SplitRef(Ref_file, Chr_list):
    os.system("mkdir ./Chr_fa")
    for ChrNum in Chr_list:
        os.system("/tools/samtools-1.16.1/samtools.exe faidx %s %s > ./Chr_fa/%s.fasta" % (Ref_file, ChrNum, ChrNum))
        os.system("awk '{print $1,$2}' %s.fai > ./lengths.txt" % (Ref_file))

def Find_SNP_Section(Chr_intervals, Section_len_half, Chr_len):
    SNP_section = []
    for SNP_pos in Chr_intervals:
        if SNP_pos < Section_len_half:
            section = [0, SNP_pos + Section_len_half]
            SNP_section.append(section)
        elif SNP_pos + Section_len_half > Chr_len:
            section = [SNP_pos - Section_len_half, Chr_len]
            SNP_section.append(section)
        else:
            section = [SNP_pos - Section_len_half, SNP_pos + Section_len_half]
            SNP_section.append(section)
    return SNP_section

def merge_ranges(ranges):
    sorted_ranges = sorted(ranges)
    merged_ranges = []
    for start, end in sorted_ranges:
        if merged_ranges and start <= merged_ranges[-1][1]:
            merged_ranges[-1] = (merged_ranges[-1][0], max(end, merged_ranges[-1][1]))
        else:
            merged_ranges.append((start, end))
    return merged_ranges

def Movefile():
	spec_line =  ReadConfig()
	os.system('mv -f %s00.Make_RefGenome/* ./  '%(Getwd()))
	ori_document = ["picard.jar","mkRef.py","README.txt","config.txt"]
	now_document = []
	for fasta_bim in os.listdir("./"):
		now_document.append(fasta_bim)
	if len(list(set(now_document)-set(ori_document))) ==2:
		os.system('gunzip ./* >/dev/null 2>&1 &')
		Ref = ""
		for file_name in os.listdir("./"):
			if ".fa" in file_name or ".fasta" in file_name:
				Ref = file_name
		os.system("cp ./%s %s.fasta" %(Ref, spec_line[0]))
		os.system("mv ./%s %s00.Make_RefGenome/" %(Ref, Getwd()))
		return spec_line
	else:
		error_document = list(set(now_document)-set(ori_document))+["config.txt"]
		document_str = ' '.join([str(elem) for elem in error_document])
		os.system("mv %s  %s00.Make_RefGenome/" %(document_str,Getwd()))
		print("\n"+70*"-"+"\nInput file Error !\nPlease check files *.fasta/*.gz and *.bim in 00.Make_RefGenome/")
		sys.exit()
def MakeREF(spec_line):
	os.system("awk '{position=$1\":\"$4\"-\"$4;print position}' \
			./*.bim > %s.intervals" %(spec_line[1]))

	Ref_file = spec_line[0]+".fasta"
	intervals_file = "%s.intervals" %(spec_line[1])

	os.system("/tools/samtools-1.16.1/samtools.exe faidx %s" % (Ref_file))
	os.system("java -jar picard.jar CreateSequenceDictionary -R %s" % (Ref_file))

	Chr_list = []
	intervals_df = open(intervals_file, 'r')

	for line in intervals_df:
	    ChrNum = line[:-1].split(":")[0]
	    if ChrNum not in Chr_list:
	        Chr_list.append(ChrNum)
	intervals_df.close()

	SplitRef(Ref_file, Chr_list)

	fw = open("./SNP_intervals.bed",'w')
	for ChrNum in Chr_list:
	    Chr_len = ''
	    for line in open("./lengths.txt", "r"):
	        if line.split(" ")[0] == ChrNum:
	            Chr_len = int(line[:-1].split(" ")[1])
	    Chr_intervals = []
	    for line in open(intervals_file, 'r'):
	        if line[:-1].split(":")[0] == ChrNum:
	            Chr_intervals.append(int(line[:-1].split(":")[1].split("-")[0]))
	    SNP_section = Find_SNP_Section(Chr_intervals, Section_len_half, Chr_len)
	    SNP_meraged_section =  merge_ranges(SNP_section)
	    for SNP_section in SNP_meraged_section:
	        fw.write(str(ChrNum)+"\t")
	        fw.write(str(SNP_section[0])+"\t")
	        fw.write(str(SNP_section[1])+"\n")
	fw.close()

	os.system("/tools/seqtk-1.3/seqtk.exe subseq %s SNP_intervals.bed > SNP_intervals.fasta"%(Ref_file))
	os.system("mv ./*.bim config.txt %s00.Make_RefGenome/" %(Getwd()))
	os.system("rm -rf lengths.txt SNP_intervals.bed Chr_fa/ ")

	result_file = spec_line[0]+"_"+spec_line[1]
	os.system("mkdir %s" %(result_file))
	os.system("mv %s.fasta %s.fasta.fai %s.dict %s.intervals SNP_intervals.fasta %s" 
		%(spec_line[0],spec_line[0],spec_line[0],spec_line[1],result_file))

	os.system("/tools/bowtie2-2.4.5-mingw-x86_64/bowtie2-build %s/%s.fasta %s/%s"
		%(result_file,spec_line[0],result_file,spec_line[0]))
	os.system("/tools/bowtie2-2.4.5-mingw-x86_64/bowtie2-build %s/SNP_intervals.fasta %s/SNP_intervals"
		%(result_file,result_file))
	os.system("rm -rf %s01.Reference_Genome/%s"%(Getwd(),result_file))
	os.system("mv %s %s01.Reference_Genome/"%(result_file,Getwd()))

def Processing(num,sta):
	i = 80
	a = "*" * num
	b = "." * (i - num)
	c = (num / i) * 100
	dur = time.perf_counter() - start
	print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end = "")


os.system('cat ./README.txt')	
input()
start = time.perf_counter()
os.system('cp %s00.Make_RefGenome/config.txt ./config.txt  '%(Getwd()))	
with open('./config.txt','r') as file:
	content = file.read()
	if CheckConfig(content):
		print(42*"-","Runing",43*"-")
		Processing(10,start)
		spec_line = Movefile()
		Processing(20,start)
		MakeREF(spec_line)
		Processing(40,start)
	else:
		os.system('rm -rf ./config.txt')
		print("\n"+70*"-"+"\nThe configuration file is empty. \nCheck the configuration file !")
		sys.exit()

with open('../Reference_Genome/config.txt', 'r') as f:
    lines = f.readlines()
dict_lines = {}
for line in lines:
    if line.startswith(">>"):
        current_key = line.strip()
        if current_key not in dict_lines:
            dict_lines[current_key] = set()
    elif line.startswith(">"):
        if current_key in dict_lines:
            dict_lines[current_key].add(line.strip())
Processing(60,start)
with open('../Reference_Genome/config.txt', 'w') as f:
    for key in dict_lines:
        f.write(key + "\n")
        for line in dict_lines[key]:
            f.write(line + "\n")
Processing(80,start)
print("\n"+40*"-"+"Completed !!!"+40*"-"+"\n"+"Please close this window.")