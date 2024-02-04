#!/usr/bin/env bash

echo "Before running this, make sure you set the server correctly in ../dropped/Dropped.java"
echo "Currently, it is set to:"
grep "// replace" ../dropped/Dropped.java | sed 's/^ *//'
echo "Hit enter to continue, or Ctrl-C to cancel"
read

cd ../dropped/
bash build-dropped.sh
if [ ! -f "dropped.b64" ]; then
    echo "Error: dropped.b64 not found"
    exit 1
fi
cd ../dropper/

echo "Inserting base64 encoded payload into app/src/main/java/com/example/dropper/MainActivity.java"
sed 's|XXX_BASE64_HERE_XXX|'"$(cat ../dropped/dropped.b64)"'|' app/src/main/java/com/example/dropper/MainActivity.java.template \
    > app/src/main/java/com/example/dropper/MainActivity.java

echo "Building dropper"
chmod +x ./gradlew
./gradlew clean
./gradlew build

echo "Signing dropper"
zipalign -v -p 4 app/build/outputs/apk/release/app-release-unsigned.apk app/build/outputs/apk/release/app-release-unsigned-aligned.apk
echo csaw2023 | apksigner sign --ks csaw2023.jks --out dropper.apk app/build/outputs/apk/release/app-release-unsigned-aligned.apk

echo "Dropper is ready in: dropper.apk"
apksigner verify dropper.apk && echo "Verification successful" || echo "Verification failed"
