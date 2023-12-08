import os
import sys
import csv
from datetime import datetime,time,timedelta
from collections import OrderedDict
BASE_DIR1 = os.getcwd()
a = BASE_DIR1.split("\\")
B1 = a[0]+"\\"+a[1]+"\\"+a[2]


# path_csv_raw = BASE_DIR+"\\Desktop\\Book1.csv"
# path_csv_result = BASE_DIR+"\\Desktop\\Book2.csv"
# first_date = "12:14,11.27.2023"
# end_date = "12:14,11.27.2023"

class TempInfo():
    
    #BASE_DIR = os.getcwd()
    
    #def __init__(self,path_csv_raw,path_csv_result,first_date,end_date,first_time,end_time,type=".csv"):        
    def __init__(self,path_csv_raw,path_csv_result,first_date,end_date,type=".xlsx"):        
        
        self.content_scraping = [] # result
        
        self.path_csv_result = B1 + path_csv_result + type   #"\\Desktop\\Book2.csv"
        #self.path_csv_result = 'C:\\Users\\sadegh' + path_csv_result + type 
        self.path_csv_raw = B1 + path_csv_raw + type         #"\\Desktop\\Book1.csv"
        #self.path_csv_raw = 'C:\\Users\\sadegh' + path_csv_raw + type         #"\\Desktop\\Book1.csv"

        self.first_date = first_date  #"12:14,11.27.2023"
        self.end_date = end_date      #"12:14,11.27.2023"
       
        #self.first_time = first_time  #"12:14,11.27.2023"
        #self.end_time = end_time      #"12:14,11.27.2023"
       
        self.content_before = self.read_from_csv()
        self.content_after = self.proccess_my_data()

    def update_content(self):
        self.content_before = self.read_from_csv()
        self.content_after = self.proccess_my_data()
        
    def read_from_csv(self):
        with open(self.path_csv_raw,"rb") as f:
            content = f.read()
            print("c is = ",content.decode(),"end c")
        return content
    
    def proccess_my_data(self):
        self.content = self.content_before
        data_proccessed = self.content[3:].replace("\n",",").replace("\"","").split(",")[:-1] #remove \n then " from data and seperate the string to list with , and ignore the last item of list becuase it's ''         
        return data_proccessed
    
    def scrape_my_data(self):
        self.content_scraping  = []
        #print(len(self.content_after))
        for i in range(0,len(self.content_after),3):
            print(i)
            #_time = self.content_after[i].split(":") 
            _time = self.content_after[i+1] 
            _date = self.content_after[i]
            #print(_date.strip()+" "+_time)
            #_tstruct = time(int(_time[0]),int(_time[1]))
            try:
                _dstruct = datetime.strptime(_date.strip()+" "+_time.strip() ,"%m/%d/%Y %H:%M")
            except ValueError:
                continue
            print(_dstruct)
            #if self.first_date <= _dstruct and self.first_time <= _tstruct and self.end_date >= _dstruct and self.end_time >= _tstruct :
            if self.first_date <= _dstruct and self.end_date >= _dstruct:
                    
                    self.content_scraping.append(self.content_after[i])
                    self.content_scraping.append(self.content_after[i+1])
                    self.content_scraping.append(self.content_after[i+2])                
            elif self.end_date < _dstruct:
                break
    
    def write_to_csv(self):
        if os.path.exists(self.path_csv_result): 
            os.remove(self.path_csv_result) 
        data_proccessed = self.content_scraping
        with open(self.path_csv_result,"a",encoding='UTF8',newline="") as f:
            a = csv.writer(f)
            for i in range(0,len(data_proccessed),3):  
                a.writerow(data_proccessed[i:i+3])
    
    def show_my_data(self,before=False,after=False):
        if before == True:
            print("### content before processed ###")
            print(self.content_before)
        
        if after == True:
            print("### content after processed ###")
            print(self.content_after)
        

    def delete_my_data(self):
        del self.content_after
        del self.content_before
        
