# CSEC721 Homework/Lab 2: Homomorphic Encryption
# Cayden Wright, Spring 2026
import numpy as np
from Pyfhel import Pyfhel
import csv

NUM_RECORDS = 10

def getPrediction(enc_values):
    # Scaled integer coefficients (multiplied by 10000)
    # f(·) = 0.5581×age + 0.0048×trestbps + 0.0044×chol - 0.0036×thalach + 0.1290×oldpeak - 28.9796
    result = (5581 * enc_values[0] + 
              48 * enc_values[3] + 
              44 * enc_values[4] - 
              36 * enc_values[7] + 
              1290 * enc_values[9])
    return result


def main():
    with open ("dataset/heart.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        i=0
        for record in reader:
            if i >= NUM_RECORDS:
                break
            HE = Pyfhel()
            HE.contextGen(scheme='bgv', n=2**14, t_bits=20)
            HE.keyGen()
            enc_values = [HE.encrypt(int(float(val))) for val in record]
            prediction = getPrediction(enc_values)
            dec_prediction = HE.decrypt(prediction)
            print(f"Record {i}: Prediction = {dec_prediction}")
            i += 1

if __name__ == "__main__":
    main()