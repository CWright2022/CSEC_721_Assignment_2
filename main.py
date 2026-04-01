#!/usr/bin/env python3
# CSEC721 Homework/Lab 2: Homomorphic Encryption
# Cayden Wright, Spring 2026
import tenseal as ts
import time
import csv

NUM_RECORDS = 10

def getPrediction(enc_values):
    # This runs on the server - it performs these values without decrypting them
    # 0.5581×age + 0.0048×trestbps + 0.0044×chol - 0.0036×thalach + 0.1290×oldpeak - 28.9796
    pre_prediction_time = time.time()
    result = (0.5581 * enc_values[0] + 
              0.0048 * enc_values[3] + 
              0.0044 * enc_values[4] - 
              0.0036 * enc_values[7] + 
              0.1290 * enc_values[9] - 
              28.9796)
    post_prediction_time = time.time()
    duration = post_prediction_time - pre_prediction_time
    return result, duration


def main():
    with open ("dataset/heart.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        i = 0
        for record in reader:
            # cap records at 10
            if i >= NUM_RECORDS:
                break
            # each person generates their own keys
            context = ts.context(ts.SCHEME_TYPE.CKKS, 
                         poly_modulus_degree=8192, 
                         coeff_mod_bit_sizes=[60, 40, 40, 60])
            context.generate_galois_keys()
            context.global_scale = 2**40
            
            # Encrypt (timing this operation)
            pre_enc_time = time.time()
            enc_values = [ts.ckks_vector(context, [float(val)]) for val in record]
            post_enc_time = time.time()
            enc_duration = post_enc_time - pre_enc_time
            
            # this "sends the values to the server" - server does not know true values
            prediction, pred_duration = getPrediction(enc_values)
            
            # Decrypt (timing this too)
            pre_dec_time = time.time()
            dec_prediction = prediction.decrypt()[0]
            post_dec_time = time.time()
            dec_duration = post_dec_time - pre_dec_time
            binary_prediction = "HIGH RISK" if dec_prediction >0 else "LOW RISK"
            
            print(f"Record {i}: Prediction = {dec_prediction} ({binary_prediction}) - Encryption: {enc_duration:.4f} Prediction: {pred_duration:.4f} Decryption: {dec_duration:.4f}")
            i += 1

if __name__ == "__main__":
    main()