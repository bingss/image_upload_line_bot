



# 儲存 ID 的函數
def save_id(id,file_path):
    with open(file_path, "a") as file:
        file.write(f"{id}\n")

# 刪除 ID 的函數
def delete_id(id,file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    with open(file_path, "w") as file:
        for line in lines:
            if line.strip() != id:
                file.write(line)

# 讀取所有 ID 的函數
def read_all_ids(file_path):
    with open(file_path, "r") as file:
        return set(line.strip() for line in file.readlines())
    