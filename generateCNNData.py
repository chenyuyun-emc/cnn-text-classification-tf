import csv

noteEventFile = file('NOTEEVENTS_DATA_TABLE.csv','rb')
diagnoseIdFile = file('DIAGNOSES_ICD_DATA_TABLE.csv','rb')

leftValue = 'History of Present Illness:'
rightValue = 'Past Medical History:'
value =''
list_pos = []

i = 0

noteEventReader = csv.reader(noteEventFile)

diagnoseIdReader = csv.reader(diagnoseIdFile)

pos_num = 0
neg_num = 0
num_1 = 0
num_2 = 0

for line in diagnoseIdReader:
    if line[4] == '4280':
        list_pos.append(line[2])


pos_file_object = open('data/rt-polaritydata/rt-polarity.pos', 'w')
neg_file_object = open('data/rt-polaritydata/rt-polarity.neg', 'w')

eval_pos_file_object = open('eval_data/rt-polaritydata/rt-polarity.pos', 'w')
eval_neg_file_object = open('eval_data/rt-polaritydata/rt-polarity.neg', 'w')

for line in noteEventReader:
    patientResult = line[10]
    left  = patientResult.find(leftValue)
    if left == -1:
        left = patientResult.find(leftValue.upper())
    right = patientResult.find(rightValue)
    if right == -1:
        right = patientResult.find(rightValue.upper())
    if left != -1 :
        value =  patientResult[left+len(leftValue):right].split('\n')
    else:
        value = ''

    hadm_id = line[2]

    if len(value) != 0 and len(hadm_id) != 0:
        resValue = ''
        num_1 = 0
        for res in value:
            if len(res) != 0 and num_1<80:
                num_1 = num_1 + 1
                resValue = resValue + res.strip() + ' '


        if hadm_id in list_pos:
            if pos_num < 1000:
                pos_num = pos_num +1
                pos_file_object.writelines(resValue+'\n')
            elif  pos_num < 2000:
                pos_num = pos_num +1
                eval_pos_file_object.writelines(resValue+'\n')

        else:
            if neg_num < 1000:
                neg_num = neg_num +1
                neg_file_object.writelines(resValue+'\n')
            elif neg_num < 2000:
                neg_num = neg_num +1
                eval_neg_file_object.writelines(resValue+'\n')

    if neg_num == 2000 and pos_num == 2000:
        break


pos_file_object.close()
neg_file_object.close()
