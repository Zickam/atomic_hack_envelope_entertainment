#sudo apt install python3.11
#curl --output anaconda_installer.sh "https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh"
#chmod +x ./anaconda_installer.sh
#./anaconda_installer.sh

conda install python==3.11 transformers pypdf2 faiss -c pytorch -c conda-forge
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install langchain-community
pip install sentence-transformers
