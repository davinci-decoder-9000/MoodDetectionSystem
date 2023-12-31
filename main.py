import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2

import time
from datetime import datetime
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
from email.message import EmailMessage

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Email configuration
sender_email = "davincidecoder878@gmail.com"  # Sender's email address
receiver_email = "shiouya878@gmail.com"  # Recipient's email address
# receiver_email = "carlxavier.c.valdez@isu.edu.ph"  # Recipient's email address
password = "muoniwayweihhgyn"  # Sender's email password
subject = 'Hello from Python!'
message = 'linux'


def send_email(emotion, sender_email, sender_password, receiver_email, subject, message):
    # Create the email message
    email_message = EmailMessage()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    email_message.set_content(emotion)

    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Connect to the SMTP server
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()

    # Login to the Gmail account
    smtp_connection.login(sender_email, sender_password)

    # Send the email
    smtp_connection.send_message(email_message)

    # Close the connection
    smtp_connection.quit()


# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode", help="train/display")
mode = ap.parse_args().mode

# plots accuracy and loss curves


def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    # summarize history for accuracy
    axs[0].plot(range(1, len(model_history.history['accuracy']) + 1),
                model_history.history['accuracy'])
    axs[0].plot(range(1, len(model_history.history['val_accuracy']) + 1),
                model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1, len(model_history.history['accuracy']) + 1),
                      len(model_history.history['accuracy']) / 10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1, len(model_history.history['loss']) + 1),
                model_history.history['loss'])
    axs[1].plot(range(1, len(model_history.history['val_loss']) + 1),
                model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1, len(
        model_history.history['loss']) + 1), len(model_history.history['loss']) / 10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()


# Define data generators
train_dir = 'data/train'
val_dir = 'data/test'

num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50
learning_rate = 0.01
decay_rate = learning_rate / num_epoch
optimizer = tf.keras.optimizers.Adam(lr=learning_rate, decay=decay_rate)

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(48, 48),
    batch_size=batch_size,
    color_mode="grayscale",
    class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(48, 48),
    batch_size=batch_size,
    color_mode="grayscale",
    class_mode='categorical')

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3),
          activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# If you want to train the same model or try other models, go for this
if mode == "train":
    model.compile(loss='categorical_crossentropy', optimizer=Adam(
        lr=0.0001, decay=1e-6), metrics=['accuracy'])
    model_info = model.fit_generator(
        train_generator,
        steps_per_epoch=num_train // batch_size,
        epochs=num_epoch,
        validation_data=validation_generator,
        validation_steps=num_val // batch_size)
    plot_model_history(model_info)
    model.save_weights('model.h5')

# emotions will be displayed on your face from the webcam feed
elif mode == "display":
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fear",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # start the webcam feed
    cap = cv2.VideoCapture(0)
    # Image
    # Folder to where image to save
    imagesFolder = "C:/Users/" + getpass.getuser() + "/documents/images"
    frameRate = cap.get(5)  # frame rate
    start_time = time.time()  # Get current time
    capture_time = 0

    # Video
    vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, 50.0, (640, 480))

    while cap.isOpened():
        # Frame Rate --Depends on the Camera
        frameId = cap.get(1)
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()

        curr_time = time.time()
        time_elapsed = curr_time - start_time
        if time_elapsed > 60:
            break

        if not ret:
            break

        #
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y - 50),
                          (x + w, y + h + 10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))

            cv2.putText(frame, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 51), 2, cv2.LINE_AA)

            if time_elapsed >= capture_time:
                filename = imagesFolder + "/image_" + \
                    str(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")) + ".png"
                cv2.imwrite(filename, frame)
                capture_time += 5

            # Check for fear or angry emotion
            # print(emotion_dict[maxindex])
            if emotion_dict[maxindex] == "Fear" or emotion_dict[maxindex] == "Angry":
                # send_email_alert(emotion_dict[maxindex])
                send_email(emotion_dict[maxindex], sender_email, password,
                           receiver_email, subject, message)

        cv2.imshow('Video', cv2.resize(
            frame, (780, 540), interpolation=cv2.INTER_LINEAR))
        output.write(frame)
        cv2.waitKey(1)

    cap.release()
    output.release()
    cv2.destroyAllWindows()
