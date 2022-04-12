ECHO Starting enrico...
:: activate conda environment
CD C:\Users\Fermi1-YCAM\anaconda3\Scripts
CALL activate.bat
CALL conda.bat activate pylablib

CD /d C:\Users\Fermi1-YCAM\Documents\Github\fermi1AndorCamera
ECHO DID YOU CLOSE THE PREVIOUS INSTANCE OF THE YCAM?
PAUSE
START python darkSpotProbe_util.py