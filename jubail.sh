#!/bin/bash

#SBATCH -p nvidia
#SBATCH -C 80g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:a100:2
#SBATCH --time=0:59:59
#SBATCH --mem=150GB
#SBATCH --job-name=infer
#SBATCH --output=/home/ms12416/projects/LLM_CTF/output/mixtral.out

module purge

MODEL=5
NUM_LOOPS=10

# Load the Conda module
source ~/.bashrc

# Activate your Conda environment
conda activate llm_ctf

export TRANSFORMERS_CACHE="/scratch/ms12416/hf_cache"
export HF_HOME="/scratch/ms12416/hf_cache"
python -u experiments/mixtral_infer.py