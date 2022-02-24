if [ -n "$SSH_CLIENT" ]; then
  echo "Remote login detected"
else
  echo "starting acarsdec"
  python acarsdisp.py > pylog.txt &
  acarsdec -l acars.log -D -j 127.0.0.1:5555 -r 0 131.55
fi

