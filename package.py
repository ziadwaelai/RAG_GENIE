from pymilvus import connections, utility

try:
    connections.connect("default", host="localhost", port="19530")
    print("Connected successfully!")
    print("Collections:", utility.list_collections())
except Exception as e:
    print(f"Connection failed: {e}")