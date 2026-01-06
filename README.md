# FIKA Assistant UI
## Fine-Tuned Model (task 1)
https://huggingface.co/spaces/YT07/Iris
## Parameter-modified Model (task 2)
https://huggingface.co/spaces/YT07/Iris2
# Task2 Improvement ways
## model-centric approach  
e.g., tune hyperparameters, change the 
fine-tuning model architecture, etc

### 1. Leaning rate
 - change the learning rate in TrainingArguments as {1e-4, 2e-4, 5e-4}
 - lr_scheduler_type: not linear but "cosine" or "cosine_with_restarts".

 I learnt that if the training learning rate should be less if we plann to train few steps. So in the lab we chose 5e-4 as learning rate. Also the cosine gently curves down which is best for small dataset and short term fine tuning. so lr_scheduler_type is set to cosine in task 2. 
 ### 2. Train more epochs
 - set num_train_epochs = 3. 

The model is 30B only one epoch the loss doesn't decrease a lot. We think more epoch could help improving. Considering the dataset is small and the gpu resources is limited we didn't try this.
 ### 3. Increase batch size
 - batch_size = 2, grad_accum = 4  so effective batch is 8. 
 
 This often stabilizes training and improves generalization.
 In the task 2 we choose batch_size = 2, grad_accum = 8 to improve the effective batch size as double of before.
### 4. Lora_hyper parameter
- Higher r gives more capacity but more memory.
- r = 8, 16, 32
- lora_alpha = 16, 32, 64

In our lab, we choose r as 32 and lora_alpha as 32 because we got to know the lora_alpha is better to equal to r or is the two times of it. But too bigger values give slow training speed so we chose 32.
### 5. Lora dropput
- lora_dropout = 0.05  # or 0.1 

This can reduce overfitting when training for more epochs.
But in task 2 we didn't try to set becasue it is short-term fine tuning with small dataset.
## data-centric approach  
In our lab, we added 2 extra dataset `theblackcat102/sharegpt-english`
and `HuggingFaceH4/ultrachat_200k`. Then we standardrized each of them and combined 3 dataset together. Also we shuffled the datasets to let them in a better natural order. Then during mapping and training we found some of dataset don't have "conversations" which is exactly we need in training. So we filtered them before mapping. In the end we have the dataset that includes 150496 items which is much bigger than before.

# Results
Since the limited time and GPU resources, we only have trained the model for 60 steps and compare the loss with the training with original parameters and one dataset. Even only training 60 steps we could clearly saw the loss dropping greatly, reach to the 0.6 around in 60th steps while the loss of original training is arounf 1, sometimes each greater than 1.

| Step | Training Loss |
|-----:|--------------:|
| 1 | 0.646100 |
| 2 | 0.606900 |
| 3 | 0.642400 |
| 4 | 0.719300 |
| 5 | 0.672400 |
| 6 | 0.602900 |
| 7 | 0.686200 |
| 8 | 0.577000 |
| 9 | 0.547600 |
| 10 | 0.577100 |
| 11 | 0.579300 |
| 12 | 0.556600 |
| 13 | 0.677000 |
| 14 | 0.836500 |
| 15 | 0.763900 |
| 16 | 0.724700 |
| 17 | 0.773400 |
| 18 | 0.865300 |
| 19 | 0.761800 |
| 20 | 0.863500 |
| 21 | 0.743700 |
| 22 | 0.727600 |
| 23 | 0.906700 |
| 24 | 0.856400 |
| 25 | 0.775600 |
| 26 | 0.710100 |
| 27 | 0.930500 |
| 28 | 0.895300 |
| 29 | 0.897100 |
| 30 | 0.692100 |
| 31 | 0.922600 |
| 32 | 0.826400 |
| 33 | 0.776100 |
| 34 | 0.764500 |
| 35 | 0.734200 |
| 36 | 0.886000 |
| 37 | 0.746300 |
| 38 | 0.785400 |
| 39 | 0.724800 |
| 40 | 0.793100 |
| 41 | 0.676500 |
| 42 | 0.929900 |
| 43 | 0.709100 |
| 44 | 0.750300 |
| 45 | 0.730900 |
| 46 | 0.892700 |
| 47 | 0.781600 |
| 48 | 0.787300 |
| 49 | 0.785600 |
| 50 | 0.654900 |
| 51 | 0.733800 |
| 52 | 0.715500 |
| 53 | 0.650500 |
| 54 | 0.754000 |
| 55 | 0.664000 |
| 56 | 0.741400 |
| 57 | 0.811300 |
| 58 | 0.796500 |
| 59 | 0.666300 |
| 60 | 0.634800 |
