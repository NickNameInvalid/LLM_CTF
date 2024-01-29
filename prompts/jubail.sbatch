#!/bin/bash

#SBATCH -q nvidia-xxl
#SBATCH -p nvidia
#SBATCH -C 80g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:a100:2
#SBATCH --time=0:59:59
#SBATCH --mem=50GB
#SBATCH --job-name=infer

module purge

MODEL=5
NUM_LOOPS=10

# Load the Conda module
source ~/.bashrc

# Activate your Conda environment
conda activate wizard

export TRANSFORMERS_CACHE="/scratch/bc3194/huggingface_cache"
export HF_HOME="/scratch/bc3194/huggingface_cache"
python -u wizardcoder_infer.py
