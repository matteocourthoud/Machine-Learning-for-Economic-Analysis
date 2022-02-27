# Script that copies selected output into final figures

# To make script executable: chmod a+x makesplides.sh

printf "\nMaking slides...\n\n"

# Save directories
indir="Dropbox/Projects/Machine-Learning-for-Economics"
outdir="Dropbox/Code/website/content/course/ml-econ"

# List files
cd ${indir}/notebooks/
FILES=$(ls *.ipynb)
cd

# Convert slides
for FILE in $FILES; do
  file=$(echo $FILE | cut -d'.' -f 1)
  jupyter nbconvert ${indir}/notebooks/${file}.ipynb --to markdown --NbConvertApp.output_files_dir=../img
  #jupyter nbconvert ${indir}/notebooks/${file}.ipynb --to slides
  #mv ${indir}/notebooks/${file}.slides.html ${indir}/slides/${file}.slides.html
  #cp ${indir}/slides/${file}.slides.html ${outdir}/${file}_slides/index.html

  # Move to website
  mv ${indir}/notebooks/${file}.md ${outdir}/${file}.md
  cp -R ${indir}/img ${outdir}
  python3 ${indir}/rename.py "${outdir}/" "${file}.md"
done

# Terminate
exit
