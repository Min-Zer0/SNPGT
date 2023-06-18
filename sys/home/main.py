#!/usr/bin/python 
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
import xlrd
import sys
import os
import time

def Timer(Start,End,Message):
	m, s = divmod(End-Start, 60)
	h, m = divmod(m, 60)
	put_text(Message,"used time: %02d:%02d:%02d" % (h, m, s))

def Getwd():
	for line in open('./install_dir'):
	    chr_dir = line
	dir_list = chr_dir[1:].split("\\")[:-1]
	Path = "/cygdrive/" + dir_list[0][:-1] + "/"
	for i in range(len(dir_list)-1):
		Path = Path+'"'+dir_list[i+1]+'"'+"/"
	return Path


def Alignment(Reference_dir,Species,Sample,Read1,Read2,Thread):
	start = time.time()
	os.system('/tools/bowtie2-2.4.5-mingw-x86_64/bowtie2 -p %s \
		-x ./Reference_Genome/%s/SNP_intervals \
		-U ./Input_Fastq/%s ./Input_Fastq/%s \
		-S temp.sam'%(Thread,Reference_dir,Read1,Read2))
	os.system('/tools/samtools-1.16.1/samtools.exe fastq -0 \
		read.fastq temp.sam && rm -rf temp.sam')
	os.system('/tools/bowtie2-2.4.5-mingw-x86_64/bowtie2 -p %s \
		-x ./Reference_Genome/%s/%s \
		-U read.fastq\
		--rg-id %s \
		--rg "PL:ILLUMINA" \
		--rg "SM:%s" \
		-S ./%s.sam'%(Thread,Reference_dir,Species,Sample,Sample,Sample))
	os.system('rm -rf read.fastq')
	os.system('/tools/samtools-1.16.1/samtools.exe view -bS \
		./%s.sam -t ./Reference_Genome/%s/%s.fai > ./%s.bam && \
		rm -rf ./%s.sam'%(Sample,Reference_dir,Species,Sample,Sample))
	os.system('/tools/samtools-1.16.1/samtools.exe sort -@ %s\
		-o ./%s.sorted.bam ./%s.bam && rm -rf ./%s.bam'%(Thread,Sample,Sample,Sample))
	end = time.time()
	Timer(start,end,Sample+" Alignment")

def  Merge_rmPCRdup(Project,Thread):
	start = time.time()
	os.system('mkdir -p samplebamfile && mv *.sorted.bam samplebamfile')
	os.system('/tools/samtools-1.16.1/samtools.exe merge ./%s.sorted.bam \
		./samplebamfile/*.sorted.bam && rm -rf ./samplebamfile'%(Project))
	os.system('/tools/samtools-1.16.1/samtools.exe rmdup -sS ./%s.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.sorted.bam'%(Project,Project,Project))
	os.system('/tools/samtools-1.16.1/samtools.exe sort -@ %s -o ./%s.rmdup.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.rmdup.bam'%(Thread,Project,Project,Project))
	os.system('/tools/samtools-1.16.1/samtools.exe index \
		./%s.rmdup.sorted.bam'%(Project))
	end = time.time()
	Timer(start,end,"Merge_rmPCRdup")

def Calling_SNP(Reference,ref,Project,Intervals,Thread):
	start = time.time()
	os.system('java -Xmx%sg -jar GenomeAnalysisTK.jar \
		-T RealignerTargetCreator \
		-R ./Reference_Genome/%s \
		-I %s.rmdup.sorted.bam \
		-o %s.realn.intervals'%(Thread,Reference,Project,Project))
	os.system('java -Xmx%sg -jar GenomeAnalysisTK.jar \
		-T IndelRealigner \
		-R ./Reference_Genome/%s \
		-targetIntervals %s.realn.intervals \
		-I %s.rmdup.sorted.bam \
		-o %s.realn.bam'%(Thread,Reference,Project,Project,Project))
	os.system('mv ./Reference_Genome/%s ./'%(Intervals))
	os.system('java -Xmx%sg -jar GenomeAnalysisTK.jar \
		-T UnifiedGenotyper \
		--genotype_likelihoods_model SNP\
		-R ./Reference_Genome/%s \
    	-I %s.realn.bam \
    	-L %s.intervals\
    	-o %s.raw.vcf \
    	--output_mode EMIT_ALL_SITES'%(Thread,Reference,Project,ref,Project))
	os.system('mv %s.intervals ./Reference_Genome/%s'%(ref,Intervals)) 	
	os.system('rm -rf %s.rmdup.sorted.bam %s.rmdup.sorted.bam.bai \
		%s.realn.bam %s.realn.bai %s.realn.intervals \
		%s.raw.vcf.idx'%(Project,Project,Project,Project,Project,Project))
	end = time.time()
	Timer(start,end,"Calling_SNP")

