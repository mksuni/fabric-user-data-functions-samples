
# Add a Connection to warehouse and lakehouse to your user data function 
# Example of using a FabricItemInput to query a Warehouse 
#  and then write the data to a csv in a Lakehouse
# Replace alias for the warehouse and lakehouse 
 
# Requirements.txt changes required:
#     uncomment the line "Pandas"
# Imports Statement changes required:
#     import json




 @app.fabric_item_input(argName="myWarehouse", alias="<My Warehouse Alias>")
 @app.fabric_item_input(argName="myLakehouse", alias="<My Lakehouse Alias>")
 @app.function("query_warehouse_and_write_to_csv")
 def query_warehouse_and_write_to_csv(myWarehouse: fabric.functions.FabricSqlConnection, myLakehouse: fabric.functions.FabricLakehouseClient) -> fabric.functions.UdfResponse:

     whSqlConnection = myWarehouse.connect()

     cursor = whSqlConnection.cursor()
     cursor.execute(f"SELECT * FROM (VALUES ('John Smith',  31) , ('Kayla Jones', 33)) AS Employee(EmpName, DepID);")

     rows = [x for x in cursor]
     columnNames = [x[0] for x in cursor.description]
     csvRows = []
     csvRows.append(','.join(columnNames))

      Turn the rows into comma separated values, and then upload it to Employees<timestamp>.csv
     for row in rows:
         csvRows.append(','.join(map(str, row)))

     lhFileConnection = myLakehouse.connectToFiles()
     csvFileName = "Employees" + str(round(datetime.now().timestamp())) + ".csv"
     csvFile = lhFileConnection.get_file_client(csvFileName)
     csvFile.upload_data('\n'.join(csvRows), overwrite=True)

      Turn the rows into a json object
     values = []

     for row in rows:
         item = {}
         for prop, val in zip(columnNames, row):
             if isinstance(val, (datetime, date)):
                 val = val.isoformat()
             item[prop] = val
         values.append(item)
    
     valJSON = json.dumps({"message": "File {} is written to {} Lakehouse. You can delete it from the Lakehouse after trying this sample.".format(csvFileName, myLakehouse.alias_name),
                           "values": values})

     cursor.close()
     whSqlConnection.close()
     csvFile.close()
     lhFileConnection.close()

     return fabric.functions.UdfResponse(valJSON)