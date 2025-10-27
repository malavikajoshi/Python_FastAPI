import json
import pprint
from fastapi import FastAPI
from pydantic import BaseModel


with open("/mnt/c/Users/joshi/Downloads/shipping_data.json") as f:
    shipping_api = json.load(f)

# print("Shipping API data:", shipping_api)

app=FastAPI()
class Shipping_data(BaseModel):
    order_id: str
    customer_name: str
    region: str
    shipping_address: str
    weight_kg: float
    shipping_cost_usd: float
    status: str
    order_date: str
    delivery_date: str

# pprint.pprint(shipping_api)

# 1. Build a GET endpoint, that returns record based on the f.
@app.get("/getUsingOrderid/{_id}")
def getDataByOrderId(_id: str):
    if  shipping_api:
        _customer_id_upper = _id.strip().upper()
        for rec1 in shipping_api:
            if rec1.get("order_id","").strip().upper() == _customer_id_upper:
                return rec1
        return {"message": "Data doesn't exist"}
    else:
        return {"message": "No data available"}
    

# 2.Build a GET endpoint, that returns all customer_names based on the region.   

customer_names=[]
@app.get("/customer-data/{_region}")
def GetDataRegion(_region:str):
    if shipping_Api:
        __region=_region.strip().upper()
        for rec2 in shipping_Api:
            if rec2.get("region").strip().upper()==__region:
                customer_names.append(rec2.get("customer_name"))
        return customer_names
    else:
        return {"data not exist"}
        
# @app.get("/getDetails/{_customer_name}")
# def getDetailsByCustomerNames(_customer_name: str):
#     if shipping_api:
#         _customer_name_upper = _customer_name.strip().upper()
#         for rec in shipping_api:
#             if rec.get("customer_name","").strip().upper() == _customer_name_upper:
#                 return rec
#         return {"message": "Data doesn't exist"}
#     else:
#         return {"message": "No data available"}


    
# 3. Build a PUT endpoint, that enters new record in into the database (for now file)
@app.put("/insert_data/")
def insert_data(_shipping: Shipping_data):
    new_record = _shipping.dict()
    shipping_api.append(new_record)
    for rec in shipping_api:
        if rec.get("order_id") == new_record["order_id"]:
            return {"message": f"Order ID {new_record['order_id']} already exists"}

    shipping_api.append(new_record)
    with open("shipping_data.json", "w") as f:
        json.dump(shipping_api, f, indent=4)
    
    return {"message": "Data inserted successfully", "record": new_record}


# 4. Build a POST endpoint, that updates record based on the order_id.
@app.post("/post_data")
def update_data(_order_id: str, updated_dt:Shipping_data):
    _updated_dt = updated_dt.dict()
    if shipping_api:
        for rec in shipping_api:
            if rec.get("order_id") ==_order_id:
                rec['customer_name'] = _updated_dt['customer_name']
                rec['region'] = _updated_dt['region']
                rec['shipping_address'] = _updated_dt['shipping_address']
                rec['weight_kg'] = _updated_dt['weight_kg']
                rec['shipping_cost_usd'] = _updated_dt['shipping_cost_usd']
                rec['status'] = _updated_dt['status']
                rec['order_date'] = _updated_dt['order_date']
                rec['delivery_date'] = _updated_dt['delivery_date']
                with open("/mnt/c/Users/joshi/Downloads/shipping_data.json", "w") as f:
                    json.dump(shipping_api, f, indent=4)
                return {"message":"Shipping data updated sucessfully", "data":rec}
        else:
            return {"message":"No relevent Shipping data found to update"}
    else:
        return {"message":"Data doesn't exists"}

# 5.Build a DELETE endpoint, that deletes the record based on the order_id.
@app.delete("/delete_data/{_order_id}")
def delete_data(_order_id:str):
    if shipping_api:
        for rec in shipping_api:
            _order_id_upper = _order_id.strip().upper()
            if rec.get("order_id","").strip().upper() ==_order_id_upper:
                print('found')
                shipping_api.remove(rec)
                with open("/mnt/c/Users/joshi/Downloads/shipping_data.json", "w") as f:
                    json.dump(shipping_api, f, indent=4)

                return {"message": "data successfully deleted"}
        return {"message": "data doesn't exists"}
    else:

        return {"message": "database doesn't exists"}