def VCF2Genotyping(Project,SamplesNum):
	sample_col=''
	for i in range(SamplesNum):
		sample_col = sample_col+',$'+str(10+i)
		col_num = "$1,$2,$4,$5"+sample_col
	os.system("grep -v '##' %s.raw.vcf | awk '{print %s}' > %s.vcf2Genotyping.txt"%(Project,col_num,Project))
	VCF_df = open(Project+'.vcf2Genotyping.txt', 'r')
	with open(Project+'.Genotype.txt', 'w') as fw:
		for line in VCF_df:
			if line[0] == "#":
				outputline=line[:-1].split(' ')[0:2] + line[:-1].split(' ')[4:SamplesNum+4]
				fw.write('\t'.join(map(str, outputline)))
				fw.write('\n')
			else:
				info = line[:-1].split(" ")
				ChrNum = info[0]
				Pos = info[1]
				bas = [info[2]] + info[3].split(',')
				outputline=[ChrNum,Pos]
				for i in range(SamplesNum):
					SNP = info[4+i].split(':')[0].split('/')
					if SNP[0] != SNP[1]:
						outputline = outputline + ['H']
					else:
						if SNP[0] == '.':
							outputline = outputline + ['.']
						else:
							outputline = outputline + [bas[int(SNP[0])]]
				fw.write('\t'.join(map(str, outputline)))
				fw.write('\n')
	os.system('rm -rf %s.vcf2Genotyping.txt'%Project)
	os.system("mv %s.Genotype.txt %s.raw.vcf %s"%(Project,Project,Getwd()))


def main_analysis(species,reference,Samples_list,project):
	alignment_reference_dir = species+'_'+reference
	gatk_reference = species+'_'+reference+'/'+species+'.fasta'
	intervals = species+'_'+reference+'/'+reference+'.intervals'
	with use_scope('scope5'):
		style(put_html("<h3>Please enter the number of threads available to run the program.</h3>"),'color:#0066CC')
		style(put_html("<b><font color=red>Note:</font> The more threads, the faster it will run. However, the actual configuration of the computer needs to be considered.</b>"),'color:green')
		thread = input('Thread', type=NUMBER)
	with use_scope('scope5',clear=True):
		confirm = actions('Run program?', ['Run'],
			help_text='There will be a 1-2 hour waiting time.')
		put_markdown('Program `%s`ing ...' % confirm)

		put_processbar('bar2',0.2, label= "Alignment...");
		for i in Samples_list:
			Alignment(alignment_reference_dir,species,i['Sample'],i['Read1'],i['Read2'],thread)
		set_processbar('bar2', 0.45, label="Merging & Removing PCR duplication ...")
		Merge_rmPCRdup(project,thread)
		set_processbar('bar2', 0.7,label="Calling SNP ...")
		Calling_SNP(gatk_reference,reference,project,intervals,thread)
		os.system('mv -f ./Input_Fastq/* %s02.Input_Fastq/ '%(Getwd()))
		os.system('rm -rf ./Input_Fastq/* ')
		VCF2Genotyping(project,len(Samples_list))
		set_processbar('bar2', 1,"Done！")
		img = open('../BgPic/Done.png', 'rb').read() 
		put_image(img, width='1000px')


