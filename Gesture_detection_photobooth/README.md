
## Authors

- [@peteproj](https://github.com/peteproj)
- [@josbor1](https://github.com/josbor1)

## Setup

Gether the necessary supplies mentioned in the README file

## Camera Setup 

1. Locate the camera connectors on the Pi. These are located right behind the
Ethernet port.

2. When using the Arducam,you will need to gently use your fingers on each side of the gray connector tab and lift up.

3. On the other end of your orange ribbon cable, there is a black side and a gold side. The gold side should face towards the Ethernet port. Your cable should fit into the groove of the connector tab.

4. Gently press the cable as far as it will go, but do not force it! Close the connector
tab by pressing it back down into the housing. Your cable should not move.

5. Open a Terminal window and enter in the following command:

```bash
  sudo apt install libcamera-apps
```
6. Then enter in the terminal: 
```bash
udo nano /boot/firmware/config.txt
```
7. Find the line that says: camera_auto_detect=1, and change the “1” to a “0”

8. Find the line that says “[all]”, and add the following line underneath it:

```bash
dtoverlay=ov5647,camX
```
Where X is the number of your display port. Check near the headers for the
correct number. 0 is closest to the Ethernet, 1 is closest to the HDMI ports.

9. To save, press “CTRL + X” on your keyboard, press “Y” to confirm, and then “Enter” to confirm again. You’ll need to reboot your Pi to make these changes.

10. Once your Pi has rebooted, open a Terminal window and enter the following
command:

```bash
libcamera-hello -t 0
```
You should see a new window with a working camera feed!

## Prep for ML training
1. Now, we need to take some pictures to train our model on what your gesture look like. In my case I will be making a peace sign.

2. On the Desktop of your Pi, make two new folders, called , “peace sign”, and
“no peace sign", respectively.

3. Right click on any one of them and click on “open in Terminal”. This saves you a
step in having to use the “cd” command!

4. Enter in the following command.

```bash
libcamera-still --timeout 150000 --timelapse 100 -o image%04d.jpg --vf
```

This will take a picture about every 1/10th of a second. When you press “Enter”, you will see a preview window. Make the appropriate gesture with your hand and make sure it is visible within the center of the frame. Move your hand around some to get some variety in the data. This process takes about 2 and a half minutes, so be patient! The camera screen will go away when the process is done:

```bash
libcamera-still --timeout 150000 --timelapse 100 -o image%04d.jpg --vf
```

If your picture is upside down, you can remove the argument --vflip to fix that!

5. Move on to the other folder and repeat steps 3-5. EXCEPT you will want to take photos of everything else but the hang gesture like background and face. You will want a separate folder for each gesture.

7. You should have ~150-180 pictures in each folder.

## Training your model with your samples

1. Using the web browser, search for “Teachable Machine” and open the
webpage.

2. Click on “Get Started” and then “Image Project”. 

3. On the left side of the screen, you’ll see that you have a number of “classes” available. Each class represents something that you want to identify. In our case, we will want to rename the classes to be “Peace Sign”, and “No Peace Sign” in that order. You’ll need to create a new class to do so.

4. For each respective class, click on “Upload” and then navigate to the folders you just made. Open the folders, press CTRL + A to select everything, and then select “Open”.

5. Once each class has their respective pictures (ie, the model’s training data), expand the “Advanced” menu. Since our amount of training data is quite small comparatively, let’s increase the number of epochs, or generations, that this model is trained on to 300. This means that our model will run throug the dataset 300 times to make associations.

6. Click on “Train Model” to start the process. This will connect to Google’s servers to create your model for you. Trust me, you wouldn’t want to run through the computation necessary for training a model with a Raspberry Pi. 

7. Once it finishes, click on “Export Model”. We want to use the “Tensorflow Lite” option here. Leave the default “Floating point” setting and click on “Download my model”. This will download a ZIP folder to your Pi’s Downloads folder.

## Installing the dependencies
1. Open a new Terminal window and enter in the following command:

```bash
sudo pip install guizero opencv-python numpy tensorflow --break-
system-packages
```

2. I’ve already written some code for you that you’ll need to download from my
GitHub. Make sure that your Terminal is at the root level, and then enter the
following command:

```bash
git clone https://github.com/peteproj/Hand-Detection-with-ML/tree/main/Gesture_detection_photobooth
```

3. Delete the Tensorflow model. Navigate to your Downloads folder on the Pi and
find your model.

4. Right click on the ZIP folder that you downloaded earlier. Click on “extract here”.
You will get a familiar looking .tflite file. Copy and paste this back in the "Hand-Detection-with-ML" folder you were just in.

## Running the code
1. Open the py file in your editor of choice

2. Double check Line 12 matches your model’s file name

3. Double check that the gesture map on lines 21-23 matches your model

4. Hit Run on your editor and wait until the camera preview starts

5. Hit start and make your gesture to capture the frame which will be saved in the "photos" folder in the "Hand-Detection-with-ML" folder.
