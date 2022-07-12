
import numpy as np

def distances_as_params(insert_cost, delete_cost, subs_cost):
    return {
        "substitute_costs": subs_cost, 
        "insert_costs": insert_cost, 
        "delete_costs": delete_cost
    }

def folder2distances(folder):
    return (
        np.load(folder + "/insert.npy"),
        np.load(folder + "/delete.npy"),
        np.load(folder + "/subs.npy")
    )
        
            

def save_distances2file(folder, insert_costs, delete_costs, substitute_costs):
    np.save(folder + "/insert", insert_costs)
    np.save(folder + "/delete", delete_costs)
    np.save(folder + "/subs", substitute_costs)
    

def distances2numpy_format(op2distance):
    insert_costs = np.ones(128, dtype=np.float64)
    delete_costs = np.ones(128, dtype=np.float64)
    substitute_costs = np.ones((128, 128), dtype=np.float64)
    
    for op, d in op2distance.items():
        
        if op[0] == "replace":
            if ord(op[1]) > 128 or ord(op[2]) > 128:
                continue
            substitute_costs[ord(op[1]), ord(op[2])] = d
            
        if op[0] == "insert":
            if ord(op[1]) > 128 :
                continue
            insert_costs[ord(op[1])] = d
            
        if op[0] == "delete":
            if ord(op[1]) > 128:
                continue
            delete_costs[ord(op[1])] = d
            
    return insert_costs, delete_costs, substitute_costs

def using_mean(op2count):
    op2distance = {}
    mean_count = np.mean(list(op2count.values()))
    for op, count in op2count.items():
        distance = 1 / (count / mean_count)
        op2distance[op] = distance
    return op2distance


def exponential_count2distance(op2count, thresh=20, max_distance=1.5, coef_small=0.98, coef_big=0.999):
    op2distance = {}
    for op, count in op2count.items():
        if count <= thresh:
            distance = max_distance * (coef_small ** count)
        else:
            distance = coef_big ** count
        op2distance[op] = distance
        
    return op2distance
    
    

