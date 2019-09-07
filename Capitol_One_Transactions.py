import json
import requests
#Delete data: curl -X DELETE --header "Accept: application/json" "http://api.reimaginebanking.com/data?type=Customers&key=73672856d8a05baa8f6f7e8a158dc9c4"
requesturl='http://api.reimaginebanking.com/customers?key=73672856d8a05baa8f6f7e8a158dc9c4'
from datetime import datetime


def store_data_and_name(data):
    store_local=[]
    keyid=data['_id']
    keyname=data['first_name']+data['last_name']
    store_local.append([keyid,keyname])
    #print(True)
    return(store_local)

def create_Customer_Account(User_data,url):
    headers = {'content-type': 'application/json','Accept': 'application/json'}
    r = requests.post(url, json=dT, headers=headers)
    #print(r.json()['objectCreated'])
    print(r.json()['message'])
    store_data_and_name(r.json()['objectCreated'])
    return(r.status_code, r.json())
dT={"first_name":"Xander","last_name":"Moswaert",
 "address":{"street_number":"21636","street_name":"State Route 644","city":"Jetersville",
            "state":"VA","zip":"23083"}}
#x=create_Customer_Account(dT,requesturl)

def clear_data(type_var):
    request_url='http://api.reimaginebanking.com/data?type='+type_var+'&key=73672856d8a05baa8f6f7e8a158dc9c4'
    r=requests.delete(request_url)
    if r.status_code==204:
        print('Cleared all Data')
    else:
        print('Some sort of error.')
    return(r.status_code)
#x=clear_data('Customers')

def my_account_details(iD):
    request_url='http://api.reimaginebanking.com/customers/5d7392313c8c2216c9fcad27?key=73672856d8a05baa8f6f7e8a158dc9c4'
    headers = {'Accept': 'application/json'}
    r = requests.get(request_url,headers)
    j = json.loads(r.text)
    if r.status_code==200:
        print("Success!")
    else:
        print('Some sort of error')
    return(j)
#r=my_account_details("5d7392313c8c2216c9fcad27")

def scan_my_records():
    var=[]
    request_url='http://api.reimaginebanking.com/customers?key=73672856d8a05baa8f6f7e8a158dc9c4'
    headers = {'Accept': 'application/json'}
    r = requests.get(request_url,headers)
    if r.status_code==200:
        x=json.loads(r.text)
        for i in range(len(x)):
            var.append(x[i]['first_name']+' '+x[i]['last_name'])
        print("Success!")
    else:
        print('Some sort of error')
   
    return(var)
#x=scan_my_records()

def search_user_id(namex):
    names=[]
    request_url='http://api.reimaginebanking.com/customers?key=73672856d8a05baa8f6f7e8a158dc9c4'
    headers = {'Accept': 'application/json'}
    r = requests.get(request_url,headers)
    if r.status_code==200:
        print('Got the data!')
    r=json.loads(r.text)
    for i in range(len(r)):
        name=r[i]['first_name']+' '+r[i]['last_name']
        ids=r[0]['_id']
        names.append((name,ids))
    #print(namex)
    for i in range(len(names)):
        #print(names[i])
        if names[i][0]==namex:
            print("Condition satisfied")
            #print('Loop in')
            return(names[i][1])
    return(0)
#x=search_user_id('Ismail Myert')
    

dT={
  "type": "Credit Card",
  "nickname": "Spidey",
  "rewards": 0,
  "balance": 1000,
  "account_number": "1451246580123476"
}
def create_user_accounts(account_data,ids):
    request_url='http://api.reimaginebanking.com/customers/'+ids+'/accounts?key=73672856d8a05baa8f6f7e8a158dc9c4'
    headers = {'content-type': 'application/json','Accept': 'application/json'}
    r = requests.post(request_url, json=dT, headers=headers)
    if r.status_code==201:
        print("Succesful account creation!")
    else:
        print("Some error occured!")
#create_user_accounts(dT,'5d73a56e3c8c2216c9fcad41')


def account_iD(upiID):
    customer_IDS=[]
    request_url='http://api.reimaginebanking.com/accounts?type=Credit%20Card&key=73672856d8a05baa8f6f7e8a158dc9c4'
    headers = {'Accept': 'application/json'}
    r = requests.get(request_url,headers)
    for i in json.loads(r.text):
        if upiID==i['nickname']:
            #print('found UPI')
            return(i['_id'])
    return(0)
    

def create_transaction(senderUPI,recieverUPI,amount,payment_description):
    #iD_sender=search_user_id(sender)
    #iD_reciever=search_user_id(reciever)
    payeeid=account_iD(senderUPI)
    #print(payeeid)
    request_url='http://api.reimaginebanking.com/accounts/'+payeeid+'/transfers?key=73672856d8a05baa8f6f7e8a158dc9c4'
    #print(request_url)
    payingid=account_iD(recieverUPI)
    #print(payingid)
    data={"medium": "balance","payee_id": payeeid,"transaction_date": "{:%B %d, %Y}".format(datetime.now()),
          "status": "pending","description": payment_description,"amount": amount}
    headers = {'content-type': 'application/json','Accept': 'application/json'}
    r = requests.post(request_url, json=data, headers=headers)
    if r.status_code==201:
        print('Transaction Succesful!')
    else:
        print('Something is not good.')
    return(r)
    
#r=create_transaction('spidey','Spidey',200,'Your yesterday money')

def make_a_purchase(purchase_acc,merchant_acc,purchase_items,desc_message):
    headers = {'content-type': 'application/json','Accept': 'application/json'}
    payeeid=account_iD(purchase_acc)
    merchantid=account_iD(merchant_acc)
    purchase_list={'5L Milk':20,'Burger':5,'Pizza Large':12,'Drinks':4,'Lunch':10,'Stationary kit': 3,'Shaving Kit': 3}
    net_amount=0
    for items in purchase_items:
        net_amount+=purchase_list[items]
    print(net_amount)
    request_url='http://api.reimaginebanking.com/accounts/'+payeeid+'/transfers?key=73672856d8a05baa8f6f7e8a158dc9c4'
    data={"medium": "balance","payee_id": merchantid,"transaction_date": "{:%B %d, %Y}".format(datetime.now()),"status": "pending",
          "description": desc_message,"amount": net_amount}
    headers = {'content-type': 'application/json','Accept': 'application/json'}
    r = requests.post(request_url, json=data, headers=headers)
    return(r)
#x=make_a_purchase('spidey','Spidey',['Pizza Large','Shaving Kit'],'Shopping List')



    
    
    

    


    

