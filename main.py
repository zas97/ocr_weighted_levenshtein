import easyocr
import doctr
import pytesseract
import numpy as np
import Levenshtein
from src.image_generator import rand_string, random_chars_generator
from src import count_editions2distances
import string
import pandas as pd
import os


def predict_doctr(model, img):
    return model([np.array(img)])[0][0]

def predict_easyocr(model, img):
    return model.recognize(np.array(img))[0][1]

def predict_tesseract(model, img):
    return pytesseract.image_to_string(img, config="--psm 8 -c load_system_dawg=0 load_freq_dawg=0")[:-1]

def get_edit_op(op, pred, truth):
    op_nature, pos_pred, pos_truth = op
    if op_nature == "delete":
        return (op_nature, pred[pos_pred])
    if op_nature == "insert":
        return (op_nature, truth[pos_truth])
    if op_nature == "replace":
        return (op_nature, pred[pos_pred], truth[pos_truth])
    raise f"{op_nature} not recognized"


def run_ocrs(list_ocrs, img_txt_generator):
    rows = []
    for it, (img, lbl) in enumerate(img_txt_generator):
        
        name_img = rand_string(20, 25, string.ascii_letters + string.ascii_uppercase)
        img_path = f"./data/{name_img}.jpg"
        img.save(img_path)
        
        for name_ocr, model, predict_func in list_ocrs:
            pred = predict_func(model, img)
            new_row = {
                "ocr": name_ocr,
                "pred": pred,
                "truth": lbl,
                "img_path": img_path
            }
            rows.append(new_row)
    
    df = pd.DataFrame.from_records(rows)
    return df

def edit_ops_from_ocr_experiment(df):
    op2count = {}
    for pred, label in df[["pred", "truth"]].values:
        pred = pred.strip()
        label = label.strip()
        ops = Levenshtein.editops(pred, label)
        for op in ops:
            parsed_op = get_edit_op(op, pred, label)
            op2count[parsed_op] = op2count.get(parsed_op, 0) + 1
    return op2count

def symmetrize_replace(op2count):
    symetric_op2count = op2count.copy()
    for op, count in op2count.items():
        if op[0] == "replace":
            symetric_op = (op[0], op[2], op[1])
            val_symetric = op2count.get(symetric_op, 0)
            new_val = (val_symetric + count) / 2
            symetric_op2count[op] = new_val
            symetric_op2count[symetric_op] = new_val
    return symetric_op2count




if __name__ == "__main__":
    folder_weights = "data/weights/exponential"
    # count = 50000
    # ocrs = [("easy_ocr", easyocr.Reader(["en", "fr"], gpu=False), predict_easyocr),
    #         ("doctr", doctr.models.recognition_predictor(pretrained=True), predict_doctr),
    #         ("tesseract", None, predict_tesseract)
    #         ]
    # df_res = run_ocrs(ocrs, random_chars_generator(count))
    # df_res.to_csv("experiment.csv")
    
    df_res = pd.read_csv("experiment.csv", index_col=0)
    df_res.fillna("", inplace=True)
    op2count = edit_ops_from_ocr_experiment(df_res)
    symetric_op2count = symmetrize_replace(op2count)
    distances = count_editions2distances.exponential_count2distance(symetric_op2count)
    insert_costs, delete_costs, substitute_costs = count_editions2distances.distances2numpy_format(distances)
    os.makedirs(folder_weights, exist_ok=True)
    count_editions2distances.save_distances2file(folder_weights, insert_costs, delete_costs, substitute_costs)
    
    
    
    
    