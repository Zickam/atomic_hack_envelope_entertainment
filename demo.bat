@REM call conda create -n env
@REM call conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
@REM call conda install python==3.11 transformers pypdf2 faiss -c pytorch -c conda-forge
call pip install transformers
call pip install pypdf2
call pip install faiss-cpu
call pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
call pip install langchain-community
call pip install sentence-transformers
cd src
call python demo.py
call echo "exiting the app..."
@REM call timeout 100000