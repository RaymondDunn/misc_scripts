# for creating conda environment
# adapted from my blog post 2018-08-06-getting-inside-micromanager.md
conda create -n micro-manager-3-6
activate micro-manager-p3
conda install -c conda forge opencv ffmpeg

echo "Do not forget to copy MMCorePy into the appropriate Micro-Manager directory!"