def Check_Sample(species,reference):
	total_start = time.time()
	os.system('mv %s02.Input_Fastq/* ./Input_Fastq/  '%(Getwd()))
	os.system('mv ./Input_Fastq/Sample.table.xls %s02.Input_Fastq/ '%(Getwd()))
	gz_files = os.listdir(r'./Input_Fastq/')
	if len(gz_files) == 0:
		popup('',[style(put_html("<h3>ERROR: Reads file does not exist!</h3> Please ensure that you have moved the reads file (*.fastq.gz) to the path: ./02.Input_Fastq."), 'color:red')])		
	else:
		with use_scope('scope3',clear=True):
			put_html("<h4>Read and unzip fastq.gz.</h4>")
			put_processbar('bar_fqgz',0.2);
			files_nums = len(gz_files)
			for i in range(files_nums):
				start = time.time()
				os.system('gunzip ./Input_Fastq/%s'%(gz_files[i]))
				set_processbar('bar_fqgz', (i+1)/files_nums)
				end = time.time()
				Timer(start,end,"Read "+gz_files[i])
		with use_scope('scope3',clear=True):
			Timer(total_start,end,"Total")
			style(put_html("<h4>Raw reads files have been read and unziped, go on!</h4>"), 'color:green')
			put_html("<h2>3. Project</h2>")
		project = input('Please enter your project name which will be the prefix of output files.', type=TEXT, placeholder='Project',
        				  required=True)
		put_html('<h3><span style="font-style: italic;">%s</span></h3>'%(project))
		Samples_list = []
		answer = 'Yes'
		while answer == 'Yes':
			read_files = os.listdir(r'Input_Fastq/')
			SampleReadinfo = input_group("Please enter your sample names and select the the corresponding reads files.",[
	  								 input('Sample', name='Sample'),
	  								 select("Read1",read_files, name="Read1"),
									 select("Read2",read_files, name="Read2")
									 ])
			with use_scope('scope4', clear=True):
				Samples_list.append(SampleReadinfo)
				sample_table = [['Sample','Read1','Read2']]
				for i in Samples_list:
					sample_table.append([i['Sample'], i['Read1'],i['Read2']])
				put_table(sample_table)
			answer = actions('Add more samples?',['Yes', 'Finish adding samples'])
		main_analysis(species,reference,Samples_list,project)

def readExcel():
	workbook = xlrd.open_workbook('Input_Fastq/Sample.table.xls')
	worksheet = workbook.sheet_by_name('Sheet1')
	nrows = worksheet.nrows
	ncols = worksheet.ncols
	data = []
	for i in range(nrows):
	    row = []
	    for j in range(ncols):
	        cell_value = worksheet.cell_value(i, j)
	        row.append(cell_value)
	    data.append(row)
	    
	data = [row[:-2] for row in data]
	data = [row for row in data if any(col != '' for col in row)]

	Samples_list = []
	for i in data[3:]:
		Sample_dict = {'Sample': i[1], 'Read1': i[2], 'Read2': i[3]}
		Samples_list.append(Sample_dict)
	project = data[1][2]
	return Samples_list,project


def  readExcel_Check_Sample(species,reference):
	total_start = time.time()
	os.system('mv  %s02.Input_Fastq/* ./Input_Fastq/'%(Getwd()))
	Excel_info = readExcel()
	Samples_list = Excel_info[0]
	project = Excel_info[1]
	gz_files = os.listdir(r'./Input_Fastq/')
	if len(gz_files) == 0:
		popup('',[style(put_html("<h3>ERROR: Reads file does not exist!</h3> Please ensure that you have moved the reads file (*.fastq.gz) to the path: ./02.Input_Fastq."), 'color:red')])		
	else:
		with use_scope('scope3',clear=True):
			put_html("<h4>Read and unzip fastq.gz.</h4>")
			put_processbar('bar_fqgz',0.2);
			files_nums = len(gz_files)
			for i in range(files_nums):
				start = time.time()
				os.system('gunzip ./Input_Fastq/%s'%(gz_files[i]))
				set_processbar('bar_fqgz', (i+1)/files_nums)
				end = time.time()
				Timer(start,end,"Read "+gz_files[i])
		with use_scope('scope3',clear=True):
			Timer(total_start,end,"Total")
			style(put_html("<h4>Raw reads files have been read and unziped, go on!</h4>"), 'color:green')
			put_html("<h2>3. Project</h2>")
		put_html('<h3><span style="font-style: italic;">%s</span></h3>'%(project))
		with use_scope('scope4', clear=True):
			sample_table = [['Sample','Read1','Read2']]
			for i in Samples_list:
				sample_table.append([i['Sample'], i['Read1'],i['Read2']])
			put_table(sample_table)
		main_analysis(species,reference,Samples_list,project)


