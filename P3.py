import tkinter as tk
from tkinter import *
import re
import requests
import codecs
from lxml import html
import os
import sys
import urllib
import copy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import glob
import pandas as pd
import csv
import shutil
from bs4 import BeautifulSoup
from datetime import date


path = "../chromedriver"
cho_path = "./chromedriver"
database_path = "./database.csv"
d_header = ("nine_code","item_code","weblink","catagry")
curren_path = os.getcwd()
dict_product={}


if not os.path.exists("./database.csv"):
    with  open('./database.csv', 'w', newline='') as outputcsv:
        writer = csv.writer(outputcsv)
        writer.writerow(d_header)

if not os.path.exists("Download_html"):
    os.makedirs("Download_html")

if not os.path.exists("result"):
    os.makedirs("result")


def certif():
    def get_certif():
        global username_s
        username_s = u2.get("1.0", "end-1c")
        global password_s
        password_s = p2.get("1.0", "end-1c")
        root.destroy()

    root = Tk()
    root.title('Function')
    root.geometry("900x300")
    u1 = Label(root, text="Enter username: ")#.grid(row=1, column= 0,sticky=W) 
    u1.grid(row=0, column= 1,sticky=W) 

    u2 = Text(root,height = 1,width = 25)
    u2.grid(row=0, column= 2,sticky=W) 

    p1 = Label(root, text="Enter password: ")#.grid(row=1, column= 0,sticky=W) 
    p1.grid(row=1, column= 1,sticky=W) 

    p2 = Text(root,height = 1,width = 25)
    p2.grid(row=1, column= 2,sticky=W) 

    f3 = tk.Button(root, text="Enter", command=get_certif)#.grid(row=1, column=2, sticky=W)
    #f3 = tk.Button(root, text="Enter").grid(row=1, column=2, sticky=W)
    # f3.pack()
    f3.grid(row=1, column= 3,sticky=W) 

    root.mainloop()
certif()
#repeated run until username and password is not null !!!
while not (username_s != '' and password_s != '' ): 
    username_s = ''
    password_s = ''
    certif()




def append_multiple_lines(file_name, lines_to_append, mode):
    # Open the file in append & read mode ('a+')
    with open(file_name, mode) as file_object:
        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        if mode == "a+":
            data = file_object.read(100)
            if len(data) > 0:
                appendEOL = True
        # Iterate over each string in the list
        for line in lines_to_append:
            # If file is not empty then append '\n' before first line for
            # other lines always append '\n' before appending line
            if appendEOL == True:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)


# This function is from project 1, it collect the information and download the infomation of the package.

def start_working():
    if len(f2.curselection()) == 0:
        url = k2.get("1.0", "end-1c")
        dir_file_name = 'url_entered'
        
    # var1.set(f2.get(f2.curselection()))
    # print(len(f2.curselection()))
    # input("check!!!")
    
    else:
        choose_url_index = f2.curselection()[0]
        url = url_list[choose_url_index]
        dir_file_name = f2.get(f2.curselection())
    
    if not os.path.exists(dir_file_name):
        os.makedirs(dir_file_name)

    os.chdir('./'+dir_file_name)

    # url = "https://bstock.com/costco/all-inventory/computers-tablets/?p=2"

    # print(url)
    # input("check !!!!")
    # print(url)
    # print(dir_file_name)
    # f2.destroy()
    # result_text.set(url)
    # print(result_text.get())
    # print(type(f2.curselection()))
    
    driver = webdriver.Chrome(path)
    driver.get(url)
    sleep(1)

    username = driver.find_element_by_id("loginId")
    username.clear()
    # username.send_keys("Info@techfrys.com")
    username.send_keys(username_s)

    password = driver.find_element_by_id("password")
    password.clear()
    # password.send_keys("T8QvUJ6zn5!gcpP")
    password.send_keys(password_s)
    driver.find_element_by_tag_name("button").click()

    sleep(2)

    text = driver.page_source
    
    wrong_pass_re = re.compile(r'Invalid login credentials')
    wrong_pass = wrong_pass_re.findall(text)
    if len(wrong_pass) != 0 : 
        root.destroy()
        driver.quit()
        print("Wrong username or password")
        exit()

    driver.get(url)
    sleep(1)
    text = driver.page_source

    regex_product = re.compile(r'<li id=.*?</li>',re.DOTALL)

    information = regex_product.findall(text)
    # print(len(information))

    # print(information[0])
    information_str = ''.join(information)

    regex_product_url_regex = re.compile(r'https://bstock.com/costco/auction/auction/view/id.\d{6}')
    result_product_url_list = regex_product_url_regex.findall(information_str)

    #check all the url list
    # def get_information(url_list):
    #     for url in url_list:
    #         print(url)
    #     print()

    result_product_url_list = list(dict.fromkeys(result_product_url_list))

    # get_information(result_product_url_list)
    # input("check?")

    # fileToRead.close()
    # driver.quit()

    append_multiple_lines("scan_url.txt",result_product_url_list,"a+")
    
    # print("\nFinish Scan. All data store in file : 'scan_url.txt' \n")
    # result_text.set("Finish Scan.\n All data store in file : 'scan_url.txt'")
    # f1.destroy()
    # f2.destroy()
    # f3.destroy()
    # k1.destroy()
    # k2.destroy()

    result_text = tk.StringVar()
    # result = tk.Label(root, textvariable=result_text)#.grid(row=2, column= 0,sticky=W)
    # #result.pack()
    # result.grid(row=4, columnspan = 4,sticky=W)
    f = open("scan_url.txt")
    readline= f.readlines()
    information_str = ''.join(readline)
    if len(information_str) == 0:
        print("Please start with first function !")
        return

