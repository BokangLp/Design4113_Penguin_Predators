import tensorflow as tf
from tensorflow import keras
from keras import callbacks
from callbacks import EarlyStopping, ModelCheckpoint 

# Define your model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(3, activation='softmax')  # 3 classes
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Callbacks for dynamic training
early_stop = EarlyStopping(
    monitor='val_loss',       # or 'val_accuracy'
    patience=5,               # wait 5 epochs without improvement
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath='best_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    save_weights_only=False
)

# Training the model dynamically
"""
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,                      # upper limit, will stop early
    callbacks=[early_stop, checkpoint],
    verbose=1
)
""" 

# Find the best epoch for training
best_epoch = early_stop.stopped_epoch - early_stop.patience
print(f"Best epoch: {best_epoch}")