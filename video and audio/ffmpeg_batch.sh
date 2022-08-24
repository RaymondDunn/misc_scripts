for i in *.MOV;
  do name=`echo "$i" | cut -d'.' -f1`
  echo "$name"
  ffmpeg -i "$i" -vcodec h264_nvenc -preset slow -profile:v high "${name}.mp4"
done