#remove last time runing to create new computer/result folder every time to aviod old information in  computer/result/information-computer.csv have old information
    if os.path.exists('./result'):
        shutil.rmtree("./result")
    if os.path.exists('./download_csv'):
        shutil.rmtree("./download_csv")

    if not os.path.exists('download_csv'):
        os.makedirs('download_csv')
    if not os.path.exists('result'):
        os.makedirs('result')
    # print(" Download! \n ")
    
    regex_product_url_regex = re.compile(r'https://bstock.com/costco/auction/auction/view/id.\d{6}')
    result_product_url_list = regex_product_url_regex.findall(information_str)
    # temp is to write back to the txt file
    temp = copy.copy(result_product_url_list)

    header = ("Six code","Current bid","Minimum bid Interval","Shipment cost","Bid close time","Costco code","Webpage url","Ext. Retail","Condition")
    
    if not os.path.exists("./result/information-%s.csv"%(dir_file_name)):
        with  open('./result/information-%s.csv'%(dir_file_name), 'w', newline='') as outputcsv:
            writer = csv.writer(outputcsv)
            writer.writerow(header)
    for page_url in result_product_url_list:
    # for i in range(0,len(result_product_url_list)):
    #     page_url = result_product_url_list[i]

        # counter +=1
        # print("counter: "+str(counter) )
        # counter -=1
        # if counter == 0:
        #     input("\nPress any key to Contiune!\n")
        #     counter =5
        # input("continue_loop?")
        # html = requests.get(page_url)
        # text = html.text
        #----------------------------------------open page one by one
        # driver = webdriver.Chrome(path)
        # driver.maximize_window()
        # driver.get(page_url)

        # input("check !!!!!!!!!!!!!!!!!!!!!!!!!!")

        # username = driver.find_element_by_id("loginId")
        # username.clear()
        # # username.send_keys("Info@techfrys.com")
        # username.send_keys(username_s)

        # password = driver.find_element_by_id("password")
        # password.clear()
        # # password.send_keys("T8QvUJ6zn5!gcpP")
        # password.send_keys(password_s)

        # driver.find_element_by_tag_name("button").click()

        # sleep(2)
        driver.get(page_url)
        sleep(2)

        print("Start crawling down information")

        text = driver.page_source

        wrong_pass_re = re.compile(r'Invalid login credentials')
        wrong_pass = wrong_pass_re.findall(text)
        if len(wrong_pass) != 0 : 
            root.destroy()
            driver.quit()
            print("Wrong username or password")
            exit()
        # fileToWrite = open("temp2.html", "w")
        # fileToWrite.write(pageSource)
        # fileToWrite.close()
        # fileToRead = open("temp2.html", "r")
        # text = fileToRead.read()
        auction_ended_regex = re.compile(r'Auction ended')
        auction_ended = auction_ended_regex.findall(text)
        # print(auction_ended)
        # print(len(auction_ended))
        # input("correct?")
        if len(auction_ended) != 0:
            #fileToRead.close()
            # driver.quit()
            temp.pop(0)
            append_multiple_lines("scan_url.txt",temp,"w")
            # print(str(page_url) + "\nHave finish the auction. Skip it from the download\n")
            # print("\nUpdated scan_file.txt file ! \n")
            # show_text = str(page_url) + "\nHave finish the auction. Skip it from the download\n"+"Updated scan_file.txt file ! \n"
            # result = tk.Label(root, textvariable=result_text)#.grid(row=2, column= 0,sticky=W)
            # #result.pack()
            # result.grid(row=4, columnspan = 4,sticky=W)
            # result_text.set(show_text)
            # result.update()

            if len(temp)==0:
                # show_text = show_text+"Finish all the file.\n"
                # result_text.set(show_text)
                break
            continue
        # input("checkpoint2")
        print("File is valid! ")
        # --------------find 6 code
        d_6_regex = re.compile(r'\d{6}?')
        d_6 = d_6_regex.findall(page_url)
        if len(d_6) ==0:
            print("No six code, contiune to next product")
        else:
            d_6 = str(d_6[0]. replace(',', ''))
        # print(d_6)

        # -------------- find current bid
        cur_bid_regex = re.compile(r'<span id="current_bid_amount">.*?</span>',re.DOTALL) 
        cur_bid = cur_bid_regex.findall(text)
        # print(cur_bid)

        cur_bid_str = ''.join(cur_bid)
        #remove newline
        # cur_bid_str = cur_bid_str.strip()
        # print(cur_bid_str)
        cur_bid_regex2 = re.compile(r'\d+,*\d*',re.DOTALL)
        cur_bid = cur_bid_regex2.findall(cur_bid_str)
        if len(cur_bid) == 0:
            cur_bid = 0
        # print(cur_bid)
        #conver from list to a int
        else:
            cur_bid = float(cur_bid[0]. replace(',', ''))

        #----------------------------------find the minimum bid

        next_bid_regex = re.compile(r'<span id="next_current_bid".*?</span>',re.DOTALL) 
        next_bid = next_bid_regex.findall(text)
        # print(next_bid)

        next_bid_str = ''.join(next_bid)
        next_bid_regex2 = re.compile(r'\d+,*\d*',re.DOTALL)
        next_bid = next_bid_regex2.findall(next_bid_str)

        if len(next_bid) == 0:
            next_bid = 0
        # print(next_bid)

        else:
            next_bid = float(next_bid[0].replace(',', ''))
        # print(next_bid)
        minimum_price = next_bid - cur_bid

        #--------------------------------shipment cost
        shipment_regex = re.compile(r'<span id="shipping_cost".*?</span>',re.DOTALL)
        shipment_cost = shipment_regex.findall(text)
        shipment_cost_str = ''.join(shipment_cost)
        shipment_regex2= re.compile(r'\d+,*\d*.?\d{2}?',re.DOTALL)
        shipment_cost = shipment_regex2.findall(shipment_cost_str)
        if len(shipment_cost) == 0:
            shipment_cost =0
        else:
            shipment_cost = float(shipment_cost[0].replace(',',''))
        # print(shipment_cost)


        #------------------------------- close date 
        end_time_regex = re.compile(r'<span id="auction_end_time".*?</span>',re.DOTALL)
        end_time = end_time_regex.findall(text)
        end_time_str = ''.join(end_time)
        end_time_regex2= re.compile(r'\S{3} \S+ \d+,.* PM|AM',re.DOTALL)
        end_time = end_time_regex2.findall(end_time_str)
        # print(end_time)
        end_time = end_time[0].replace(',','')
        # print(end_time)

        #-----------------short name #MON-2734918
        title_regex = re.compile(r'<h1 itemprop="name".*?</h1>',re.DOTALL)
        title = title_regex.findall(text)
        title_str = ''.join(title)
        # print(title_str)


        title_regex2= re.compile(r'\S{3}\-\d+',re.DOTALL)
        title = title_regex2.findall(title_str)
        # print(title)
        title = title[0].replace(',','')
        # print(title)

        #-----------get condition
        condition_regex = re.compile(r'data cleared|new condition|like new|A/B|Mixed Condition|C/D',re.IGNORECASE)
        condition_find = condition_regex.findall(title_str)
        if len(condition_find) ==0:
            condition_string = "Not specificed"
        # print(cur_bid)
        # condition_string = ''.join(condition_find)
        else:
            condition_string = condition_find[0].replace(',','')


        #---------get download URL 
        d_url_regex = re.compile(r'<button class="button" onclick.*?</button>')
        d_url = d_url_regex.findall(text)
        d_url_str = ''.join(d_url)
        # print(d_url_str)
        d_url_regex2= re.compile(r'https.*csv')
        d_url = d_url_regex2.findall(d_url_str)
        # print(d_url)
        if len(d_url) == 0:
            print("Auction is not avaialable. Skip this one")
            continue
        d_url = d_url[0].replace(',','')
        d_url = d_url.replace('&amp;','&') 
        # print(d_url)

        #--------------------get condition !!


        # title_regex = re.compile(r'<h1 itemprop="name.*?</h1>',re.DOTALL) 
        # title_find = title_regex.findall(text)
        # title_str = ''.join(title_find)
        # # print(cur_bid_str)

        # condition_regex = re.compile(r'data cleared|new condition|like new',re.IGNORECASE)
        # condition_find = condition_regex.findall(title_str)
        # # print(cur_bid)
        # condition_string = ''.join(condition_find)


        urllib.request.urlretrieve(d_url, './download_csv/%s.csv'%(title))
        file_name = title + ".csv"

        df = pd.read_csv("./download_csv/%s"%(file_name))
        df["Costco Order#"] = title
        ext_retail_total = df['Ext. Retail'].sum()

        # remove Inmar order # due the combine problem.
        a = list(df.columns)
        if('Inmar Order #' in a):
            a.remove('Inmar Order #')

        # df["Inmar Order#"] = d_6
        df[a].to_csv("./download_csv/%s"%(file_name), index=False)

        # input("maker sure xxx-xx.csv in download_csv dirctory the file added information current!!!")

        # print(d_6)
        # print(cur_bid)
        # print(minimum_price)
        # print(shipment_cost)
        # print(end_time)
        # print(title)
        # print(page_url)
        
        scan_infor = (str(d_6),str(cur_bid),float(minimum_price),float(shipment_cost),str(end_time),str(title),str(page_url),float(ext_retail_total),str(condition_string))
        with  open('./result/information-%s.csv'%(dir_file_name), 'a+', newline='') as outputcsv:
            writer = csv.writer(outputcsv)
            writer.writerow(scan_infor)
        print("\nUpdate the scanned informtaion to %s/result/information-%s.csv"%(dir_file_name,dir_file_name))

        # input("make sure information.csv is correct")
        # list_d6 = ["Six code is : ", d_6]
        # list_cur_bid= ["Current bid is : ", cur_bid]
        # list_minimum_price = ["Minimum bid price is : ", minimum_price]
        # list_shipment_cost = ["shipment cost is : ", shipment_cost]
        # list_endtime = ["Bid end time is  : " , end_time]
        # list_title = ["The name is : ", title]
        # from csv import writer
        # def append_list_as_row(file_name, list_of_elem):
        #     # Open file in append mode
        #     with open(file_name, 'a+', newline='') as write_obj:
        #         # Create a writer object from csv module
        #         csv_writer = writer(write_obj)
        #         # Add contents of list as last row in the csv file
        #         csv_writer.writerow(list_of_elem)

        # row_contents = [32,'Shaun','Java','Tokyo','Morning']
        # Append a list as new line to an old csv file

        # append_list_as_row(file_name, list_d6)
        # append_list_as_row(file_name, list_cur_bid)
        # append_list_as_row(file_name, list_minimum_price)
        # append_list_as_row(file_name, list_shipment_cost)
        # append_list_as_row(file_name, list_endtime)
        # append_list_as_row(file_name, list_title)

        # driver.quit()
        temp.pop(0)
        append_multiple_lines("scan_url.txt",temp,"w")
        # fileToRead.close()

        # sleep(2)
        # print("Finish file:  " + title + ".csv ! Store at download_csv dirctory \n")
        # print("Updated scan_file.txt file ! \n")
        
        # show_text = "Finish file:  " + title + ".csv ! Store at download_csv dirctory \n" + "Updated scan_file.txt file ! \n"
        # result = tk.Label(root, textvariable=result_text)#.grid(row=2, column= 0,sticky=W)
        #     #result.pack()
        # result.grid(row=4, columnspan = 4,sticky=W)
        # result_text.set(show_text)
        # result.update()

        # print(str(len(temp))+"!!!!")
        # input("check")
        if len(temp)==0:
            # show_text = show_text+"Finish all the file.\n"
            # result_text.set(show_text)
            break
    driver.quit()


    result_text = tk.StringVar()

    if not os.path.exists('download_csv'):
        return
    if not os.path.exists('result'):
        os.makedirs('result')
    os.chdir('./download_csv')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    os.chdir('../result')
    # combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
    combined_csv.to_csv( "combined_csv-%s.csv"%(dir_file_name), index=False)
    # print("\nCombine all the csv file store at result/combined_csv.csv\n")

    #extract two features from the csv file
    with open('combined_csv-%s.csv'%(dir_file_name), newline='') as inputcsv, open('temp.csv', 'w', newline='') as outputcsv:
        fieldnames = ('Costco Item #', 'Item Description')
        
        # writer = csv.DictWriter(outputcsv, fieldnames=fieldnames)
        # writer = csv.DictWriter(outputcsv,fieldnames=fieldnames)
        data = csv.DictReader(inputcsv)
        # print("Costco Item #")
        writer = csv.writer(outputcsv)
        writer.writerow(fieldnames)
        # data = csv.reader(inputcsv)

        #print("---------------------------------")
        for row in data:
            # print(row['\ufeffCostco Item #'], row['Item Description'])
            # print(row)
            dataselect = row[next(iter(row))], row['Item Description']
            writer.writerow(dataselect)
            # print(dataselect)
            # print(row[next(iter(row))])

    #remove duplicates of the two features.
    with open('temp.csv','r') as in_file, open('unique_item-%s.csv'%(dir_file_name),'w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate
            seen.add(line)
            out_file.write(line)
    os.remove("./temp.csv")
    os.chdir('..')
    # shutil.rmtree("./download_csv")

    os.chdir('..')
    # print("\nDelete download_csv dirctory\n")
    # print("\nFinish combine file, stored all unique items at result/unique_item.csv! \n")

    show_text = "Stored all information in ./information-%s.csv\n"%(dir_file_name) +  \
        "Combine all the csv file store at result/combined_csv-%s.csv\n"%(dir_file_name) + \
                "Stored all unique items at result/unique_item-%s.csv! "%(dir_file_name) 
    result = tk.Label(root, textvariable=result_text)#.grid(row=2, column= 0,sticky=W)
        #result.pack()
    result.grid(row=4, columnspan = 4,sticky=W)
    result_text.set(show_text)
    result.update()
    searchOutProduct(dir_file_name)

#support function from project 3 !!!   

def getInformation(text,item_number,driver1):
    not_find_regex = re.compile(r"We're sorry. We were not able to find a match.",re.DOTALL) 
    not_find = not_find_regex.findall(text)
    not_find_regex_2 = re.compile(r"but we weren't able to find the product you were looking for",re.DOTALL) 
    not_find_2 = not_find_regex_2.findall(text)
    url = driver1.current_url
    if(len(not_find)!=0 or len(not_find_2)!= 0):
        # print("Page not exits")
        # print("add to dictionary")
        # print(dict_product)
        # input("check !!!")
        return "-1","-1",url,"-1","-1","-1","-1","-1","-1","-1","-1","-1"

    
    d_9_regex = re.compile(r'\d{9}?')
    d_9 = d_9_regex.findall(str(url))
    if(len(d_9) == 0):
        d_9_regex = re.compile(r'\d{8}?')
        d_9 = d_9_regex.findall(str(url))
    if(len(d_9) == 0):
        print("Error 1: the nine code in this product is not found !!!"+ \
        "  The url is :" + str(url))
        #successful excuted try block when open url with multiple product with one item number
        try:
            title_regex = re.compile(r'<div class="product-tile-set.*?</div>',re.DOTALL)
            title = title_regex.findall(text)
            # print(len(title))

            title_str = ''.join(title)
            prod_regex = re.compile(r'https://www.costco.com.*?.html',re.DOTALL)
            prod_list = prod_regex.findall(title_str)
            url = prod_list[0]
            return "0","0",url,"0","0","0","0","0","0","0","0","0"

        except:
            d_9 = [0]
    d_9 = str(d_9[0])

    soup = BeautifulSoup(text, 'html.parser')
    #find description
    res2 = soup.find("div",{"id":"product-details"})
    res = soup.find("div",{"class":"product-info-description"})
    price_text = soup.find("div",{"id":"pull-right-price"})
    try:
        shadow_s = driver1.execute_script('return document.querySelector("#syndi_powerpage > div").shadowRoot.querySelector("div")')
        shadow = shadow_s.get_attribute("innerHTML")
        # print(type(shadow))
        # print(shadow)
        # print("shadow!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #    input("cccccccccccccccccccccccccccccccccccccccccccc")
    except :
        shadow = ""
    
    if(shadow == ""):
        if(res == None):
            return "-1","-1",url,"-1","-1","-1","-1","-1","-1","-1","-1","-1"
        else:
            description_s = res.get_text().split()
            description_s = " ".join(description_s)
    else:
        if(shadow_s == None):
            return "-1","-1",url,"-1","-1","-1","-1","-1","-1","-1","-1","-1"
        else:
            description_s = shadow_s.get_attribute("innerText").split()
            description_s = " ".join(description_s)

    product_detail_s = res2.get_text().split()
    product_detail_s = " ".join(product_detail_s)
    # string_encode = str.encode("ascii", "ignore").decode()

    d_7_s = soup.find("p",{"id":"product-body-item-number"})
    d_7_regex = re.compile(r'\d{7}?')
    d_7 = d_7_regex.findall(str(d_7_s))
    if(len(d_7) ==0):
        d_7_s = soup.find("p",{"id":"product-body-item-number"})
        d_7_regex = re.compile(r'\d{6}?')
        d_7 = d_7_regex.findall(str(d_7_s))
    if(len(d_7) == 0):
        print("Error 2: the item code in this product is not found !!!"+ \
        "  The url is :" + str(url))
        d_7 = [0]
    d_7 = str(d_7[0])

    model_s = soup.find("p",{"id":"product-body-model-number"})
    
    if(model_s == None ):
        model_s = ""
    else:

        model_s = model_s.get_text()
        model_s = model_s.replace("Model","")
        model_s = model_s.strip()

    description_s = description_s.encode("ascii", "ignore").decode()
    product_detail_s = product_detail_s.encode("ascii", "ignore").decode()

    features_csv = soup.find("ul",{"class":"pdp-features"})
    if(features_csv == None):
        features_csv = ""
    else:
        features_csv = features_csv.get_text().split()
        features_csv = " ".join(features_csv)

    if(price_text == None):
        price_text_csv = ""
    else:
        price_text_csv = price_text.get_text().split()
        price_text_csv = " ".join(price_text_csv)
    return d_7,d_9,url,description_s,product_detail_s,model_s,price_text,res,res2,shadow,features_csv,price_text_csv



def searchOutProduct(dir_file_name):
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    folder_entered = "./"+dir_file_name+"/"+"download_csv"
    dir_list = os.listdir(folder_entered)

    # driver1 = webdriver.Chrome(cho_path)

    for file_found in dir_list:
        if file_found.endswith(".csv"):
            if not os.path.exists("./result/"+dir_file_name+"/" +d4):
                os.makedirs("./result/"+dir_file_name+"/" +d4)

            #format is ./result/computer&electrios/feb-02-22/

            save_file = "./result/"+dir_file_name+"/" +d4+"/"+file_found+"_information.csv"

            file_path = folder_entered +"/"+ file_found
            df = pd.read_csv(file_path)
            df2 = pd.read_csv("database.csv")
            for index, row in df.iterrows():
                if 'Costco Item #' in df.columns:
                    item_number = row["Costco Item #"] 
                else:
                    item_number = row["Item #"] 
                print("Item number working on is " + str(item_number))
                # input("check")
                if item_number in dict_product.keys():
                    df.loc[index,"Model_scan"] = dict_product[item_number][0]
                    df.loc[index,"URL"] = dict_product[item_number][1]
                    df.loc[index,"product_detail"] = dict_product[item_number][2]
                    df.loc[index,"description"] = dict_product[item_number][3]
                    df.loc[index,"features"] = dict_product[item_number][4]
                    df.loc[index,"price_online"] = dict_product[item_number][5]
                    df.to_csv(save_file, index=False)
                    print("Item updated according to previous data")
                    print(" ------------------------------------------------------------ ")
                    continue

                nine_code= df2[df2["item_code"]==item_number]["nine_code"]
                if(nine_code.empty):
                    print("File not founded in database " + str(item_number))
                    http_str = "https://www.costco.com/CatalogSearch?dept=All&keyword="+ str(item_number)
                    driver1 = webdriver.Chrome(cho_path)
                    driver1.get(http_str)
                    sleep(1)
                    text = driver1.page_source
                    
                    d_7,d_9,url,description_s,product_detail_s,model_s,price_text,res,res2,shadow,features_csv,price_text_csv = getInformation(text,item_number,driver1)
                    #only happen when open url with multiple product with one item number

                    # print(d_7)
                    # print(d_9)
                    # print(description_s)
                    # input("-------------------------")

                    if(d_7 =="-1" and d_9 =="-1" and description_s =="-1"):
                        dict_product[item_number] = ["NA","NA","NA","NA","NA","NA"]
                        df.loc[index,"Model_scan"] ="NA"
                        df.loc[index,"URL"] = "NA"
                        df.loc[index,"product_detail"] = "NA"
                        df.loc[index,"description"] = "NA"
                        df.loc[index,"features"] = "NA"
                        df.loc[index,"price_online"] = "NA"
                        df.to_csv(save_file, index=False)
                        print("Item is not found in the online search")
                        print(" ------------------------------------------------------------ ")
                        driver1.quit()
                        continue


                    if(d_7 =="0" and d_9 =="0" and description_s =="0"):
                        # driver1.quit()
                        # print("-------------------------------------")
                        print("enter the mutiple page of product")
                        driver1 = webdriver.Chrome(cho_path)
                        driver1.get(url)
                        sleep(1)
                        text = driver1.page_source
                        d_7,d_9,url,description_s,product_detail_s,model_s,price_text,res,res2,shadow,features_csv,price_text_csv = getInformation(text,item_number,driver1)

                    # except:
                    #     #only happen when cosco.com can't find the product and result "We're sorry. We were not able to find a match." or "we weren't able to find the product you were looking fo"
                    #     # dict_product[item_number] = ["","","",""]
                    #     df.loc[index,"Model_scan"] ="NA"
                    #     df.loc[index,"URL"] = "NA"
                    #     df.loc[index,"product_detail"] = "NA"
                    #     df.loc[index,"description"] = "NA"
                    #     df.loc[index,"features"] = "NA"
                    #     df.loc[index,"price_online"] = "NA"
                    #     df.to_csv(save_file, index=False)
                    #     print("Item is not found in the online search")
                    #     print(" ------------------------------------------------------------ ")
                    #     driver1.quit()
                    #     continue

                    download_path ="./"+"Download_html"+"/"+ d_9+ ".html"
                    driver1.quit()

                    with open(download_path,"a", encoding="utf-8") as myfile:
                        myfile.write(str(res2))
                        # myfile.write(d_7_header)
                        myfile.write(str(price_text))
                        myfile.write(shadow)
                        myfile.write(str(res))

                    scan_infor =(d_9,item_number,str(url),"")
                    with open('./database.csv', 'a', newline='') as outputcsv:
                        writer = csv.writer(outputcsv)
                        writer.writerow(scan_infor)
                    outputcsv.close()

                    # input("chekc !!! database write !!")

                    dict_product[item_number] = [model_s,url,product_detail_s,description_s,features_csv,price_text_csv]
                    #write to package
                    df.loc[index,"Model_scan"] = dict_product[item_number][0]
                    df.loc[index,"URL"] = dict_product[item_number][1]
                    df.loc[index,"product_detail"] = dict_product[item_number][2]
                    df.loc[index,"description"] = dict_product[item_number][3]
                    df.loc[index,"features"] = dict_product[item_number][4]
                    df.loc[index,"price_online"] = dict_product[item_number][5]
                    print("Item added by found online")
                    print(" ------------------------------------------------------------ ")
                    df.to_csv(save_file, index=False)
                    # print(dict_product)
                    # input("dictionary product check !!")

                else:
                    print("Find file in local database " + str(item_number))
                    nine_code = nine_code.astype(int)
                    file_to_find = nine_code.to_string(index=False) + ".html"
                    Download_path = curren_path+ "\Download_html"
                    for root, dirs, files in os.walk(Download_path):
                        # print("file to find ----------------------------") 
                        # print(file_to_find)
                        # print("files : ----------------------------")
                        # print(files)
                        # input("check !!!!!!!!!!")
                        if file_to_find in files:
                            # input("check 2222")
                            file_location = os.path.join(root, file_to_find)
                            print("Founded file store at : "+file_location)
                            # input("check!!!!")
                            driver1 = webdriver.Chrome(cho_path)
                            driver1.get(file_location)
                            sleep(1)
                            text = driver1.page_source
                            d_7,d_9,url,description_s,product_detail_s,model_s,price_text,res,res2,shadow,features_csv,price_text_csv = getInformation(text,item_number,driver1)
                            driver1.quit()

                            # if(int(d_7) != item_number ):
                            #     print("--------------------------------------------")
                            #     print(url)
                            #     print("--------------------------------------------")
                            #     input(" Critcal error !!, d_7 not equal to item_number")
                                
                            dict_product[item_number] = [model_s,url,product_detail_s,description_s,features_csv,price_text_csv]
                            # print(dict_product)
                            df.loc[index,"Model_scan"] = dict_product[item_number][0]
                            df.loc[index,"URL"] = dict_product[item_number][1]
                            df.loc[index,"product_detail"] = dict_product[item_number][2]
                            df.loc[index,"description"] = dict_product[item_number][3]
                            df.loc[index,"features"] = dict_product[item_number][4]
                            df.loc[index,"price_online"] = dict_product[item_number][5]
                            print("Item updated by found on local database")
                            print("------------------------------------------------------------ ")
                            df.to_csv(save_file, index=False)
    driver1.quit()
    

    #adding information to end of the file of each ***-**.csv_information.csv   format is 
    # ("Six code","Current bid","Minimum bid Interval","Shipment cost","Bid close time","Costco code","Webpage url","Ext. Retail","Condition","percentage")
    # (x,x,x,x,x,x,x)
    print("Adding data to each .csv_information.csv file")
    # dir_file_name

    folder_entered_2 = "./"+dir_file_name+"/"+"download_csv"
    result_infor_file = "./"+dir_file_name + "/result/information-%s.csv"%(dir_file_name)
    dir_list = os.listdir(folder_entered_2)

    header = ("Six code","Current bid","Minimum bid Interval","Shipment cost","Bid close time","Costco code","Webpage url","Ext. Retail","Condition","percentage")

    df = pd.read_csv(result_infor_file)

    for file_found in dir_list:
        save_file = "./result/"+dir_file_name+"/" +d4+"/"+file_found+"_information.csv"
        file_path = "./"+folder_entered_2 +"/"+ file_found

        file_name_without_extension = os.path.splitext(file_found)[0]
        row_infor = df[df["Costco code"]==file_name_without_extension]
        cur = df[df["Costco code"]==file_name_without_extension]["Current bid"]
        ext = df[df["Costco code"]==file_name_without_extension]["Ext. Retail"]
        # percentage = cur/ext

        ext_0 = ext.iloc[0]
        cur_0 = cur.iloc[0]
        percentage = cur_0/ext_0

        # print("------------------------------------------------------------ ")
        # print("File found is "+ file_found)
        # print(ext)
        # print(cur)
        # print(percentage)
        percentage = float(percentage)
        percentage_str = "{:.0%}".format(percentage)
        row_infor["percentage"] = percentage_str
        with open(save_file, 'a', newline='') as outputcsv:
            writer = csv.writer(outputcsv)
            writer.writerow(header)
            # writer.writerow(row_infor)
        outputcsv.close()

        row_infor.to_csv(save_file,mode='a', index=False, header=False)
    
    store_excl = "./result/"+dir_file_name+"/" +d4+"/"+"excel_file"

    if not os.path.exists(store_excl):
        os.makedirs(store_excl)

    dir_list_2= os.listdir("./result/"+dir_file_name+"/" +d4)

    #pip install openpyxl 
    #file found has a format of "abc.csv_information.csv", in order to get file name "abc", we need to do two times of os.path.splitext

    for file_found in dir_list_2:
        if file_found.endswith(".csv"):
            file_name_without_extension = os.path.splitext(file_found)[0]
            file_name_without_extension2 = os.path.splitext(file_name_without_extension)[0]

            data = pd.read_csv("./result/"+dir_file_name+"/" +d4+"/"+file_found)
            # print(store_excl+"/"+file_name_without_extension2+".xls")
            data.to_excel(store_excl+"/"+file_name_without_extension2+".xlsx", index=None, header=True)

    files = os.listdir(store_excl)
    df = pd.DataFrame()
    for file in files:
        if file.endswith('.xlsx'):
            df = df.append(pd.read_excel(store_excl+"/"+file), ignore_index=True) 
    df.head() 
    df.to_excel(store_excl+'/All_Data_Combined.xlsx')

    print("------------------------------------------------------------ ")
    print(" ALL PROGRAM FINISHED !! ")



def main():
    global root 
    root = Tk()
    root.title('Function')
    root.geometry("900x300")
    # frmLT = Frame(width=500, height=320, bg='white')
    # frmLT.grid(row=0, column=0,padx=1,pady=3)

    # first_function = Button(root, text="Scan URL and create download list", command=first_print).grid(row=0, column=0, sticky=W)
    # second_function = Button(root, text="Download and extract feature", command=second_f).grid(row=0, column=1, sticky=W)
    # third_function = Button(root, text="Combine and get unique item", command=third_f).grid(row=0, column=2, sticky=W)
    result_text = tk.StringVar()
    list_value = tk.StringVar()
    list_value.set(("Computer & tablets", "Consumer electronics","hardware","Apparel","Cookware","Domestics","Food & Sundries",
    "Footwear","Garden-Patio","Health & beauty","Home Comfort","Home furnishings","Luggage","Major appliances","Mixed Lots",
    "Printers","Rugs","Seasonal","Small appliances","Sporting goods","Vacuums"))
    

    global url_list
    url_list = ["https://bstock.com/costco/all-inventory/computers-tablets/?limit=48",
            "https://bstock.com/costco/all-inventory/small-electronics/?limit=48",
            "https://bstock.com/costco/all-inventory/hardware/?limit=48",
            "https://bstock.com/costco/all-inventory/apparel/?limit=48",
            "https://bstock.com/costco/all-inventory/cookware/?limit=48",
            "https://bstock.com/costco/all-inventory/domestics/?limit=48",
            "https://bstock.com/costco/all-inventory/sundries/?limit=48",
            "https://bstock.com/costco/all-inventory/footwear/?limit=48",
            "https://bstock.com/costco/all-inventory/garden-patio/?limit=48",
            "https://bstock.com/costco/all-inventory/health-beauty/?limit=48",
            "https://bstock.com/costco/all-inventory/home-comfort/?limit=48",
            "https://bstock.com/costco/all-inventory/home-furnishings/?limit=48",
            "https://bstock.com/costco/all-inventory/luggage/?limit=48",
            "https://bstock.com/costco/all-inventory/major-appliances/?limit=48",
            "https://bstock.com/costco/all-inventory/mixed-lots/?limit=48",
            "https://bstock.com/costco/all-inventory/printers/?limit=48",
            "https://bstock.com/costco/all-inventory/rugs/?limit=48",
            "https://bstock.com/costco/all-inventory/seasonal/?limit=48",
            "https://bstock.com/costco/all-inventory/small-appliances/?limit=48",
            "https://bstock.com/costco/all-inventory/toys-sporting-goods/?limit=48",
            "https://bstock.com/costco/all-inventory/vacuums/?limit=48"]

    f1 = Label(root, text="Choose a catagry to contiune")#.grid(row=1, column= 0,sticky=W) 
    #f1.pack()
    f1.grid(row=1, column= 0,sticky=W) 

    global f2

    f2 = tk.Listbox(root, listvariable=list_value)#.grid(row=1,column= 1,sticky=W)
    # f2.pack()
    f2.grid(row=1, column= 1,sticky=W) 

    f3 = tk.Button(root, text="Enter", command=start_working)#.grid(row=1, column=2, sticky=W)
    #f3 = tk.Button(root, text="Enter").grid(row=1, column=2, sticky=W)
    # f3.pack()
    f3.grid(row=1, column= 2,sticky=W) 
    result_text.set("")
    result = tk.Label(root, textvariable=result_text)#.grid(row=2, column= 0,sticky=W)
    #result.pack()
    result.grid(row=4, columnspan = 4,sticky=W)
    result.update()

    k1 = Label(root, text="Or Enter URL")#.grid(row=1, column= 0,sticky=W) 
    k1.grid(row=2, column= 0,sticky=W) 

    global k2
    k2 = Text(root,height = 1,width = 25)
    k2.grid(row=2, column= 1,sticky=W) 

    root.mainloop()

main()


# def first_print():
    

