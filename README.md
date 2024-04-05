# WallStreetPulse
Use a virtual environment of Python 3.10/3.11 
pip install -r requirements.txt

# Analyzing the GameStop Event on Reddit's WallStreetBets Using Large Language Models

## Overview

This project aims to analyze the GameStop event that occurred on the Reddit community r/WallStreetBets in January 2021, where a coordinated effort by retail investors drove a massive short squeeze on GameStop (GME) stock. We utilize large language models (LLMs) to gain insights into the dynamics of this event and the impact of online communities on real-world financial markets.

## Motivation

The GameStop event highlighted the potential influence of online communities and social media on financial markets, demonstrating the power of coordinated retail investor actions. Our goal is to leverage the capabilities of large language models to understand the underlying factors that contributed to this event, including the flow of information, user activities, and sentiment within the r/WallStreetBets community.

## Challenges

1. **Data Retrieval**: The Reddit API only provides access to the most recent 1,000 posts, limiting our ability to gather historical data from r/WallStreetBets during the critical time period of the GameStop event.

2. **Modeling as a Social Network**: The r/WallStreetBets subreddit can be viewed as a complex social network, with users interacting, sharing information, and influencing each other's decisions. Modeling the flow of information and the dynamics within this network is a challenging task.

3. **Analyzing User Activities with Large Language Models**: Effectively prompting and querying large language models to extract valuable insights from user activities and discussions within the r/WallStreetBets community requires careful consideration and experimentation.

## Approach

1. **Data Collection Pipeline**: We developed a custom data collection pipeline to retrieve posts and comments from the r/WallStreetBets subreddit during the GameStop event, overcoming the limitations of the Reddit API.

2. **Social Network Modeling**: We modeled the r/WallStreetBets subreddit as a social network, analyzing the flow of information and the interactions between users.

3. **Large Language Model Analysis**: We leveraged the power of large language models, including specialized models like FinGPT, fine-tuned on financial data, to analyze user activities and discussions within the r/WallStreetBets community.

## Results

Our analysis provided valuable insights into the impact of online communities and social media on real-world financial events. We demonstrated the effectiveness of large language models in understanding the dynamics of these communities and their influence on market behavior.

1. We provide an analysis model specifically for GME stock during the 2021 GME event period. The model aims to determine whether or not the market will crash at a certain date of GME event with adjustable input parameters indicating the community size of individual investors of r/WallStreetBets.
2. We provide a pipeline that gets the r/WallStreetBets parameters for the provided model. 

## Future Work

- Experiment with different prompting strategies to extract more specific insights from large language models.
- Explore the use of fine-tuned or specialized language models, such as FinGPT, for enhanced financial or social media analysis.
- Develop visualizations to better represent the complex networks and information flow within online communities.
- Apply similar methodologies to other online communities across various domains to study their impact and dynamics.

