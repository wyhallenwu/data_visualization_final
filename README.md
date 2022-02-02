# Data Visualization Final Project
## Introduction
This is the final project for course "data visualization". After changing topics repeatedly, I finally choose "metaverse tokens and cryptocurrencies" as my topic. There are obvious reasons, (1) after facebook regroup as meta, metaverse becomes a big hit. (2) metaverse tokens and currencies haven't been seriously 
concerned(2022-02-02) (3) will metaverse be economic bubble?  
These questions are interesting and I will try to disclose and explain some of these questions in this project. But I only know a little about economy, my analysis maybe naive and has mistakes. It doesn't matter. If you could point it out and discuss with me, I would appreciate it a lot.  
## Dataset
> This dataset is collected by myself, the source website is: https://coinmarketcap.com/  
> coinmarketcap has already provide api to access some data, but it charges. So I write a rough crawler
### Dataset structure
I provide datasets both in csv and json format. Each file is named by its original name.  
I collect 76 kinds tokens'(the rank100 but other 24 doesn't have 120 days data or already expired) historical data.  
| Date | Open | High | Low | Close | Volume | Marketcap |
| ---- | ---- | ---- | --- | ----- | ------ | --------- |

**Date**: from 2021-10-05 to 2022-02-01  
**Volume**: 

## Usage
I will refactor the whole project to make it more usage-friendly. I strongly you rewrite some parts of the crwaler.py because I directly use sleep(), but there are better ways. I will rewrite it later.

## Schedule
- [x] crawler
- [x] collect dataset
- [ ] analyze
- [ ] visualize