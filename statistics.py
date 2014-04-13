import random
random.seed(3)
#data_list = [random.randint(0,100) for r in range(100)]
#data_list = [1,1,2,2]
'''
print data_list
data_list.sort()
dis_list = list(set(data_list))
dis_list.sort()
print dis_list
'''

def cdf_to_textfile(input_list,file_name):
	data_list = input_list
	data_list.sort()
	dis_list = list(set(data_list))
	dis_list.sort()
	cdf_f = open("output_stat/"+file_name,'w')
	cdf_current = 0
	for item in dis_list:
		cdf_current +=  (float(data_list.count(item))/ len(data_list))
		tmp = str(round(item,4))+"\t"+str(round(cdf_current,4))
		cdf_f.write(tmp+"\n")
	cdf_f.close()	


def pdf_to_textfile(input_list,file_name):
	data_list = input_list
	data_list.sort()
	dis_list = list(set(data_list))
	dis_list.sort()
	pdf_f = open("output_stat/"+file_name,'w')	
	pdf_current = 0
	for item in dis_list:
		pdf_current =  (float(data_list.count(item))/ len(data_list))
		tmp = str(round(item,4))+"\t"+str(round(pdf_current,4))
		pdf_f.write(tmp+"\n")
	pdf_f.close()


def to_textfile(input_list,file_name):
	pdf_f = open("raw_data/"+file_name,'w')	
	for item in input_list:
		pdf_f.write(str(item)+"\n")
	pdf_f.close()

