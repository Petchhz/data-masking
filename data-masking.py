import pandas as pd
from pythainlp.tag.named_entity import ThaiNameTagger
import re
from nltk.tokenize import RegexpTokenizer
from pythainlp.tokenize import word_tokenize

df = """ data """

message_list = df["Message"].to_list()

new_message_regex = []
thainer = ThaiNameTagger()
angle_pattern = r"\<(.*?)\>(.*?)\<\/(.*?)\>"
angle_tokenizer = RegexpTokenizer(angle_pattern)

#thainer = ner.get_ner(text, pos=False)
#print(thainer, "\n")

for idx, text in enumerate(message_list):
    ner_tag = thainer.get_ner(str(text), pos=False, tag=True)
    print("ID: ", idx+1, "\n")
    #print(ner_tag)
    entity_tokens = angle_tokenizer.tokenize(ner_tag)
    #entity_tokens = list(entity_tokens[0])
    #if "[" in entity_tokens[1]:
    #    masked_token_search = re.search(r"\[([A-Za-z0-9_]+)\]", entity_tokens[1])
    #    entity_tokens[1] = normalize_label(masked_token_search.group(1))
    print(entity_tokens, "\n") #print tag only
    temp_text = text
    #for e in entity_tokens:
        #if e[0] == "PERSON":
            #person_name = e[1]
            #print("CustomerName: ", person_name)

    #-==================================================================== NER =========================================================================
    
    for e in entity_tokens:
        #print(e)
        if e[0] == "PERSON":
            person_name = e[1]
            temp_text = temp_text.replace(person_name, "[CustomerName]")
            #temp_text = temp_text.replace(person_name, "<PERSON>" + person_name + "</PERSON>", "[CustomerName]")
            #print(e)
            #print("PERSON:", e)
        if e[0] == "ORGANIZATION":
            organization = e[1]
            temp_text = temp_text.replace(organization, "[Organization]")
            #temp_text = temp_text.replace(organization, "<ORGANIZATION>" + organization + "</ORGANIZATION>", "[Organization]")
            #print("LOCATION:", e)
        #if e[0] == "DATE":
            #dob = e[1]
            #if re.findall(r"\s(\d{4})", dob):
            #temp_text = re.sub(dob, "[DateOfBirth]", temp_text)
            #print("DATE:", e)
    
    #====================================================================== REGEX =========================================================================

    #--------------------------------------------------------------------- CitizenId ----------------------------------------------------------------------
    # 0000000000000 
    if re.findall(r"[\d]{13}", temp_text):
        temp_text = re.sub(r"[\d]{13}", "[CitizenId]", temp_text)
    # 0 0000 00000 00 0
    elif re.findall(r"[\d]{1}\s[\d]{4}\s[\d]{5}\s[\d]{2}\s[\d]{1}", temp_text):
        temp_text = re.sub(r"[\d]{1}\s[\d]{4}\s[\d]{5}\s[\d]{2}\s[\d]{1}", "[CitizenId]", temp_text)
    # 0 000000 000000
    elif re.findall(r"[\d]{1}\s[\d]{6}\s[\d]{6}", temp_text):
        temp_text = re.sub(r"[\d]{1}\s[\d]{6}\s[\d]{6}", "[CitizenId]", temp_text)
    
    #------------------------------------------------------------------- PhoneNumber ----------------------------------------------------------------------
    # 000-000-0000
    if re.findall(r"[\d]{3}-[\d]{3}-[\d]{4}", temp_text):
        temp_text = re.sub(r"[\d]{3}-[\d]{3}-[\d]{4}", "[PhoneNumber]", temp_text)       
    # 000-0000000
    elif re.findall(r"[\d]{3}-[\d]{7}", temp_text):
        temp_text = re.sub(r"[\d]{3}-[\d]{7}", "[PhoneNumber]", temp_text)
    # 0000000000
    elif re.findall(r"[0][\d]{9}", temp_text):
        temp_text = re.sub(r"[\d]{10}", "[PhoneNumber]", temp_text)
    # (000-0000000)
    elif re.findall(r"([\d]{3}-[\d]{7})", temp_text):
        temp_text = re.sub(r"([\d]{3}-[\d]{7})", "[PhoneNumber]", temp_text)
    # (000-000-0000)
    elif re.findall(r"([\d]{3}-[\d]{3}-[\d]{4})", temp_text):
        temp_text = re.sub(r"([\d]{3}-[\d]{3}-[\d]{4})", "[PhoneNumber]", temp_text)
    # 000 000-0000    
    elif re.findall(r"[\d]{3}\s[\d]{3}-[\d]{4}", temp_text):
        temp_text = re.sub(r"[\d]{3}\s[\d]{3}-[\d]{4}", "[PhoneNumber]", temp_text)
    # 000 000 0000
    elif re.findall(r"[\d]{3}\s[\d]{3}\s[\d]{4}", temp_text):
        temp_text = re.sub(r"[\d]{3}\s[\d]{3}\s[\d]{4}", "[PhoneNumber]", temp_text)
    # 000 0000000    
    elif re.findall(r"([\d]{3}\s[\d]{7})", temp_text):
        temp_text = re.sub(r"([\d]{3}\s[\d]{7})", "[PhoneNumber]", temp_text)   
    # 00-00000000    
    elif re.findall(r"[\d]{2}-[\d]{8}", temp_text):
        temp_text = re.sub(r"[\d]{2}-[\d]{8}", "[PhoneNumber]", temp_text)
    # 00-0000-0000
    elif re.findall(r"[\d]{2}-[\d]{4}-[\d]{4}", temp_text):
        temp_text = re.sub(r"[\d]{2}-[\d]{4}-[\d]{4}", "[PhoneNumber]", temp_text)
  
    # 0000000000 2201-2400 found 3 phone number in conversation use it for detect phonenumber 
    if re.findall(r"[^\d](\d{10})[^\d]", temp_text):
        temp_text = re.sub(r"[^\d](\d{10})[^\d]", "[PhoneNumber]", temp_text)
    
    #------------------------------------------------------------------- Address ------------------------------------------------------------------------
    #ที่อยู่ บ้านเลขที่ ตำบล อำเภอ จังหวัด รหัสไปรษณีย์
    if re.findall(r"(ที่อยู่)+\s[\u0E00-\u0E7F0-9/ -.()\s]+\d{5}", temp_text):
        temp_text = re.sub(r"(ที่อยู่)+\s[\u0E00-\u0E7F0-9/ -.()\s]+\d{5}", "[Address]", temp_text)
    #บ้านเลขที่(xx/xx) ตำบล อำเภอ จังหวัด รหัสไปรษณีย์
    elif re.findall(r"\d{1,}/\d{1,}\s[\u0E00-\u0E7F0-9/ -.\s]+\d{5}", temp_text):
        temp_text = re.sub(r"\d{1,}/\d{1,}\s[\u0E00-\u0E7F0-9/ -.\s]+\d{5}", "[Address]" , temp_text)
    #บ้านเลขที่(xx) ตำบล อำเภอ จังหวัด รหัสไปรษณีย์
    elif re.findall(r"\d{1,}\s[\u0E00-\u0E7F0-9/ -.\s]+\d{5}", temp_text):
        temp_text = re.sub(r"\d{1,}\s[\u0E00-\u0E7F0-9/ -.\s]+\d{5}", "[Address]", temp_text)

    #------------------------------------------------------------------ DateOfBirth ------------------------------------------------------------------------
    #00/00/0000
    if re.findall(r"\d{1,2}/\d{1,2}/\d{1,4}", temp_text):
        temp_text = re.sub(r"\d{1,2}/\d{1,2}/\d{1,4}", "[Date]", temp_text)
    #วัน เดือน ปี
    elif re.findall(r"\d{1,2}[\u0E00-\u0E7F.\s]{1,9}\d{2,4}", temp_text):
        temp_text = re.sub(r"\d{1,2}[\u0E00-\u0E7F.\s]{1,9}\d{2,4}", "[Date]", temp_text)


    #------------------------------------------------------------------- ContactEmail ----------------------------------------------------------------------     
    if re.findall(r"\b[A-Za-z0-9.%_+-]+@[a-zA-Z]+\.(com|edu|net|COM)", temp_text):
        temp_text = re.sub(r"\b[A-Za-z0-9.%_+-]+@[a-zA-Z]+\.(com|edu|net|COM)", "[ContactEmail]", temp_text)
    elif re.findall(r"\b[A-Za-z0-9.%_+-]+@[a-zA-Z]+\.(ac)+\.(th)", temp_text):
        temp_text = re.sub(r"\b[A-Za-z0-9.%_+-]+@[a-zA-Z]+\.(ac)+\.(th)", "[ContactEmail]" , temp_text)

    #new_list.append(temp_text)
    #new_tag_py.append(entity_tokens) #add tag to list
    #new_message.append(temp_text) #add message to list
    new_message_regex.append(temp_text)
    print(temp_text,"\n")
    #print(text, "\n")
    print("="* 90, "\n")

df["Masked_Message_Pythai"] = new_message_regex

#save excel or csv file
df.to_excel('Sheet.xlsx')
df.to_csv('Sheet.csv')