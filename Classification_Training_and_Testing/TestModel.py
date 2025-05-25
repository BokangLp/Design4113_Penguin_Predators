from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load model
model = load_model("Penguin_Badger.h5")

# Test data path
test_path = r'C:\Users\Bokang Lepolesa\OneDrive - University of Cape Town\SCHOOL WORK\UCT\Year 4\Design\PHBTesting'

# Data generator
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    test_path,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Reverse class indices
label_map = {v: k for k, v in test_generator.class_indices.items()}

# Collect predictions and ground truths
all_y_true = []
all_y_pred = []
misclassified = []

# Evaluate and collect predictions
for i in range(len(test_generator)):
    batch_x, batch_y = test_generator[i]
    preds = model.predict(batch_x)
    y_true = np.argmax(batch_y, axis=1)
    y_pred = np.argmax(preds, axis=1)

    all_y_true.extend(y_true)
    all_y_pred.extend(y_pred)

    for j in range(len(y_true)):
        if y_true[j] != y_pred[j]:
            img = batch_x[j]
            misclassified.append({
                "image": img,
                "true_label": label_map[y_true[j]],
                "predicted_label": label_map[y_pred[j]]
            })

# Convert to numpy arrays
all_y_true = np.array(all_y_true)
all_y_pred = np.array(all_y_pred)

# False Positives and False Negatives
fp = np.sum((all_y_true == 1) & (all_y_pred == 0))  # Penguin predicted as Badger
fn = np.sum((all_y_true == 0) & (all_y_pred == 1))  # Badger predicted as Penguin
total_penguins = np.sum(all_y_true == 1)
total_badgers = np.sum(all_y_true == 0)

fp_percent = 100 * fp / total_penguins if total_penguins > 0 else 0
fn_percent = 100 * fn / total_badgers if total_badgers > 0 else 0

print(f"False Positives (Penguin → Badger): {fp} / {total_penguins} ({fp_percent:.2f}%)")
print(f"False Negatives (Badger → Penguin): {fn} / {total_badgers} ({fn_percent:.2f}%)")
print(f"Size of misclassified: {len(misclassified)}")

# ---- Optional: Misclassified Images Display ----
num_to_show = min(12, len(misclassified))
plt.figure(figsize=(15, 10))
for i in range(num_to_show):
    plt.subplot(3, 4, i + 1)
    plt.imshow(misclassified[i]["image"])
    plt.title(f"True: {misclassified[i]['true_label']}\nPred: {misclassified[i]['predicted_label']}")
    plt.axis('off')
plt.suptitle("Examples of Misclassified Images", fontsize=16)
plt.tight_layout()
plt.show()
