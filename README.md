# Docker Registry Cleaner
-------------------------

## Why?
Removing images from private registry is a painful and complicated process for me so i just wrote a simple python script with simple command to make it easy this complex once and for all.

## Structure
### libraries
All you need to run this script is listed in `requirments.txt` and you can install it with `pip`.

`pip install -r requirments.txt`

### Registry Class
`regsitry.py` is the main file that contains the `Registry` class. This class has main function you need to delete all list images of private registry.

### Cleaner
`cleaner.py` using `Regsitry` is a python script to work with the python class. I wrote it quickly and for my own usage so it will be a good idea to change it but it works fine for me.

## Docker Registry Configs
If you want to delete images from your Rgeitsry first you should set `storage.delete.enabled=true` in resgitry config file or if you are running Docker Regsitry like me set `REGISTRY_STORAGE_DELETE_ENABLED=true` env varibale. Otherwise you can not delete any image or digest.

## Current process of `cleaner.py`
First it caches all repositiries in registry and print it. You have three choice now.

 * Choose one of repositires to work with
 	* write its name 
 * Keep all of the images of reposiries except recentrly created ones. By default it keeps last 10.
 	* Type `last` to just keep last 10 images in each repository. (I use this one most of the time)
 	* Type `last N` to just keep last N images in each repository.
* Type `q` to quiet.


**Sorry for mistakes anyway i will make it better in future**

 	