def Check_Ref(species,reference):
		os.system('mv -f %s01.Reference_Genome/* ./Reference_Genome/ '%(Getwd()))		
		start=time.time()
		if os.path.exists(r'Reference_Genome/%s.tar.gz'%(species+'_'+reference)) == False and os.path.exists(r'Reference_Genome/%s'%(species+'_'+reference)) == False:
			popup('%s.tar.gz '%(species+'_'+reference),
				[style(put_html("<h3>ERROR: Dataset index does not exist! <br/><font color=#0066CC size=3>Please ensure that you have moved the downloaded file (*.tar.gz) to the path: ./01.Reference_Genome.</font></h3> "), 'color:red')])
		else:
			with put_loading():	
				os.system('tar -zxvf ./Reference_Genome/%s.tar.gz '%(species+'_'+reference))
				os.system('rm ./Reference_Genome/%s.tar.gz '%(species+'_'+reference))
				os.system('mv %s ./Reference_Genome/ '%(species+'_'+reference))
				os.system('rm -rf %s'%(species+'_'+reference))
				files = os.listdir(r'Reference_Genome/%s'%(species+'_'+reference))
				Check_file = {species+'.fasta',species+'.fasta.fai',
							  species+'.1.bt2',species+'.2.bt2',species+'.3.bt2',species+'.4.bt2',
							  species+'.rev.1.bt2',species+'.rev.2.bt2',species+'.dict',
							  reference+'.intervals',
							  'SNP_intervals.fasta',
							  'SNP_intervals.1.bt2','SNP_intervals.2.bt2','SNP_intervals.3.bt2','SNP_intervals.4.bt2',
							  'SNP_intervals.rev.1.bt2','SNP_intervals.rev.2.bt2'}
			if  set(files) == Check_file:
				popup('%s.tar.gz '%(species+'_'+reference),
					[style(put_html("<h3>Dataset indexing completed!</h3>"), 'color:green')])	
				end=time.time()
				with use_scope('scope2',clear=True):
					Timer(start,end,"Verifying Dataset index file")
					style(put_html("<h3>Indexing of the dataset has been completed, go on!</h3>"), 'color:green')
					put_html("<h2>2. Your samples raw data</h2>")
				read_mode = radio("Define the sample read sequence table",
					options=["Manual selection","Reading Excel table"])
				if read_mode == "Reading Excel table":
					with use_scope('scope3'):
						style(put_html("<h4>Move your reads files <font color=red>(*.fastq.gz)</font> or <font color=red>(*.fastq)</font> to the path: <font color=red>./02.Input_Fastq</font>.</h4>"),'color:#0066CC')	
						style(put_html("<h4>And fill in the Ecxel file<font color=red>(./02.Input_Fastq/Sample.table.xls)</font>.</h4>"),'color:#0066CC')	
						put_html("<h3>example:</h3>")	
						img = open('../BgPic/Excel.exp.png', 'rb').read()
						put_image(img, width='1000px')
						put_html("<h4>	</h4>")
						put_button('Confirm', lambda:readExcel_Check_Sample(species,reference))
				else:
					with use_scope('scope3'):
						style(put_html("<h4>Move your reads files <font color=red>(*.fastq.gz)</font> or <font color=red>(*.fastq)</font> to the path: <font color=red>./02.Input_Fastq</font>.</h4>"),'color:#0066CC')	
						put_button('Confirm', lambda:Check_Sample(species,reference))
			else:
				popup('%s.tar.gz '%(species+'_'+reference),
					[style(put_html("<h3>Dataset index file corruption! <br/><font color=#0066CC size=3>Re-download and move the file.</font></h3>"), 'color:red')])		
				os.system('rm -rf ./Reference_Genome/%s '%(species+'_'+reference))
			

