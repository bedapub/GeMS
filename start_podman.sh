IMG_NAME="gems"
CONT_NAME="gems_cont"
PORT=1234

if [ ! "$(sudo podman ps -q -f name='$CONT_NAME')" ]; then
  echo "Found container with same name"

  if [ ! "$(sudo podman ps -aq -f status=exited -f name='$CONT_NAME')" ]; then
    echo "Container is still running. Stop container \"$CONT_NAME now\""
    sudo podman stop "$CONT_NAME"
  fi

  echo "Remove container $CONT_NAME"
  sudo podman rm "$CONT_NAME"

fi

echo "Build container"
sudo podman build -t "$IMG_NAME" .
echo "Run container"
#sudo podman run -p "$PORT":1234 --name "$CONT_NAME" "$IMG_NAME"

sudo podman run -d -e MONGODB_USERNAME=dbuser \
-e MONGODB_PASSWORD=dbpass \
-e MONGODB_HOST=dbhost \
-e MONGODB_PORT=dbport \
-e MONGODB_DB=dbname \
-p "$PORT":1234 --name "$CONT_NAME" "$IMG_NAME"