#print(content)
def data_input(path = False):
    def get_path():
        path_csv_raw = input("path_csv_raw (defult=\\Desktop\\Book1):")
        if path_csv_raw == "":
            path_csv_raw = "\\Desktop\\Book1"
            
        path_csv_result = input("path_csv_result (defult=\\Desktop\\Book2):")
        if path_csv_result == "":
            path_csv_result = "\\Desktop\\Book2"
        return path_csv_raw,path_csv_result
    
    def date_and_time():
        
        first_date = input("first_date as format:month/day/year (example=12/14/2023, defualt = two days ago) :")
        first_time = input("first_time as format:hour/minute    (example=12:45 , defualt=00:01) :")
        end_date =   input("\nend_date as format:month/day/year (example=12/27/2023, defualt = today) :")
        end_time =   input("end_time as format:hour/minute      (example=13:15 , defualt = now) :")
        
        now_datetime = datetime.today()
        
        if first_time == "":
            first_time = "00:01"
        if end_time == "":
            end_time = str(now_datetime.hour)+":"+str(now_datetime.minute)
        if first_date == "":
            tow_day_ago = now_datetime - timedelta(days=2)
            first_date = str(tow_day_ago.month)+"/"+str(tow_day_ago.day)+"/"+str(tow_day_ago.year)
        if end_date == "":
            end_date = str(now_datetime.month)+"/"+str(now_datetime.day)+"/"+str(now_datetime.year)
 
        return first_date.strip(),first_time.strip(),end_date.strip(),end_time.strip()
   
    # type = print("type of file (defult = .csv):")
    # if type == "":
    #     type = ".csv"
   
    path_csv_raw,path_csv_result = None,None
    if path == True:
        path_csv_raw,path_csv_result = get_path()
    
    
    #while True:
        
    first_date,first_time,end_date,end_time = date_and_time()
    
    first_date = datetime.strptime(first_date+" "+first_time , "%m/%d/%Y %H:%M")
    end_date = datetime.strptime(end_date+" "+end_time, "%m/%d/%Y %H:%M")
    #first_time = time(int(first_time.split(":")[0]),int(first_time.split(":")[1]))
    #end_time = time(int(end_time.split(":")[0]) ,int(end_time.split(":")[1]))
        #except:
        #    print("\n\n!! ERROR !!\n please try to correct data and time input\n")        
        #else:
        #    break
    #return path_csv_raw,path_csv_result,first_date,first_time,end_date,end_time
    return path_csv_raw,path_csv_result,first_date,end_date


if __name__ == "__main__":
    
    #path_csv_raw,path_csv_result,first_date,first_time,end_date,end_time = data_input(path=True)
    path_csv_raw,path_csv_result,first_date,end_date = data_input(path=True)
    
    #main_object = TempInfo(path_csv_raw,path_csv_result,first_date,end_date,first_time,end_time)     
    main_object = TempInfo(path_csv_raw,path_csv_result,first_date,end_date)     
    
    while True:
        dict_of_action = {#1:"print data before processing",
                          #2:"print data after processing",
                          3:"inter the new time to scraping",
                          4:"update the content and file",
                          5:"print input time and date",
                          6:"scrap and return data",
                          7:"write data to result file",
                          10:"nothing and close the progrom",}
        print()
        for i in list(dict_of_action.items()):
            print("\t",i[0]," : ",i[1],sep="")
        #input()
        #try:
        action = int(input("please inter the command to do:"))
        print()
    
        if action == 1:
            main_object.show_my_data(before=True)
        elif action == 2:
            main_object.show_my_data(after=True)
        elif action == 3:
            #_,_,first_date,first_time,end_date,end_time=data_input(path=False)
            _,_,first_date,end_date=data_input(path=False)
            main_object.first_date = first_date
            main_object.end_date = end_date
            
        elif action == 4:
            main_object.update_content()
            main_object.show_my_data(before=True,after=True)
        elif action == 5:
            print("first_date:{}\nend_date:{}\n".format(first_date,end_date))
        elif action == 6:
            main_object.scrape_my_data()
            for i in range(0,len(main_object.content_scraping),3):
                print(main_object.content_scraping[i]," ",main_object.content_scraping[i+1]," ",main_object.content_scraping[i+2])
        elif action == 7:
            main_object.write_to_csv()   
        #except:
         #   continue
        else:
            if action == 10:
                quit()
                sys.exit()
            