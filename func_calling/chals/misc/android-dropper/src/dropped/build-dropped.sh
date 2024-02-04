#!/bin/sh

rm dropped.b64
rm Dropped.class
rm Dropped.jar
rm classes.dex

javac -source 8 -target 8 Dropped.java 
jar cvf Dropped.jar Dropped.class
d8 --lib "${ANDROID_HOME}/platforms/android-33/android.jar" Dropped.jar

base64 -w 0 -i classes.dex > dropped.b64
