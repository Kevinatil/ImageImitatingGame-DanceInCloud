
# Images Imitating Game with Openpose from  *Dance In Cloud*  Team

A game for image imitating and scoring using scoring process designed by *Dance In Cloud* Team.


## Introduction
This repo provides a game to do image imitating scoring and evaluating. You can choose a target image with single person to imitate.

This version supports *image* imitating and scoring. For video imitating and scoring, please turn to [MoveImitatingGame-DanceInCloud](https://github.com/Kevinatil/MoveImitatingGame-DanceInCloud).You can put your target images into `origin_pics` folder, and use your camera to imitate the image. The framework will do pose estimation and give you a score based on your performance. The score includes total score and detail scores for each joint.

## Environment

The scoring process is based on [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose), and [ffmpeg](https://ffmpeg.org/). Please configure them before running this framework.

```bash
# After configuring OpenPose and ffmpeg, run command to install packages
pip install -r requirements.txt
```

## Demo

The interface and scoring process are shown below. The scoring process is obfuscated by `pyarmor` because of the commercial usage.

![img](https://github.com/Kevinatil/ImageImitatingGame-DanceInCloud/blob/main/media/show.gif)

## Usage

1. Put the target image into `origin_pics` folder;

2. Run *origin.bat* to generate rendered images and json files;

3. Run *imitate.py* after changing the work directory based on your environment;

4. Click *take photos* and *show score* to get the scores of your imitation;

5. The scoring process can be restarted by clicking input box.


## Quick start

You can watch a scoring demo by setting the `pose`, `camera` and `del_all` as *False* in the `photo_score` function in `imitate.py`. The scoring function will use cached json files to do scoring.

```python
elif 5<x<140 and 70<y<120:
    score,name_score=photo_score(ns=name[:-4], num=num, 
                                 camera=True, pose=True, del_all=True) # set as False to use cached json files to score
```
