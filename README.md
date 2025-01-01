# How to create ELAN ANNOTATIONS

This requires you having in this directory foler Input_Videos with all videos we want to annotate

1. Open Anaconda Prompt
2. Navigate into the main folder of this directory - cd C:/FLESH_IteratedLearning
3. Run python file - python create_ELAN.py

This should lead to creating folder ELAN_anno with bunch of .eaf files, each corresponding to a video file from Input_Videos. By opening it in ELAN, you should directly see the video as well as template as we know it from previous work.

4. Annotate gesture on- and offsets in various body regions (If you wish to annotate only movement_in_trial and hands/arms, just ignore the rest)
5. Save the .eaf file.
