# Second sub-project

### 1. Requirements

Study a DL model for object detection, implement and evaluate the performance on public dataset. You must explain the reason for choosing the model, well understand it and analyze the obtained results.

### 2. Evaluation

- Checkpoint: DETR Resnet 50
- Dataset: COCO2017 valset
- Results:
  ![Evaluation](imgs/evaluation.png)

### 3. Inference result

**Inference on large object**
![Large object](imgs/000000018380.jpg)

**Inference on small object**
![Small object](imgs/000000303713.jpg)

### 4. Visualize attention

**Original detection**
![Detection](imgs/000000039769.jpg)

**Decoder attention**
![Decoder](imgs/decoder_attention.jpg)

**Encoder attention**
![Encoder](imgs/encoder_attention.jpg)
