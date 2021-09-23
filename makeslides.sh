# Script that copies selected output into final figures

# To make script executable: chmod a+x makesplides.sh

printf "\nMaking slides...\n\n"

# Move to directory
cdir="Dropbox/Projects/Machine-Learning-for-Economic-Analysis"
wdir="Dropbox/code/website/course/ml-econ"

# Convert slides
jupyter nbconvert ${cdir}/1_regression.ipynb --to slides
jupyter nbconvert ${cdir}/2_iv.ipynb --to slides
jupyter nbconvert ${cdir}/3_nonparametric.ipynb --to slides
jupyter nbconvert ${cdir}/4_crossvalidation.ipynb --to slides
jupyter nbconvert ${cdir}/5_regularization.ipynb --to slides
jupyter nbconvert ${cdir}/6_convexity.ipynb --to slides
jupyter nbconvert ${cdir}/7_trees.ipynb --to slides
jupyter nbconvert ${cdir}/8_neuralnets.ipynb --to slides
jupyter nbconvert ${cdir}/9_postdoubleselection.ipynb --to slides
jupyter nbconvert ${cdir}/10_unsupervised.ipynb --to slides

# Copy slides
cp ${cdir}/1_regression.slides.html       ${wdir}/1-regression/index.html
cp ${cdir}/2_iv.slides.html               ${wdir}/2-iv/index.html
cp ${cdir}/3_nonparametric.slides.html    ${wdir}/3-nonparametric/index.html
cp ${cdir}/4_crossvalidation.slides.html  ${wdir}/4-crossvalidation/index.html
cp ${cdir}/5_regularization.slides.html   ${wdir}/5-regularization/index.html
cp ${cdir}/6_convexity.slides.html        ${wdir}/6-convexity/index.html
cp ${cdir}/7_trees.slides.html            ${wdir}/7-trees/index.html
cp ${cdir}/8_neuralnets.slides.html       ${wdir}/8-neuralnets/index.html
cp ${cdir}/9_postdoubleselection.slides.html ${wdir}/9-postdoubleselection/index.html
cp ${cdir}/10_unsupervised.slides.html    ${wdir}/10-unsupervised/index.html

# Copy slides
cd Dropbox/Projects/Empirical-io/1_introduction.slides.html Dropbox/Code/website/content/courses

# Terminate
exit
