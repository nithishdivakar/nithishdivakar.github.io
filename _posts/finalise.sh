nbdev_nb2md $1.ipynb 
python finalise.py $1.md
rm -r ../images/$1_files
cp -r $1_files ../images/
rm -r $1_files