def Select_Ref():
	with open('./Reference_Genome/GenomeAnalysis.config.txt', 'r') as f:
		Gen_Config = f.read()
	Gen_Config_info = Gen_Config.split(">>")[1:]
	Gen_info = []
	for S in Gen_Config_info:
		info = S.split("\n")
		speciesnamelist = info[0]
		line_list = []
		for i in info:
			if ">" in i:
				line_list.append(i[1:])
		line=[speciesnamelist,line_list]
		Gen_info.append(line)
	
	speciesnamelist = [sub_list[0] for sub_list in Gen_info]	
	species_select = select("Species", speciesnamelist)

	for i in range(0,len(Gen_info)):
		if species_select == Gen_info[i][0]:
			Line_list = [s.split("[")[0] for s in Gen_info[i][1]]
			species = species_select.replace(" ", "").replace("\t", "")
			with use_scope('scope1'):
				put_table([["Species","Dataset","Download Links"],[species_select]])
			reference_select = radio("Dataset",options=Line_list)
			for line in Gen_info[i][1]:
				if reference_select == line.split("[")[0]:
					reference = reference_select.replace(" ", "").replace("\t", "")
					Geno_url = line.split("[")[1].split("]")[0]
					markdown_url = '['+Geno_url+']'+'('+Geno_url+')'
					with use_scope('scope1', clear=True):
						put_table([["Species","Dataset","Download Links"],
								   [species,species+'_'+reference+".tar.gz",put_markdown(markdown_url)]])
	with use_scope('scope2'):
		style(put_html("<h3>Move the downloaded file <font color=red>(*.tar.gz)</font> to the path: <font color=red>./01.Reference_Genome</font>.</h3>"),'color:#0066CC')
		put_html('<b style="color:green"><font color=red>Note:</font> If you have already placed the downloaded file (*.tar.gz) under the path mentioned above and this is not your first time using this program, then you do not need to repeat this step.</b>')
	return species,reference


def Select_UserDefined():
	with open('./Reference_Genome/config.txt', 'r') as f:
		Gen_Config = f.read()
	Gen_Config_info = Gen_Config.split(">>")[1:]
	Gen_info = []
	for S in Gen_Config_info:
		info = S.split("\n")
		speciesnamelist = info[0]
		line_list = []
		for i in info:
			if ">" in i:
				line_list.append(i[1:])
		line=[speciesnamelist,line_list]
		Gen_info.append(line)
	
	speciesnamelist = [sub_list[0] for sub_list in Gen_info]	
	species_select = select("Species", speciesnamelist)

	for i in range(0,len(Gen_info)):
		if species_select == Gen_info[i][0]:
			Line_list = [s.split("[")[0] for s in Gen_info[i][1]]
			species = species_select.replace(" ", "").replace("\t", "")
			with use_scope('scope1'):
				put_table([["Species","Dataset"],[species_select]])
			reference_select = radio("Dataset",options=Line_list)
			for line in Gen_info[i][1]:
				if reference_select == line:
					reference = reference_select.replace(" ", "").replace("\t", "")
					with use_scope('scope1', clear=True):
						put_table([["Species","Dataset"],
								   [species,species+'_'+reference+".tar.gz"]])
	return species,reference


def Genotyping():
	img = open('../BgPic/head.png', 'rb').read() 
	put_image(img, width='1000px')
	put_html("<h2>1. Species and Dataset</h2>")
	file_path = os.path.join("./Reference_Genome", "config.txt")
	if os.path.exists(file_path):
		with use_scope('scope1'):
			put_html('<h3 style="color:#0066CC">Do you use User-Defined Reference genomes?</h3>')
		defined = radio("Dataset",options=["Default","User-Defined"])
		if defined == "User-Defined":
			species_reference = Select_UserDefined()
			with use_scope('scope2'):	
				put_button('Verify file', lambda:Check_Ref(species_reference[0],species_reference[1]))
		else:
			with use_scope('scope1'):
				put_html('<h3 style="color:#0066CC">Please select the species and dataset to genotype your samples.</h3>')
			species_reference = Select_Ref()
			with use_scope('scope2'):	
				put_button('Verify file', lambda:Check_Ref(species_reference[0],species_reference[1]))
	else:
		with use_scope('scope1'):
			put_html('<h3 style="color:#0066CC">Please select the species and dataset to genotype your samples.</h3>')
		species_reference = Select_Ref()
		with use_scope('scope2'):	
			put_button('Verify file', lambda:Check_Ref(species_reference[0],species_reference[1]))

if __name__ == '__main__':
	start_server( Genotyping,port = 80,debug=True,auto_open_webbrowser=True)