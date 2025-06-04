# To Embody or Not: The Effect Of Embodiment On User Perception Of LLM-based Conversational Agents

[Paper](https://arxiv.org/abs/2506.02514)

![Embodied agent interface](images/interface_embodied.png)

Embodiment in conversational agents (CAs) refers to the physical or visual representation of these agents, which can significantly influence user perception and interaction. Limited work has been done examining the effect of embodiment on the perception of CAs utilizing modern large language models (LLMs) in non-hierarchical cooperative tasks, a common use case of CAs as more powerful models become widely available for general use. To bridge this research gap, we conducted a mixed-methods within-subjects study on how users perceive LLM-based CAs in cooperative tasks when embodied and non-embodied. The results show that the non-embodied agent received significantly better quantitative appraisals for competence than the embodied agent, and in qualitative feedback, many participants believed that the embodied CA was more sycophantic than the non-embodied CA. Building on prior work on users' perceptions of LLM sycophancy and anthropomorphic features, we theorize that the typically-positive impact of embodiment on perception of CA credibility can become detrimental in the presence of sycophancy. The implication of such a phenomenon is that, contrary to intuition and existing literature, embodiment is not a straightforward way to improve a CA's perceived credibility if there exists a tendency to sycophancy.

This repository contains the code and instructions needed to replicate the study conducted, including the embodied CA.

## Quickstart Guide

1. Download [Nvidia Omniverse](https://developer.nvidia.com/omniverse) and install [Audio2Face](https://docs.omniverse.nvidia.com/audio2face/latest/overview.html).
2. Download [Unreal Engine](https://www.unrealengine.com/en-US/download).
3. Download [LM Studio](https://lmstudio.ai/), and load Llama 3.1 8B Instruct in a Local Inference Server.
4. Load the [Omniverse USD file](embodied_assets/audio2face.usd) in Audio2Face. Go to the "A2F Data Conversion" tab, click the option in "BlendShape Solver(s)", and click "DELETE SETUP". Then click "SET UP BLENDSHAPE SOLVE". Next, select the "StreamLivelink" object in the Stage window. Then, check "Activate" in the Property window.
5. In a terminal, load a virtual Python environment with the appropriate libraries installed, and run the [provided script](scripts/MainScript_desert_voice.py).
6. Open the Unreal Engine project file and load the "level_combined" level. Click the "+ Source" button in the Live Link tab, hover over the NVIDIA Omniverse LiveLink option, and click "OK". Press Alt+P.
7. You may now chat with the agent in the terminal window.

8. ## citation

If you find this work interesting, please cite our paper: 

   ```
   @article{wang2025embodynoteffectembodiment,
      title={To Embody or Not: The Effect Of Embodiment On User Perception Of LLM-based Conversational Agents}, 
      author={Kyra Wang and Boon-Kiat Quek and Jessica Goh and Dorien Herremans},
      year={2025},
      title={arXiv: 2506.02514}
}
   ```
