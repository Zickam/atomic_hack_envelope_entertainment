@REM call conda create -n env
@REM call conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
@REM call conda install python==3.11 transformers pypdf2 faiss -c pytorch -c conda-forge
call install_deps
cd src
call python demo.py
call echo "exiting the app..."
@REM call timeout 100000