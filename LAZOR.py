print("Hello")
import pickle

# Read pickle file
file_path = "/Users/huyinan/Desktop/PY/data.pickle" 
with open(file_path, "rb") as f:
    data = pickle.load(f)

# show data
print(type(data))  
print(data)  
import pickle
import matplotlib.pyplot as plt

# 读取 pickle 文件
file_path = "/Users/huyinan/Desktop/PY/data.pickle" 
with open(file_path, "rb") as file:
    data = pickle.load(file)
# Load the data from the pickle file